#!/usr/bin/env python3
"""Report path and branch naming."""

from __future__ import annotations

import re

_SAFE = re.compile(r"[^A-Za-z0-9_.-]")


def report_path(name):
    """Filesystem path for the named report."""
    return "reports/%s.txt" % _SAFE.sub("_", name)


def report_branch(name):
    """Branch that carries the named report."""
    return "reports/%s" % _SAFE.sub("_", name)
