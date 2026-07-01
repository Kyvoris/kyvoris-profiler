"""Benchmark a real Hugging Face model inference call.

This example keeps model loading outside the measured function, so the benchmark
captures inference latency rather than setup time.
"""

from __future__ import annotations

from kyvoris_profiler import benchmark_callable, format_text_report


MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
TEXT = "Kyvoris Profiler makes inference benchmarking simple."


def main() -> None:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise SystemExit(
            "This example requires optional model dependencies.\n"
            "Install them with:\n"
            '  python -m pip install "transformers[torch]"'
        ) from exc

    classifier = pipeline("sentiment-analysis", model=MODEL_NAME)

    def run_inference() -> list[dict[str, float | str]]:
        return classifier(TEXT)

    sample_output = run_inference()

    result = benchmark_callable(run_inference, iterations=10, warmup=1)

    print(format_text_report(result, title="Real Model Inference Benchmark"))
    print()
    print(f"Model: {MODEL_NAME}")
    print(f"Input: {TEXT}")
    print(f"Sample output: {sample_output}")


if __name__ == "__main__":
    main()
