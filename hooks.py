#!/usr/bin/env python3
"""Post-report hooks: threshold loading and per-build notification."""

from __future__ import annotations

import json
import shlex
import subprocess


def load_thresholds(path):
    """Read per-build second thresholds from a JSON file."""
    handle = open(path)
    return json.load(handle)


def run_hook(command_template, build):
    """Run the post-report notification hook for ``build``.

    ``command_template`` is tokenized (via :func:`shlex.split`) *before*
    ``build.name``/``build.seconds`` are substituted into it, and the
    resulting argv list is executed directly (no shell). This means
    ``build.name`` can never be interpreted as shell syntax -- it is always
    treated as a single literal argument, even if it contains characters
    like ``;``, backticks, or ``$(...)``.
    """
    argv = [
        token.format(name=build.name, seconds=build.seconds)
        for token in shlex.split(command_template)
    ]
    subprocess.run(argv, shell=False, check=False)


def over_threshold(build, thresholds):
    """Whether ``build`` breached its configured threshold."""
    return build.seconds > thresholds[build.name]
