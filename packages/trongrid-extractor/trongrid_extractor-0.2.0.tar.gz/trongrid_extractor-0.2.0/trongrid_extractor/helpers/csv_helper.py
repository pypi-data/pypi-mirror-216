import csv
from dataclasses import dataclass, field, asdict, fields
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union

from trongrid_extractor.config import log
from trongrid_extractor.helpers.address_helpers import symbol_for_address
from trongrid_extractor.trc20_txn import Trc20Txn


def write_rows(file_path: Union[str, Path], rows: List[Trc20Txn]) -> None:
    if len(rows) == 0:
        log.warning(f"No rows to write!")
        return

    log.info(f"Writing {len(rows)} rows to '{file_path}'...")
    _fields = [fld.name for fld in fields(type(rows[0]))]

    if Path(file_path).exists():
        file_mode = 'a'
    else:
        file_mode = 'w'

    with open(file_path, file_mode) as f:
        csv_writer = csv.DictWriter(f, _fields)

        if file_mode == 'w':
            csv_writer.writeheader()

        csv_writer.writerows([asdict(row) for row in rows])


def output_csv_path(address: str, dir: Optional[Path] = None) -> Path:
    """Build a filename that contains the address and (if available) the symbol."""
    dir = dir or Path('')
    filename = 'events_'
    symbol = symbol_for_address(address)

    if symbol:
        filename += f"{symbol}_"

    filename += f"written_{datetime.now().strftime('%Y-%m-%dT%H.%M.%S')}.csv"
    return dir.joinpath(filename)


# def append_rows(file_path: str, rows: List[Trc20Txn]) -> None:
#     _fields = [fld.name for fld in fields(type(rows[0]))]

#     with open(file_path, 'a') as f:
#         csv_writer = csv.DictWriter(f, _fields)
#         csv_writer.writerows([asdict(row) for row in rows])
