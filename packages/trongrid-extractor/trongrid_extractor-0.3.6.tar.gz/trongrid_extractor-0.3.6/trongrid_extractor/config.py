import logging
from os import environ

from rich.logging import RichHandler

LOG_LEVEL = environ.get('LOG_LEVEL', 'INFO')


log = logging.getLogger('trongrid_extractor')
log.setLevel(LOG_LEVEL)
rich_stream_handler = RichHandler(rich_tracebacks=True)
rich_stream_handler.setLevel(LOG_LEVEL)
log.addHandler(rich_stream_handler)
