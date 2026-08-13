# load\_thresholds leaks file handle by not closing it

**Tool:** `review`
**Severity:** medium
**Category:** review
**Location:** `hooks.py:10`

## What's wrong

`load_thresholds` opens `path` with `open(path)` but never closes the handle via a `with` block or explicit `close()`.

Under CPython the handle is eventually reclaimed by garbage collection, but repeated calls (e.g. reloading thresholds per build or per report) accumulate open file descriptors until GC runs, which can exhaust the process's FD limit under sustained use.

```python
def load_thresholds(path):
    with open(path) as handle:
        return json.load(handle)
```
