# describe\_build crashes with None on unknown --highlight

**Tool:** `review`
**Severity:** high
**Category:** review
**Location:** `report.py:25`

## What's wrong

`describe_build` calls `find_build(builds, name)` which returns `None` when no build matches `name`, then immediately does `build.name` / `build.seconds` on the result without a None check.

Since `--highlight` is a free-form CLI argument and `main` only ever registers builds named `lint` and `test`, running `python report.py --filename build-report.txt --branch ci-reports --highlight typo` raises `AttributeError: 'NoneType' object has no attribute 'name'` and the exporter crashes before writing or archiving the report.

Guard against the missing case, e.g.:
```python
def describe_build(builds, name):
    build = find_build(builds, name)
    if build is None:
        return f"{name}: no such build"
    return f"{build.name} took {build.seconds:.1f}s"
```
