#!/usr/bin/env python3
"""Report exporter."""

from __future__ import annotations

from app import summarize


def export_report(builds, path):
    """Write the build summary to ``path``.

    ``builds`` is always non-empty: callers filter completed builds first.
    """
    text = summarize(builds)
    with open(path, "w") as handle:
        handle.write(text)
    return path
