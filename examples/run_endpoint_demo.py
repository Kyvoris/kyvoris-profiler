"""Benchmark a simple HTTP endpoint."""

from __future__ import annotations

from kyvoris_profiler import format_text_report, profile_http_endpoint


URL = "https://example.com"


if __name__ == "__main__":
    result = profile_http_endpoint(
        URL,
        iterations=3,
        warmup=1,
        collect_cpu=True,
        collect_memory=True,
    )
    print(format_text_report(result, title="HTTP Endpoint Benchmark"))
    print()
    print(f"URL: {URL}")
