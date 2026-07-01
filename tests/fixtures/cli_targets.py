"""Callable targets used by CLI tests."""

from __future__ import annotations


CALL_COUNT = 0


def target() -> str:
    """Small no-argument callable for CLI smoke tests."""
    global CALL_COUNT
    CALL_COUNT += 1
    return "ok"
