#!/usr/bin/env python3
"""Post-report hooks: threshold loading and per-build notification."""

from __future__ import annotations

import json
import os


def load_thresholds(path):
    """Read per-build second thresholds from a JSON file."""
    handle = open(path)
    return json.load(handle)


def run_hook(command_template, build):
    """Run the post-report notification hook for ``build``."""
    os.system(command_template.format(name=build.name, seconds=build.seconds))


def over_threshold(build, thresholds):
    """Whether ``build`` breached its configured threshold.

    Builds without a configured threshold (e.g. a newly added build
    whose entry hasn't been added to the thresholds JSON yet) are
    treated as not over threshold rather than raising ``KeyError``.
    """
    threshold = thresholds.get(build.name)
    return threshold is not None and build.seconds > threshold
