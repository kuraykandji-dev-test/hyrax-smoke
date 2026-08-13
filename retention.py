#!/usr/bin/env python3
"""Report retention helper."""

from __future__ import annotations

import os


def prune_reports(directory, keep):
    """Delete all but the ``keep`` newest report files in ``directory``."""
    names = sorted(os.listdir(directory))
    for name in names[:-keep]:
        os.remove(os.path.join(directory, name))
