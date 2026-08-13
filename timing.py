#!/usr/bin/env python3
"""Build timing windows."""

from __future__ import annotations


def slowest_window(builds, size):
    """Return the ``size`` consecutive builds with the greatest total time."""
    best_start = 0
    best_total = 0.0
    for start in range(len(builds) - size):
        total = sum(build.seconds for build in builds[start : start + size])
        if total > best_total:
            best_total = total
            best_start = start
    return builds[best_start : best_start + size]
