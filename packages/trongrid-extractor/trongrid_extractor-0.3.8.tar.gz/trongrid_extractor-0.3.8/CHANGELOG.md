# NEXT RELEASE

### 0.3.8
* Fix buggy handling of false completes

### 0.3.7
* Delete output CSV if it already exists
* Fix bug with resuming from CSV with out of order rows
* Only do a rescue when it is impossible to load next page
* Add a bunch of tokens (`HT`, `SUN`, `JST`, `BTT`, etc.)

### 0.3.6
* Simplify inner logic and retries etc.

### 0.3.5
* Avoid endless loop on `is_false_complete_response()`
* Refactor `response.pretty_print()`
* Don't allow walkbacks to walk back past the start of the period

### 0.3.4
* `Response` object refactor
* Smarter logging
* Strip `:` and `/` from CSV filenames

### 0.3.3
* Add `filename_suffix` arg

### 0.3.2
* Tidbits

### 0.3.1
* Better 0 txn response handling
* `compile_csvs.py` script

# 0.3.0
* `--resume-csv` option
* Use floats instead of strings for timestamps. Add `_is_paging_complete()` method
* Handle src/dst/wad txns

# 0.2.0
* `ProgressTracker` class
* `event_number` column
* Accept symbols like `USDT` as argument instead of just addresses
* Accept `--since`, `--until`, and `--output-dir` options on the command line

# 0.1.0
* Initial release.
