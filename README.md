# buildstats

A small command-line helper for summarizing CI build durations.

## Usage

```
python app.py lint=12.5 test=30.1 package=8.0
```

Prints the build count, the total and average wall-clock time, the median
build duration, the p95 percentile, and whichever build took the longest.
