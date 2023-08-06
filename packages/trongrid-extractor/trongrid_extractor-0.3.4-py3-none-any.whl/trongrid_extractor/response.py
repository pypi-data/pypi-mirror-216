"""
Wrapper for trongrid's response JSON data.
"""
import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Union

import requests
from tenacity import after_log, retry, stop_after_attempt, wait_exponential

from trongrid_extractor.config import log
from trongrid_extractor.helpers.csv_helper import *
from trongrid_extractor.helpers.string_constants import *
from trongrid_extractor.helpers.time_helpers import *

JSON_HEADERS = {'Accept': 'application/json'}


@dataclass
class Response:
    response: Dict[str, Any]
    params: Dict[str, Any]

    @classmethod
    @retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(7), after=after_log(log, logging.DEBUG))
    def get_response(cls, url: str, params: Optional[Dict[str, Union[str, int, float]]] = None) -> 'Response':
        """Hit the endpoint and extract JSON data."""
        params = params or {}

        # Min/Max timestamps are INCLUSIVE.
        if MIN_TIMESTAMP in params and MAX_TIMESTAMP in params:
            msg = f"Requesting records from {ms_to_datetime(params[MIN_TIMESTAMP])} to {ms_to_datetime(params[MAX_TIMESTAMP])}."
            log.info(msg)

        log.debug(f"\nURL: {url}\nParams: {params}")
        response = requests.get(url, headers=JSON_HEADERS, params=params).json()
        log.debug(f"Response: {response}")
        return cls(response, deepcopy(params))

    def is_continuable_response(self) -> bool:
        return self.next_url() is not None

    def is_paging_complete(self) -> bool:
        page_size = self.page_size() or 0
        return self.was_successful() and page_size > 0 and self.next_url() is None

    def is_false_complete_response(self) -> bool:
        """Sometimes for no reason TronGrid just returns 0 rows to a query that would otherwise return rows."""
        return self.was_successful() and self.page_size() == 0 and self.next_url() is None

    def was_successful(self) -> bool:
        if SUCCESS not in self.response:
            log.warning(f"No '{SUCCESS}' key found in response!\n{self.response}")
            return False

        success = self.response[SUCCESS]

        if not isinstance(success, bool):
            raise ValueError(f"{success} is of type {type(success)} instead of bool!")

        return success

    def next_url(self) -> Optional[str]:
        if META in self.response and LINKS in self.response[META] and NEXT in self.response[META][LINKS]:
            return self.response[META][LINKS][NEXT]

    def page_size(self) -> Optional[int]:
        if META in self.response and PAGE_SIZE in self.response[META]:
            return self.response[META][PAGE_SIZE]

    def without_data(self) -> Dict[str, Any]:
        """Return the response JSON just without the 'data' field."""
        abbreviated_response = deepcopy(self.response)
        abbreviated_response['data'] = f"[Skipping {len(self.response['data'])} elements of 'data' array]"
        return abbreviated_response
