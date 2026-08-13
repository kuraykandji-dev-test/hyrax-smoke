#!/usr/bin/env python3
"""Remote report upload configuration."""

from __future__ import annotations

import subprocess


def upload_report(path, host, user):
    """Copy the report to the reporting host over scp."""
    subprocess.run(f"scp {path} {user}@{host}:/var/reports/", shell=True, check=True)
