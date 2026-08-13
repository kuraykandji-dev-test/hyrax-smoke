# KeyError when build.name missing from thresholds

**Tool:** `review`
**Severity:** high
**Category:** review
**Location:** `hooks.py:22`

## What's wrong

`over_threshold` does `thresholds[build.name]` with no fallback or existence check. If a build's name isn't present in the thresholds JSON loaded by `load_thresholds` (e.g. a newly added build without a configured threshold), this raises `KeyError` and crashes the caller instead of skipping or applying a default.

This will happen the first time a new build is reported before its threshold entry is added to the JSON config, causing the whole post-report hook path to blow up.

Use `.get()` with an explicit policy, e.g.:
```python
def over_threshold(build, thresholds):
    threshold = thresholds.get(build.name)
    return threshold is not None and build.seconds > threshold
```
