import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kyvoris_profiler import LatencySummary, benchmark_callable


class BenchmarkCallableTests(unittest.TestCase):
    def test_benchmark_callable_reports_summary_stats(self) -> None:
        def target() -> None:
            time.sleep(0.001)

        stats = benchmark_callable(target, iterations=5)

        self.assertIsInstance(stats, LatencySummary)
        self.assertEqual(stats.iterations, 5)
        self.assertEqual(stats.warmup_iterations, 0)
        self.assertGreater(stats.average_ms, 0.0)
        self.assertGreaterEqual(stats.max_ms, stats.min_ms)
        self.assertGreaterEqual(stats.p50_ms, stats.min_ms)
        self.assertLessEqual(stats.p95_ms, stats.max_ms)

    def test_benchmark_callable_rejects_non_positive_iterations(self) -> None:
        with self.assertRaises(ValueError):
            benchmark_callable(lambda: None, iterations=0)

    def test_benchmark_callable_runs_warmup_before_measured_iterations(self) -> None:
        calls = 0

        def target() -> None:
            nonlocal calls
            calls += 1

        stats = benchmark_callable(target, iterations=3, warmup=2)

        self.assertEqual(calls, 5)
        self.assertEqual(stats.iterations, 3)
        self.assertEqual(stats.warmup_iterations, 2)

    def test_benchmark_callable_rejects_negative_warmup(self) -> None:
        with self.assertRaises(ValueError):
            benchmark_callable(lambda: None, warmup=-1)


if __name__ == "__main__":
    unittest.main()
