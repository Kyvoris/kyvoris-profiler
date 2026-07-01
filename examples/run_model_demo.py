"""Benchmark real Hugging Face model inference calls.

This example keeps model loading outside the measured function, so the benchmark
captures inference latency rather than setup time.
"""

from __future__ import annotations

import argparse

from kyvoris_profiler import format_text_report, profile_callable


MODEL_NAMES = (
    "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "lxyuan/distilbert-base-multilingual-cased-sentiments-student",
)
TEXT = "Kyvoris Profiler makes inference benchmarking simple."


def parse_args() -> argparse.Namespace:
    """Parse example-only command-line options."""
    parser = argparse.ArgumentParser(
        description="Benchmark one or more Hugging Face sentiment models.",
    )
    parser.add_argument(
        "--model",
        action="append",
        dest="models",
        help=(
            "Model ID to benchmark. Can be passed multiple times. "
            "Default: three curated sentiment models."
        ),
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=10,
        help="Number of measured iterations per model. Default: 10.",
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=1,
        help="Number of untimed warmup calls per model. Default: 1.",
    )
    parser.add_argument(
        "--text",
        default=TEXT,
        help="Input text used for each model.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        from transformers import pipeline
    except ImportError as exc:
        raise SystemExit(
            "This example requires optional model dependencies.\n"
            "Install them with:\n"
            '  python -m pip install "transformers[torch]"'
        ) from exc

    model_names = args.models or list(MODEL_NAMES)

    for index, model_name in enumerate(model_names, start=1):
        classifier = pipeline("sentiment-analysis", model=model_name)

        def run_inference() -> list[dict[str, float | str]]:
            return classifier(args.text)

        sample_output = run_inference()

        result = profile_callable(
            run_inference,
            iterations=args.iterations,
            warmup=args.warmup,
            collect_cpu=True,
            collect_memory=True,
        )

        if index > 1:
            print()
        print(format_text_report(result, title="Real Model Inference Benchmark"))
        print()
        print(f"Model: {model_name}")
        print(f"Input: {args.text}")
        print(f"Sample output: {sample_output}")


if __name__ == "__main__":
    main()
