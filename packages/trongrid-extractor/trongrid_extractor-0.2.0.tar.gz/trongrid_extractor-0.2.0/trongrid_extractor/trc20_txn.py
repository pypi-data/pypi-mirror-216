"""
Dataclass representing one TRC20 token transfer.

Example response from Trongrid:
{
    'transaction_id': 'ceb20398469dbf7c6b07f0ce3ed760418af02afd4643dbe6962177fa03f81266',
    'token_info': {
        'symbol': 'USDC',
        'address': 'TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8',
        'decimals': 6,
        'name': 'USD Coin'
    },
    'block_timestamp': 1686038304000,
    'from': 'TYE218dMfzo2TH348AbKyHD2G8PjGo7ESS',
    'to': 'TL6752QaiLmEAidRCXkL85CNiwSG4asy9M',
    'type': 'Transfer',
    'value': '4900000'
}
"""

from dataclasses import dataclass
from typing import Any, List, Optional

import pendulum

from trongrid_extractor.config import log
from trongrid_extractor.helpers.address_helpers import hex_to_tron


@dataclass(kw_only=True)
class Trc20Txn:
    token_address: str
    from_address: str
    to_address: str
    amount: float
    transaction_id: str
    event_index: int
    ms_from_epoch: float
    block_number: Optional[int] = None

    def __post_init__(self):
        self.seconds_from_epoch = self.ms_from_epoch / 1000.0
        self.datetime = pendulum.from_timestamp(self.seconds_from_epoch, pendulum.tz.UTC)
        self.unique_id = f"{self.transaction_id}/{self.event_index}"

    @classmethod
    def extract_from_response(cls, response: dict[str, Any]) -> List['Trc20Txn']:
        """Extract a list of txns from the Trongrid response object."""
        txns = [
            cls(
                token_address=row['token_info']['address'],
                from_address=row['from'],
                to_address=row['to'],
                amount=float(row['value']) / 10**row['token_info']['decimals'],
                ms_from_epoch=float(row['block_timestamp']),
                transaction_id=row['transaction_id'],
                event_index=row['event_index']
            )
            for row in response['data']
        ]

        log.debug(f"Extracted {len(txns)} txns from the response...")
        return txns

    @classmethod
    def extract_from_events(cls, events: dict[str, Any]) -> List['Trc20Txn']:
        """Extract transfers from events."""
        txns = [
            cls(
                token_address=row['contract_address'],
                from_address=hex_to_tron(row['result']['from']),
                to_address=hex_to_tron(row['result']['to']),
                amount=row['result']['value'],
                ms_from_epoch=float(row['block_timestamp']),
                block_number=int(row['block_number']),
                transaction_id=row['transaction_id'],
                event_index=row['event_index']
            )
            for row in events['data']
        ]

        log.debug(f"Extracted {len(txns)} txns from the response...")
        return txns

    def __str__(self) -> str:
        msg = f"Token: {self.token_address[0:10]}..., From: {self.from_address[0:10]}..."
        msg += f", To: {self.to_address[0:10]}..., ID: {self.transaction_id[0:10]}.../{self.event_index}"
        msg += f", Amount: {self.amount} (at {self.datetime})"
        return msg
