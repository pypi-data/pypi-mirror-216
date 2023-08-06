import re
from typing import Union

import pendulum
from pendulum import DateTime

from trongrid_extractor.config import log

# 2017-01-01, though Tron was really prolly launched in 2018
TRON_LAUNCH_TIME = pendulum.datetime(2017, 1, 1, tz='UTC')
TRON_LAUNCH_TIME_IN_EPOCH_MS = TRON_LAUNCH_TIME.timestamp() * 1000
MAX_TIME = DateTime.now().add(years=2)


def ms_to_datetime(ms: Union[float, int, str]) -> DateTime:
    ms = float(ms)

    try:
        datetime = pendulum.from_timestamp(float(ms))
    except ValueError as e:
        if not re.match('year \\d+ is out of range', str(e)):
            raise e

        datetime = pendulum.from_timestamp(float(ms) / 1000.0)

    log.debug(f"Extracted time {datetime} from {ms}")
    return datetime


def datetime_to_ms(timestamp: Union[str, DateTime]) -> float:
    if isinstance(timestamp, str):
        timestamp = DateTime.fromisoformat(timestamp)

    is_valid_timestamp(timestamp)
    return timestamp.timestamp() * 1000


def str_to_timestamp(iso_timestamp_string: str) -> DateTime:
    timestamp = DateTime.fromisoformat(iso_timestamp_string)
    is_valid_timestamp(timestamp)
    return timestamp


def is_valid_timestamp(timestamp: DateTime) -> bool:
    if timestamp < TRON_LAUNCH_TIME:
        raise ValueError(f"{timestamp} is before {TRON_LAUNCH_TIME}!")
    elif timestamp > MAX_TIME:
        raise ValueError(f"{timestamp} is too far in the future!")

    return True
