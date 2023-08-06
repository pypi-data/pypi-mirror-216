from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import exit

from trongrid_extractor.config import log
from trongrid_extractor.helpers.address_helpers import is_contract_address, address_of_symbol
from trongrid_extractor.helpers.time_helpers import str_to_timestamp

parser = ArgumentParser(
    description='Pull transactions for a given token address'
)

parser.add_argument('token_address',
                    help="Token address or a string like 'USDT' (at least for a limited number of known symbols)",
                    metavar='TOKEN_ADDRESS_OR_SYMBOL')

parser.add_argument('-s', '--since',
                    help='Get transactions up to and including this time (ISO 8601 Format)',
                    metavar='DATETIME')

parser.add_argument('-u', '--until',
                    help='Get transactions starting from this time (ISO 8601 Format)',
                    metavar='DATETIME')

# TODO: this should accept an S3 URI.
parser.add_argument('-o', '--output-dir',
                    help='Write transaction CSVs to this location.',
                    metavar='OUTPUT_DIR')

parser.add_argument('-r', '--resume-csv',
                    help='If a file is found in OUTPUT_DIR for this token extraction will resume and rows will be appended',
                    metavar='CSV_FILE')


def parse_args() -> Namespace:
    args = parser.parse_args()
    args.output_dir = Path(args.output_dir or '')
    args.resume_csv = Path(args.resume_csv) if args.resume_csv else None

    if not is_contract_address(args.token_address):
        address = address_of_symbol(args.token_address)

        if address is None:
            log.error(f"Unknown symbol: '{args.token_address}'")
            exit(1)
        else:
            log.info(f"Using '{args.token_address}' address '{address}'")
            args.token_address = address

    if args.since:
        since = str_to_timestamp(args.since)
        log.info(f"Requested records since '{args.since}' which parsed to {since}.")
        args.since = since

    if args.until:
        until = str_to_timestamp(args.until)
        log.info(f"Requested records until '{args.until}' which parsed to {until}.")
        args.until = until

    return args
