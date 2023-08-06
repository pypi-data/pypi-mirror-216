from argparse import ArgumentParser, Namespace

from trongrid_extractor.config import log
from trongrid_extractor.helpers.time_helpers import str_to_timestamp

parser = ArgumentParser(
    description='Pull transactions for a given token address'
)

parser.add_argument('token_address', metavar='TOKEN_ADDRESS')

parser.add_argument('-s', '--since',
                    help='Get transactions up to and including this time (ISO 8601 Format)',
                    metavar='DATETIME')

parser.add_argument('-u', '--until',
                    help='Get transactions starting from this time (ISO 8601 Format)',
                    metavar='DATETIME')


def parse_args() -> Namespace:
    args = parser.parse_args()

    if args.since:
        since = str_to_timestamp(args.since)
        log.info(f"Requested records since '{args.since}' which parsed to {since}.")
        args.since = since

    if args.until:
        until = str_to_timestamp(args.until)
        log.info(f"Requested records until '{args.until}' which parsed to {until}.")
        args.until = until

    return args
