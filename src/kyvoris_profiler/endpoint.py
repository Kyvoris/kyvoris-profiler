"""Endpoint profiling helpers."""

from __future__ import annotations

from collections.abc import Mapping
from urllib.request import Request, urlopen

from kyvoris_profiler.benchmark import profile_callable
from kyvoris_profiler.metrics import ProfileSummary


def profile_http_endpoint(
    url: str,
    iterations: int = 10,
    warmup: int = 0,
    method: str = "GET",
    headers: Mapping[str, str] | None = None,
    data: bytes | None = None,
    timeout: float = 10.0,
    collect_memory: bool = False,
    collect_cpu: bool = False,
    continue_on_error: bool = False,
) -> ProfileSummary:
    """Profile a simple HTTP endpoint request."""

    def request_once() -> bytes:
        request = Request(
            url,
            data=data,
            headers=dict(headers or {}),
            method=method,
        )
        with urlopen(request, timeout=timeout) as response:
            return response.read()

    return profile_callable(
        request_once,
        iterations=iterations,
        warmup=warmup,
        collect_memory=collect_memory,
        collect_cpu=collect_cpu,
        continue_on_error=continue_on_error,
    )
