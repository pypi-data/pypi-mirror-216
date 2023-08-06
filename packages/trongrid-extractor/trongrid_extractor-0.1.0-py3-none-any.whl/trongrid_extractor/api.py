'''

'''

import csv
import logging
import os
import tempfile
from locale import atof
from time import sleep
from typing import Any, Dict, List, Optional

import pendulum
import requests
from tenacity import retry, wait_exponential

from trongrid_extractor.config import log
from trongrid_extractor.helpers.csv_helper import *
from trongrid_extractor.helpers.string_constants import *
from trongrid_extractor.helpers.time_helpers import *
from trongrid_extractor.trc20_txn import Trc20Txn

JSON_HEADERS = {'Accept': 'application/json'}
MAX_TRADES_PER_CALL = 200
SLEEP_TIME = 1


class Api:
    def __init__(self, network: str = MAINNET, api_key: str = '') -> None:
        network = '' if network == MAINNET else f".{network}"
        self.base_uri = f"https://api{network}.trongrid.io/v1/"
        self.api_key = api_key

    def trc20_xfers_for_wallet(self, contract_addr: str, wallet_addr: str, token_type: str = TRC20) -> List[Trc20Txn]:
        """Use the TRC20 endpoint to get transfers for a particular wallet/token combo."""
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
        """
        contract_url = f"{self.base_uri}contracts/{contract_addr}/transactions"
        params = Api.build_params(extra={'contract_address': contract_addr})
        response = Api.get_response(contract_url, params)
        return response

    def events_for_token(
            self,
            contract_addr: str,
            since: Optional[DateTime] = None,
            until: Optional[DateTime] = None
        ) -> None:
        """In docs: Get events by contract address and write to CSV. This is the way that works."""
        already_processed_txns = set()
        until = until or MAX_TIME

        # TODO: refactor to its own method
        def remove_already_processed_txns(txns: List[Trc20Txn]) -> List[Trc20Txn]:
            filtered_txns = []

            for txn in txns:
                if txn.transaction_id in already_processed_txns:
                    log.debug(f"Already processed {txn}")
                    continue

                filtered_txns.append(txn)
                already_processed_txns.add(txn.transaction_id)

            log.debug(f"  Removed {len(txns) - len(filtered_txns)} duplicate transactions...")
            return filtered_txns

        contract_url = f"{self.base_uri}contracts/{contract_addr}/events"
        params = Api.build_params(max_timestamp=datetime_to_ms(until), extra={'event_name': 'Transfer'})
        response = Api.get_response(contract_url, params)
        retrieved_txns = Trc20Txn.extract_from_events(response)

        # Write CSV
        output_csv_filename = csv_filename_for_address(contract_addr)
        log.info(f"Output CSV file: '{output_csv_filename}'...")
        write_rows(output_csv_filename, retrieved_txns)

        # This uses the "next_url" approach which fails after a while.
        while META in response and LINKS in response[META] and NEXT in response[META][LINKS]:
            next_url = response[META][LINKS][NEXT]
            log.debug(f"Retrieving next URL '{next_url}'...")
            response = Api.get_response(next_url)

            # Therefore when it fails we go back to filtering by timestamp.
            # TODO: I tried something involving the response[META][FINGERPRINT] but didn't help.
            if not response[SUCCESS]:
                log.info(f"Failed to retrieve next_url. Trying again after moving end timestamp of request...")
                log.debug(f"  Next URL: '{next_url}'")
                min_timestamp = min([tx.ms_from_epoch for tx in retrieved_txns])
                params[MAX_TIMESTAMP] = str(min_timestamp)
                log.debug(f"Setting {MAX_TIMESTAMP} to {params[MAX_TIMESTAMP]}")
                response = Api.get_response(contract_url, params)

            log.debug(response)
            retrieved_txns = remove_already_processed_txns(Trc20Txn.extract_from_events(response))

            if len(retrieved_txns) == 0:
                if MAX_TIMESTAMP in params:
                    log.warning(f"We seem to be stuck at {ms_to_datetime(params[MAX_TIMESTAMP])}.")
                    log.warning("Subtracting 1 second and trying again.")
                    params[MAX_TIMESTAMP] -= 1000
            else:
                write_rows(output_csv_filename, retrieved_txns)

    @staticmethod
    @retry(wait=wait_exponential(multiplier=1, min=4, max=60))
    def get_response(url: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        params = params or {}

        if MIN_TIMESTAMP in params and MAX_TIMESTAMP in params:
            msg = f"Requesting records from {ms_to_datetime(params[MIN_TIMESTAMP])} to {ms_to_datetime(params[MAX_TIMESTAMP])}."
            log.info(msg)

        log.debug(f"\nURL: {url}\nParams: {params}")
        response = requests.get(url, headers=JSON_HEADERS, params=params).json()
        log.debug(f"Response: {response}")
        return response

    @staticmethod
    def build_params(max_timestamp: Optional[float] = None, extra: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        params = {
            'only_confirmed': 'true',
            'limit': str(MAX_TRADES_PER_CALL),
            MIN_TIMESTAMP: str(TRON_LAUNCH_TIME_IN_EPOCH_MS),
            MAX_TIMESTAMP: str(max_timestamp or pendulum.now('UTC').timestamp() * 1000)
        }

        return {**params, **(extra or {})}
