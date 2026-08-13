#!/usr/bin/env python3
"""Lookup helpers for named builds."""

from __future__ import annotations


def find_build(builds, name):
    """Return the build called ``name``, or ``None`` when there is no match."""
    for build in builds:
        if build.name == name:
            return build
    return None


def describe_build(builds, name):
    """One-line description of a named build."""
    build = find_build(builds, name)
    if build is None:
        return f"{name}: no such build"
    return f"{build.name} took {build.seconds:.1f}s"


def describe_all(builds, names):
    """Describe each requested build, one per line."""
    return "\n".join(describe_build(builds, name) for name in names)
