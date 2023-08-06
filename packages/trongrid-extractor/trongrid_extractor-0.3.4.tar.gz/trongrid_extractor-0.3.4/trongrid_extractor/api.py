'''
API wrapper for TronGrid.
'''
import os
import tempfile
from copy import deepcopy
from pathlib import Path
from time import sleep
from typing import Any, Dict, List, Optional

import pendulum
import requests
from pendulum import DateTime
from rich.pretty import pprint
from tenacity import after_log, retry, stop_after_attempt, wait_exponential

from trongrid_extractor.config import log
from trongrid_extractor.helpers.csv_helper import *
from trongrid_extractor.helpers.string_constants import *
from trongrid_extractor.helpers.time_helpers import *
from trongrid_extractor.progress_tracker import ProgressTracker
from trongrid_extractor.response import Response
from trongrid_extractor.trc20_txn import Trc20Txn

MAX_TRADES_PER_CALL = 200

RESCUE_DURATION_WALKBACK_SECONDS = [
    20,
    3600,
    24 * 3600
]

ONE_SECOND_MS = 1000.0
EMPTY_RESPONSE_RETRY_AFTER_SECONDS = 60

# Currently we poll from the most recent to the earliest events which is perhaps non optimal
ORDER_BY_BLOCK_TIMESTAMP_ASC = 'block_timestamp,asc'
ORDER_BY_BLOCK_TIMESTAMP_DESC = 'block_timestamp,desc'


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
            filename_suffix: Optional[str] = None,
            resume_csv: Optional[Path] = None,
            event_name: Optional[str] = 'Transfer'
        ) -> Path:
        """
        Get events by contract address and write to CSV. This is the endpoint that actually works
        to get all transactions (unlike the '[CONTRACT_ADDRESS]/transactions' endpoint).

        Test harness: https://developers.tron.network/v4.0/reference/events-by-contract-address
        """
        contract_url = f"{self.base_uri}contracts/{contract_addr}/events"
        log.info(f"Retrieving '{event_name}' events since {since} until {until} from '{contract_url}'")
        params = Api.build_params(since, until, extra={'event_name': event_name})
        log.info(f"Initial params: {params}")

        # Resume from CSV if requested
        if resume_csv:
            if not resume_csv.exists():
                raise ValueError(f"CSV '{resume_csv}' doesn't exist!")

            progress_tracker = ProgressTracker.resume_from_csv(resume_csv)
            params[MAX_TIMESTAMP] = progress_tracker.earliest_block_timestamp_seen
            log.info(f"Resuming CSV '{resume_csv}' from {ms_to_datetime(params[MAX_TIMESTAMP])}...")
            output_csv_filename = resume_csv
        else:
            progress_tracker = ProgressTracker()
            output_csv_filename = output_csv_path(contract_addr, output_dir, filename_suffix)

        # Start retrieving
        response = Response.get_response(contract_url, params)
        retrieved_txns = Trc20Txn.extract_from_events(response.response)
        retrieved_txns = progress_tracker.remove_already_processed_txns(retrieved_txns)
        force_continue_from_rescue = False

        # Write to CSV
        write_rows(output_csv_filename, retrieved_txns)

        # This uses the "next_url" approach which fails after a while.
        while response.is_continuable_response() or force_continue_from_rescue:
            force_continue_from_rescue = False
            next_url = response.next_url()

            # Pull the next record
            if next_url is not None:
                log.debug(f"Retrieving next URL '{next_url}'...")
                response = Response.get_response(next_url)
            elif response.is_false_complete_response():
                # TODO: this should really use a retry block, otherwise can be an infinite loop
                log.warning(f"0 row response! Sleeping {EMPTY_RESPONSE_RETRY_AFTER_SECONDS}s and trying again...")
                log.warning(f"   Params: {params}\n   Response:")
                pprint(response, expand_all=True)
                sleep(EMPTY_RESPONSE_RETRY_AFTER_SECONDS)
                response = Response.get_response(contract_url, params)
            else:
                log.error(f"Unparseable response!")
                pprint(response, expand_all=True)
                raise ValueError("Unparseable response!")

            # Handle case where Trongrid barfs because we paged too much
            if response.is_paging_complete():
                log.info(f"Paging complete for {params}.")
                log.info(f"Setting {MAX_TIMESTAMP} to {progress_tracker.earliest_block_timestamp_seen}")

                # Log a simplified version of the response
                pprint(response.without_data(), expand_all=True)
                params[MAX_TIMESTAMP] = progress_tracker.earliest_block_timestamp_seen
                response = Response.get_response(contract_url, params)
            elif not response.was_successful():
                # When the "next URL" paging fails we go back to filtering by timestamp but move
                # the max_timestamp parameter. (I tried something involving the response[META][FINGERPRINT]
                # but it didn't help.)
                log.info(f"Failed to retrieve provided next URL. Moving end timestamp and restarting...")
                log.debug(f"  Next URL: '{next_url}'.\n  Setting {MAX_TIMESTAMP} to {params[MAX_TIMESTAMP]}")
                params[MAX_TIMESTAMP] = progress_tracker.earliest_block_timestamp_seen
                response = Response.get_response(contract_url, params)

            retrieved_txns = Trc20Txn.extract_from_events(response.response)
            retrieved_txns = progress_tracker.remove_already_processed_txns(retrieved_txns)

            # See comment on _rescue_extraction() but tl;dr TronGrid is broken.
            # TODO: is this actually necessary?
            if len(retrieved_txns) == 0:
                for walkback_seconds in RESCUE_DURATION_WALKBACK_SECONDS:
                    log.warning(f"0 txns found. We seem to be stuck at {ms_to_datetime(params[MAX_TIMESTAMP])}.")
                    log.warning(f"  (Maybe) Last request params: {params}")
                    pprint(response.response, expand_all=True)

                    # Get txns
                    retrieved_txns = self._rescue_extraction(contract_url, params, walkback_seconds)
                    retrieved_txns = progress_tracker.remove_already_processed_txns(retrieved_txns)

                    if len(retrieved_txns) > 0:
                        log.info(f"Rescued {len(retrieved_txns)}, forcibly continuing...")
                        force_continue_from_rescue = True
                        break

            write_rows(output_csv_filename, retrieved_txns)

        log.info("Extraction loop is complete; here is the last response from the api for params: {params}")
        pprint(response, expand_all=True)
        return output_csv_filename

    def trc20_xfers_for_wallet(self, contract_addr: str, wallet_addr: str, token_type: str = TRC20) -> List[Trc20Txn]:
        """Use the TRC20 endpoint to get transfers for a particular wallet/token combo."""
        raise ValueError("Needs revision to use ProgressTracker and more.")
        wallet_url = f"{self.base_uri}accounts/{wallet_addr}/transactions/{token_type}"
        params = Api.build_params(extra={'contract_address': contract_addr})
        response = Response.get_response(wallet_url, params)
        txns = Trc20Txn.extract_from_wallet_transactions(response)

        while META in response and 'links' in response[META]:
            if DATA not in response or len(response[DATA]) == 0:
                break

            min_timestamp = min([tx.ms_from_epoch for tx in txns])
            params[MAX_TIMESTAMP] = min_timestamp
            response = Response.get_response(wallet_url, params)
            txns.extend(Trc20Txn.extract_from_wallet_transactions(response))

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
        response = Response.get_response(contract_url, params)
        return response

    def _rescue_extraction(self, url: str, params: Dict[str, Union[str, float]], walkback: int) -> List[Trc20Txn]:
        """
        Try a smaller time range; maybe the "next URL" thing will work. The idea here is that the
        'next' URL paging doesn't work very well if you request a large timespan - it only lets
        you retrieve a few pages before barfing. So here we temporarily switch to a much smaller
        time range.

        IMPORTANT: The 'params' dict is modified by this method!
        'walkback' is the number of seconds between min_timestamp and max_timestamp

        Example problematic call:
             extract_tron_transactions TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t -u 2023-06-26T13:16:24+00:00
        """
        log.warning(f"Attempting rescue by requesting from max_timestamp minus {walkback} seconds...")
        log.debug(f"Params before new min_timestamp: {params}")

        old_min_timestamp = params[MIN_TIMESTAMP]
        params[MIN_TIMESTAMP] = params[MAX_TIMESTAMP] - (walkback * 1000.0)
        response: Response = Response.get_response(url, params)
        txns = Trc20Txn.extract_from_events(response.response)
        subtract_one_second = True

        while response.is_continuable_response():
            next_url = response.next_url()
            log.debug(f"Retrieving next URL '{next_url}'...")
            response = Response.get_response(next_url)

            if not response.was_successful():
                msg = f"Failed to retrieve next_url: '{next_url}'"
                log.error(f"{msg}\n\nFinal response:")
                pprint(response.response, expand_all=True)
                # If we fail to page all the whole response that means we might not yet have all the
                # records for that second in time.
                subtract_one_second = False
                break

            last_txns = Trc20Txn.extract_from_events(response.response)
            log.info(f"Rescued {len(last_txns)} more records")
            txns.extend(last_txns)

        log.debug(f"Exiting loop; no META or next url. Here's the final response: {response}")
        params[MAX_TIMESTAMP] = params[MIN_TIMESTAMP]

        if subtract_one_second:
            params[MAX_TIMESTAMP] -= ONE_SECOND_MS

        params[MIN_TIMESTAMP] = old_min_timestamp
        log.info(f"  Returning {len(txns)} transactions from _rescue_extraction(), modified params in place.")
        log.debug(f"Modified params: {params}")
        return txns

    @staticmethod
    def build_params(
            min_timestamp: Optional[DateTime] = None,
            max_timestamp: Optional[DateTime] = None,
            extra: Optional[Dict[str, Any]] = None
        ) -> Dict[str, Union[str, float, int]]:
        """Build params for requests. Anything besides min and max timestamp should go in 'extra'."""
        params = {
            'only_confirmed': 'true',
            'limit': MAX_TRADES_PER_CALL,
            MIN_TIMESTAMP: datetime_to_ms(min_timestamp or TRON_LAUNCH_TIME),
            MAX_TIMESTAMP: datetime_to_ms(max_timestamp or pendulum.now('UTC').add(seconds=1))
        }

        return {**params, **(extra or {})}
