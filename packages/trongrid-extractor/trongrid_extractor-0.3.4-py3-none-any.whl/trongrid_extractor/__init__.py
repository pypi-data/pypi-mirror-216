from trongrid_extractor.api import Api
from trongrid_extractor.helpers.argument_parser import parse_args
from trongrid_extractor.helpers.time_helpers import MAX_TIME, TRON_LAUNCH_TIME, str_to_timestamp


def extract_tron_transactions():
    args = parse_args()

    Api().events_for_token(
        args.token_address,
        since=args.since,
        until=args.until or MAX_TIME,
        resume_csv=args.resume_csv,
        output_dir=args.output_dir
    )
