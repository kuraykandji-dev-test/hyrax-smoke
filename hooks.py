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

    Substitution uses plain literal ``str.replace`` (not ``str.format``)
    on each token, so a template containing stray ``{`` / ``}`` characters
    unrelated to the ``{name}``/``{seconds}`` placeholders (e.g. an
    embedded JSON snippet) is passed through unchanged instead of raising
    ``KeyError``/``ValueError``. It also means ``build.name`` can't trigger
    ``str.format`` attribute/index lookups (e.g. ``{0.__class__}``).
    """
    argv = [
        token.replace("{name}", str(build.name)).replace(
            "{seconds}", str(build.seconds)
        )
        for token in shlex.split(command_template)
    ]
    subprocess.run(argv, shell=False, check=False)


def over_threshold(build, thresholds):
    """Whether ``build`` breached its configured threshold.

    Builds without a configured threshold (e.g. a newly added build
    whose entry hasn't been added to the thresholds JSON yet) are
    treated as not over threshold rather than raising ``KeyError``.
    """
    threshold = thresholds.get(build.name)
    return threshold is not None and build.seconds > threshold
