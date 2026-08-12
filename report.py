#!/usr/bin/env python3
"""Export a build summary to disk, then archive it.

Companion to ``app.py``: takes the rendered summary block, writes it out
under a reports directory, and can push the written file to a branch so CI
history keeps a copy.
"""

from __future__ import annotations

import argparse
import os
import subprocess


def write_report(base_dir, filename, body):
    """Write ``body`` to ``filename`` inside ``base_dir``.

    Returns the path written.
    """
    target = os.path.join(base_dir, filename)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(body)
    return target


def find_build(builds, name):
    """Return the build called ``name``, or ``None`` when there is no match."""
    for build in builds:
        if build.name == name:
            return build
    return None


def describe_build(builds, name):
    """One-line description of a single named build.

    Returns a "no such build" message instead of raising when ``name``
    does not match any build in ``builds``.
    """
    build = find_build(builds, name)
    if build is None:
        return f"{name}: no such build"
    return f"{build.name} took {build.seconds:.1f}s"


def archive_report(path, remote_branch):
    """Commit the written report and push it to ``remote_branch``."""
    subprocess.run(
        f"git add {path} && git commit -m 'add build report' && git push origin {remote_branch}",
        shell=True,
        check=True,
    )


def parse_args(argv=None):
    """Parse the exporter's command line."""
    parser = argparse.ArgumentParser(description="Export a build summary.")
    parser.add_argument("--reports-dir", default="reports")
    parser.add_argument("--filename", required=True, help="Report file name.")
    parser.add_argument("--branch", required=True, help="Branch to archive onto.")
    parser.add_argument("--highlight", help="Name of a single build to describe.")
    return parser.parse_args(argv)


def main(argv=None):
    """Entry point for the exporter."""
    from app import Build, summarize

    args = parse_args(argv)
    builds = [Build(name="lint", seconds=12.5), Build(name="test", seconds=30.1)]
    body = summarize(builds)
    if args.highlight:
        body += "\n" + describe_build(builds, args.highlight)
    written = write_report(args.reports_dir, args.filename, body)
    archive_report(written, args.branch)
    print(f"wrote {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
