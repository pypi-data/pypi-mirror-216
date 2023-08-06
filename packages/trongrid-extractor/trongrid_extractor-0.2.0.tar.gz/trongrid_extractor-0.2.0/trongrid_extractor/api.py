'''
API wrapper for TronGrid.
'''
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import pendulum
import requests
from pendulum import DateTime
from rich.pretty import pprint
from tenacity import retry, wait_exponential

from trongrid_extractor.config import log
from trongrid_extractor.helpers.csv_helper import *
from trongrid_extractor.helpers.string_constants import *
from trongrid_extractor.helpers.time_helpers import *
from trongrid_extractor.progress_tracker import ProgressTracker
from trongrid_extractor.trc20_txn import Trc20Txn

JSON_HEADERS = {'Accept': 'application/json'}
MAX_TRADES_PER_CALL = 200
RESCUE_WINDOW_DURATION_MS = 20000.0
ONE_SECOND_MS = 1000.0


class Api:
    def __init__(self, network: str = MAINNET, api_key: str = '') -> None:
        network = '' if network == MAINNET else f".{network}"
        self.base_uri = f"https://api{network}.trongrid.io/v1/"
        self.api_key = api_key

    def events_for_token(
            self,
            contract_addr: str,
            since: Optional[DateTime] = None,
            until: Optional[DateTime] = None,
            output_dir: Optional[Path] = Path(''),
            event_name: Optional[str] = 'Transfer'
        ) -> None:
        """
        Get events by contract address and write to CSV. This is the endpoint that actually works
        to get all transactions (unlike the '[CONTRACT_ADDRESS]/transactions' endpoint).

        Test harness: https://developers.tron.network/v4.0/reference/events-by-contract-address
        """
        contract_url = f"{self.base_uri}contracts/{contract_addr}/events"
        log.info(f"Retrieving {event_name} events from {since} to {until} from '{contract_url}'")
        params = Api.build_params(since, until, extra={'event_name': event_name})
        log.info(f"Initial params: {params}")

        # Start retrieving
        response = Api.get_response(contract_url, params)
        retrieved_txns = Trc20Txn.extract_from_events(response)
        progress_tracker = ProgressTracker(retrieved_txns)

        # Setup and write to CSV
        output_csv_filename = output_csv_path(contract_addr, output_dir)
        write_rows(output_csv_filename, retrieved_txns)
        force_continue_from_rescue = False

        # This uses the "next_url" approach which fails after a while.
        while self._is_continuable_response(response) or force_continue_from_rescue:
            force_continue_from_rescue = False
            next_url = response[META][LINKS][NEXT]
            log.debug(f"Retrieving next URL '{next_url}'...")
            response = Api.get_response(next_url)

            # Therefore when it fails we go back to filtering by timestamp.
            # I tried something involving the response[META][FINGERPRINT] but didn't help.
            if not response[SUCCESS]:
                log.info(f"Failed to retrieve provided next URL. Moving end timestamp and restarting...")
                log.debug(f"  Next URL: '{next_url}'")
                params[MAX_TIMESTAMP] = str(progress_tracker.earliest_block_timestamp_seen)
                log.debug(f"  Setting {MAX_TIMESTAMP} to {params[MAX_TIMESTAMP]}")
                response = Api.get_response(contract_url, params)

            retrieved_txns = Trc20Txn.extract_from_events(response)
            retrieved_txns = progress_tracker.remove_already_processed_txns(retrieved_txns)

            # See comment on _rescue_extraction() but tl;dr TronGrid is broken.
            if len(retrieved_txns) == 0:
                log.warning(f"0 txns found. We seem to be stuck at {ms_to_datetime(params[MAX_TIMESTAMP])}.")
                pprint(response, expand_all=True)
                log.warning(f"  Params: {params}")
                retrieved_txns = self._rescue_extraction(contract_url, params)
                retrieved_txns = progress_tracker.remove_already_processed_txns(retrieved_txns)
                force_continue_from_rescue = True

            write_rows(output_csv_filename, retrieved_txns)

        log.info("Extraction loop is complete; here is the last response from the api for params: {params}")
        pprint(response, expand_all=True)

    def trc20_xfers_for_wallet(self, contract_addr: str, wallet_addr: str, token_type: str = TRC20) -> List[Trc20Txn]:
        """Use the TRC20 endpoint to get transfers for a particular wallet/token combo."""
        raise ValueError("Needs revision to use ProgressTracker and more.")
        wallet_url = f"{self.base_uri}accounts/{wallet_addr}/transactions/{token_type}"
        params = Api.build_params(extra={'contract_address': contract_addr})
        response = Api.get_response(wallet_url, params)
        txns = Trc20Txn.extract_from_response(response)

        while META in response and 'links' in response[META]:
            if DATA not in response or len(response[DATA]) == 0:
                break

            min_timestamp = min([tx.ms_from_epoch for tx in txns])
            params[MAX_TIMESTAMP] = str(min_timestamp)
            response = Api.get_response(wallet_url, params)
            txns.extend(Trc20Txn.extract_from_response(response))

        unique_txns = Trc20Txn.unique_txns(txns)
        log.info(f"Extracted a total of {len(txns)} txns ({len(unique_txns)} unique txns).")
        return unique_txns

    def txns_for_token(self, contract_addr: str) -> List[Trc20Txn]:
        """
        See README.md for example response. Note that this is a different endpoint than
        events_for_token() and it doesn't work as well.

        Test harness: https://developers.tron.network/v4.0/reference/testinput
        """
        raise ValueError("This endpoint doesn't really work.")
        contract_url = f"{self.base_uri}contracts/{contract_addr}/transactions"
        params = Api.build_params(extra={'contract_address': contract_addr})
        response = Api.get_response(contract_url, params)
        return response

    def _is_continuable_response(self, response: Dict[str, Any]) -> bool:
        return META in response and LINKS in response[META] and NEXT in response[META][LINKS]

    def _rescue_extraction(self, url: str, params: Dict[str, str]) -> List[Trc20Txn]:
        """
        Try a smaller time range; maybe the "next URL" thing will work. The idea here is that the
        'next' URL paging doesn't work very well if you request a large timespan - it only lets
        you retrieve a few pages before barfing. So here we temporarily switch to a much smaller
        time range.

        Example problematic call:
             extract_tron_transactions TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t -u 2023-06-26T13:16:24+00:00
        """
        log.warning(f"Attempting rescue by requesting from max_timestamp minus {RESCUE_WINDOW_DURATION_MS} ms...")
        log.debug(f"Params: {params}")
        old_min_timestamp = params[MIN_TIMESTAMP]
        params[MIN_TIMESTAMP] = str(float(params[MAX_TIMESTAMP]) - RESCUE_WINDOW_DURATION_MS)
        response = Api.get_response(url, params)
        txns = Trc20Txn.extract_from_events(response)

        while self._is_continuable_response(response):
            next_url = response[META][LINKS][NEXT]
            log.debug(f"Retrieving next URL '{next_url}'...")
            response = Api.get_response(next_url)

            if not response[SUCCESS]:
                msg = f"Failed to retrieve next_url: '{next_url}'"
                log.error(f"{msg}\n\nFinal response:")
                pprint(response, expand_all=True)
                raise ValueError(msg)

            last_txns = Trc20Txn.extract_from_events(response)
            log.info(f"Rescued {len(last_txns)} more records")
            txns.extend(last_txns)

        log.debug(f"Exiting loop; no META or next url. Here's the final response: {response}")
        params[MAX_TIMESTAMP] = str(float(params[MIN_TIMESTAMP]) - ONE_SECOND_MS)
        params[MIN_TIMESTAMP] = old_min_timestamp
        log.info(f"  Returning {len(txns)} transactions from _rescue_extraction(), modified params in place.")
        log.debug(f"Modified params: {params}")
        return txns

    @staticmethod
    @retry(wait=wait_exponential(multiplier=1, min=4, max=60))
    def get_response(url: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Hit the endpoint and extract JSON data."""
        params = params or {}

        # Min/Max timestamps are INCLUSIVE.
        if MIN_TIMESTAMP in params and MAX_TIMESTAMP in params:
            msg = f"Requesting records from {ms_to_datetime(params[MIN_TIMESTAMP])} to {ms_to_datetime(params[MAX_TIMESTAMP])}."
            log.info(msg)

        log.debug(f"\nURL: {url}\nParams: {params}")
        response = requests.get(url, headers=JSON_HEADERS, params=params).json()
        log.debug(f"Response: {response}")
        return response

    @staticmethod
    def build_params(
            min_timestamp: Optional[DateTime] = None,
            max_timestamp: Optional[DateTime] = None,
            extra: Optional[Dict[str, Any]] = None
        ) -> Dict[str, str]:
        """Build params for requests. Anything besides min and max timestamp should go in 'extra'."""
        params = {
            'only_confirmed': 'true',
            'limit': str(MAX_TRADES_PER_CALL),
            MIN_TIMESTAMP: str(datetime_to_ms(min_timestamp or TRON_LAUNCH_TIME)),
            MAX_TIMESTAMP: str(datetime_to_ms(max_timestamp or pendulum.now('UTC').add(seconds=1)))
        }

        return {**params, **(extra or {})}
