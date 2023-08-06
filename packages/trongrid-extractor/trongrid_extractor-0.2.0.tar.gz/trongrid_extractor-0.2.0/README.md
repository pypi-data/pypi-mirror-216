# Usage
## Command Line
`--since` and `--until` arguments should be specified in ISO8601 time format:
```sh
extract_tron_transactions  --until 2023-06-26T16:07:39+00:00 TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
```

Set `LOG_LEVEL=DEBUG` to get debug logging.

## As Package
```python
from trongrid_extractor.api import Api

Api().events_for_token('Tf2939nbd23kmdo')
```

`events_for_token()` hits the `contracts/[CONTRACT_ADDRESS]/events` endpoint and can pull all transfers for a given contract by filtering for `event_name=Transfer`. Other endpoints like `contracts/[CONTRACT_ADDRESS]/transactions` don't seem to really work.

# Trongrid Documentation, Quirks, Etc.
When you make an API request to TronGrid they return you a page of results. If there are more than the page size (200 here) then the response includes a `next` key that has a URL you can hit to get the next page. Sounds convenient, right? Except it doesn't work. After 5 pages TronGrid will tell you your timespan is too big and please try again. This package is written to go around this "quirk" by backing up the `max_timestamp` parameter when it can't page any more.

* [Trongrid API documentation](https://developers.tron.network/v4.0/reference/note)


# Contributing
This project was developed with `poetry` and as such is probably easier to work with using `poetry` to manage dependencies in the dev environment. Install with:
```
poetry install --with=dev
```
## Running Tests
```
pytest
```

## Publishing to PyPi
1. `poetry config repositories.chain_argos_pypi https://upload.pypi.org/legacy/`
2. `poetry config pypi-token.chain_argos_pypi [API_TOKEN]`
3. `poetry publish --build --repository chain_argos_pypi`
