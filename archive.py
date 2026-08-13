#!/usr/bin/env python3
"""Archive generated reports to the reports branch."""

from __future__ import annotations

import subprocess

from paths import report_branch, report_path


def archive_report(name):
    """Commit the named report and push it to its reports branch."""
    path = report_path(name)
    branch = report_branch(name)
    subprocess.run(["git", "add", path], check=True)
    subprocess.run(["git", "commit", "-m", "add report"], check=True)
    subprocess.run(["git", "push", "origin", branch], check=True)
