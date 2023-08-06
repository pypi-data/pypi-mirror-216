"""
Class to track with transactions we've already seen and the CSV to write to.
"""
import csv
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pendulum import DateTime

from trongrid_extractor.config import log
from trongrid_extractor.trc20_txn import Trc20Txn
from trongrid_extractor.helpers.time_helpers import ms_to_datetime


class ProgressTracker:
    def __init__(self, output_csv_path: Path, resume_from_csv: bool = False) -> None:
        self.output_csv_path = output_csv_path
        self.already_processed_uniq_ids = set()
        self.earliest_timestamp_seen_ms = None

        # Resume from CSV if requested
        if resume_from_csv:
            self._load_csv_progress()
            log.info(f"Resuming CSV '{self.output_csv_path}' from {self.earliest_timestamp_seen()}...")
        elif self.output_csv_path.exists():
            log.warning(f"File '{self.output_csv_path}' already exists, deleting...")
            os.remove(self.output_csv_path)

    def process_response(self, response: Dict[str, Any]) -> List[Trc20Txn]:
        retrieved_txns = Trc20Txn.extract_from_events(response)
        return self.remove_already_processed_txns(retrieved_txns)

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

            if self.earliest_timestamp_seen_ms is None or txn.ms_from_epoch <= self.earliest_timestamp_seen_ms:
                self.earliest_timestamp_seen_ms = txn.ms_from_epoch

            filtered_txns.append(txn)
            self.already_processed_uniq_ids.add(txn.unique_id)

        removed_txn_count = len(txns) - len(filtered_txns)

        if removed_txn_count > 0:
            log.info(f"  Removed {removed_txn_count} duplicate transactions...")

        return filtered_txns

    def earliest_timestamp_seen(self) -> Optional[DateTime]:
        """Convert the milliseconds to a DateTime."""
        if self.earliest_timestamp_seen_ms:
            return ms_to_datetime(self.earliest_timestamp_seen_ms)

    def _load_csv_progress(self) -> None:
        """Read a CSV and consider each row as having already been processed."""
        if not self.output_csv_path.exists():
            raise ValueError(f"Can't resume from CSV because '{csv_path}' doesn't exist!")

        row_count = 0

        with open(self.output_csv_path, mode='r') as csvfile:
            for row in csv.DictReader(csvfile, delimiter=','):
                self.remove_already_processed_txns([Trc20Txn(**row)])
                row_count += 1

        log.info(f"Processed {row_count} rows in '{self.output_csv_path}',")
        log.info(f"   Resuming from min timestamp {self.earliest_timestamp_seen()}.")
