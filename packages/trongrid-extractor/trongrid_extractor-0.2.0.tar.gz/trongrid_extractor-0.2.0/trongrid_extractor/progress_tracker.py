"""
Class to track with transactions we've already seen.
"""
from typing import List, Optional

from trongrid_extractor.config import log
from trongrid_extractor.trc20_txn import Trc20Txn


class ProgressTracker:
    def __init__(self, txns: List[Trc20Txn]) -> None:
        self.already_processed_uniq_ids = set([txn.unique_id for txn in txns])
        self.earliest_block_timestamp_seen: Optional[float] = min([txn.ms_from_epoch for txn in txns])

        if len(txns) != len(self.already_processed_uniq_ids):
            log.error(txns)
            raise ValueError(f"Should be {len(txns)} unique IDs but only {len(self.already_processed_uniq_ids)}!")

    def remove_already_processed_txns(self, txns: List[Trc20Txn]) -> List[Trc20Txn]:
        """
        Track already seen unique_ids ("transaction_id/event_index") and the earliest block_timestamp
        encountered. Remove any transactions w/IDs return the resulting list.
        """
        filtered_txns = []

        for txn in txns:
            if txn.unique_id in self.already_processed_uniq_ids:
                log.debug(f"Already processed: {txn}")
                continue

            if self.earliest_block_timestamp_seen is None or txn.block_number <= self.earliest_block_timestamp_seen:
                self.earliest_block_timestamp_seen = txn.ms_from_epoch

            filtered_txns.append(txn)
            self.already_processed_uniq_ids.add(txn.unique_id)

        removed_txn_count = len(txns) - len(filtered_txns)

        if removed_txn_count > 0:
            log.info(f"  Removed {removed_txn_count} duplicate transactions...")

        return filtered_txns
