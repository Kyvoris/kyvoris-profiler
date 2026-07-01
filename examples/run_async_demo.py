"""Run a small async Kyvoris Profiler benchmark demo."""

from __future__ import annotations

import asyncio

from kyvoris_profiler import format_text_report, profile_async_callable


async def simulated_async_inference() -> str:
    """Stand in for a remote model endpoint or async inference call."""
    await asyncio.sleep(0.005)
    return "ok"


async def main() -> None:
    result = await profile_async_callable(
        simulated_async_inference,
        iterations=5,
        warmup=1,
        collect_cpu=True,
        collect_memory=True,
    )
    print(format_text_report(result, title="Async Inference Benchmark"))


if __name__ == "__main__":
    asyncio.run(main())
