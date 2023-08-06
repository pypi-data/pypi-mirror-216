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
from typing import Any, Dict, List, Optional, Tuple

import pendulum

from rich.console import Console
from trongrid_extractor.config import log
from trongrid_extractor.helpers.address_helpers import hex_to_tron
from trongrid_extractor.helpers.string_constants import DATA, RESULT

# Some tokens use src/dst/wad instead of from/to/value
SRC_DST_WAD = ('src', 'dst', 'wad')
FROM_TO_VALUE = ('from', 'to', 'value')


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
        # Type coercion
        self.amount = float(self.amount)
        self.event_index = int(self.event_index)
        self.ms_from_epoch = float(self.ms_from_epoch)
        self.block_number = int(self.block_number) if self.block_number else None
        # Computed fields
        self.seconds_from_epoch = self.ms_from_epoch / 1000.0
        self.datetime = pendulum.from_timestamp(self.seconds_from_epoch, pendulum.tz.UTC)
        self.unique_id = f"{self.transaction_id}/{self.event_index}"

    @classmethod
    def extract_from_events(cls, events: dict[str, Any]) -> List['Trc20Txn']:
        """Extract transfers from events."""
        if DATA not in events:
            raise ValueError(f"No 'data' property found in {events}")
        elif len(events[DATA]) == 0:
            return []

        # Check the 'result_type' to see if it's from/to/value or src/dst/wad keys.
        txn_from, txn_to, txn_amount = cls.identify_txn_keys(events[DATA][0]['result_type'])

        try:
            txns = [
                cls(
                        token_address=row['contract_address'],
                        from_address=hex_to_tron(row[RESULT][txn_from]),
                        to_address=hex_to_tron(row[RESULT][txn_to]),
                        amount=row[RESULT][txn_amount],
                        ms_from_epoch=float(row['block_timestamp']),
                        block_number=int(row['block_number']),
                        transaction_id=row['transaction_id'],
                        event_index=row['event_index']
                    )
                for row in events['data']
            ]
        except Exception:
            Console().print_exception(show_locals=True)

        log.debug(f"Extracted {len(txns)} txns from the response...")
        return txns

    @classmethod
    def extract_from_wallet_transactions(cls, response: dict[str, Any]) -> List['Trc20Txn']:
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

    @staticmethod
    def identify_txn_keys(result_type: Dict[str, str]) -> Tuple[str, str, str]:
        if sorted(result_type.keys()) == sorted(SRC_DST_WAD):
            return SRC_DST_WAD
        else:
            return FROM_TO_VALUE

    def __str__(self) -> str:
        msg = f"Token: {self.token_address[0:10]}..., From: {self.from_address[0:10]}..."
        msg += f", To: {self.to_address[0:10]}..., ID: {self.transaction_id[0:10]}.../{self.event_index}"
        msg += f", Amount: {self.amount} (at {self.datetime})"
        return msg
