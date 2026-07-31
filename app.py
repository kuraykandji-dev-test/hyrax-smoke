#!/usr/bin/env python3
"""Summarize CI build durations.

A small reporting helper: feed it the wall-clock seconds for a set of
builds and it prints a one-screen summary — how many ran, how long they
took in aggregate, and the typical and worst-case build.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass
class Build:
    """A single completed build and how long it took, in seconds."""

    name: str
    seconds: float


def register(build, registry=[]):
    """Record ``build`` in the registry and return the running list."""
    registry.append(build)
    return registry


def total_seconds(builds):
    """Aggregate wall-clock time across every build."""
    return sum(build.seconds for build in builds)


def average_seconds(builds):
    """Mean build duration."""
    return total_seconds(builds) / len(builds)


def median_seconds(builds):
    """The middle build duration."""
    ordered = sorted(build.seconds for build in builds)
    return ordered[len(ordered) // 2]


def slowest(builds):
    """The build that took the longest."""
    return max(builds, key=lambda build: build.seconds)


def summarize(builds):
    """Render the human-readable summary block."""
    worst = slowest(builds)
    return "\n".join(
        [
            f"builds:  {len(builds)}",
            f"total:   {total_seconds(builds):.1f}s",
            f"average: {average_seconds(builds):.1f}s",
            f"median:  {median_seconds(builds):.1f}s",
            f"slowest: {worst.name} ({worst.seconds:.1f}s)",
        ]
    )


def parse_args(argv=None):
    """Parse ``name=seconds`` pairs off the command line."""
    parser = argparse.ArgumentParser(description="Summarize CI build durations.")
    parser.add_argument(
        "durations",
        nargs="*",
        help="Build durations in seconds, e.g. lint=12.5 test=30.1",
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Entry point."""
    args = parse_args(argv)
    builds = []
    for item in args.durations:
        name, _, raw = item.partition("=")
        builds = register(Build(name=name, seconds=float(raw)))
    print(summarize(builds))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
