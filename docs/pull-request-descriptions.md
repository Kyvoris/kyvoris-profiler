# Pull Request Descriptions

Pull requests should be short, specific, and easy to review. Use this structure
for feature work.

## Template

```markdown
## Summary

- What changed?
- Why is it needed?

## Testing

- [ ] `python -m pytest`
- [ ] `python -m unittest discover -s tests`

## Release Notes

- Added/Changed/Fixed:

## Risk

- What could break?
- Is the public API affected?

## Linked Issues

Closes #
```

## Example for 0.2.0

```markdown
## Summary

- Added warmup iterations to `benchmark_callable()`.
- Added JSON and HTML report formatters.
- Updated examples, docs, tests, and release planning artifacts.

## Testing

- [x] `python -m pytest`
- [x] `python -m unittest discover -s tests`

## Release Notes

- Added warmup-aware benchmark runs.
- Added structured JSON and standalone HTML reports.

## Risk

- Low. Existing `benchmark_callable(callable_obj, iterations=N)` usage remains
  compatible because `warmup` defaults to `0`.

## Linked Issues

Closes #1
Closes #2
Closes #3
```

## Example for 0.3.0

```markdown
## Summary

- Added `profile_callable()` for opt-in resource profiling.
- Added process CPU time and peak Python-traced memory metrics.
- Updated reports, examples, docs, tests, and release notes for `0.3.0`.

## Testing

- [x] `python -m pytest`
- [x] `python -m unittest discover -s tests`

## Release Notes

- Added CPU and memory profiling support.
- Preserved `benchmark_callable()` compatibility for latency-only usage.

## Risk

- Low. Resource collection is opt-in, and the default latency-only behavior
  remains unchanged.

## Linked Issues

Closes #4
Closes #5
Closes #6
```

## Example for 0.4.0

```markdown
## Summary

- Added `kyvoris-profiler` console script and `python -m kyvoris_profiler`.
- Added CLI options for iterations, warmup, output format, output path, CPU,
  memory, and title.
- Updated README, CLI docs, release notes, issue guidance, and tests.

## Testing

- [x] `python -m pytest`
- [x] `python -m unittest discover -s tests`

## Release Notes

- Added command-line benchmarking for no-argument `module:function` targets.

## Risk

- Low. CLI is additive and reuses the existing profiling and reporting APIs.

## Linked Issues

Closes #7
Closes #8
Closes #9
```

## Example for 0.5.0

```markdown
## Summary

- Added async callable profiling APIs.
- Added lightweight HTTP endpoint profiling.
- Added failure counts for captured measured-iteration errors.
- Updated CLI, examples, tests, release notes, and docs for `0.5.0`.

## Testing

- [x] `python -m pytest`
- [x] `python -m unittest discover -s tests`
- [x] `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## Release Notes

- Added async and endpoint benchmark support.

## Risk

- Medium-low. New APIs are additive, and existing sync behavior remains the
  default.

## Linked Issues

Closes #10
Closes #11
Closes #12
```

## Example for 0.6.0

```markdown
## Summary

- Added `compare_profiles()` and comparison dataclasses.
- Added text, Markdown, JSON, and HTML comparison reports.
- Added `kyvoris-profiler compare` for saved JSON benchmark reports.
- Updated examples, tests, test runner, release notes, and docs for `0.6.0`.

## Testing

- [x] `python -m pytest`
- [x] `python -m unittest discover -s tests`
- [x] `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## Release Notes

- Added benchmark comparison support.

## Risk

- Low. The comparison API is additive and preserves existing profiling behavior.

## Linked Issues

Closes #13
Closes #14
Closes #15
```

## Example for 0.7.0

```markdown
## Summary

- Added threshold evaluation for profile comparisons.
- Added CLI regression gate flags for comparison reports.
- Added TOML config support for repeatable comparison settings.
- Updated test runner, docs, release notes, and tests for `0.7.0`.

## Testing

- [x] `python -m pytest`
- [x] `python -m unittest discover -s tests`
- [x] `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## Release Notes

- Added CI-friendly threshold checks for benchmark regressions.

## Risk

- Low. Threshold checks are opt-in and do not change existing comparison output.

## Linked Issues

Closes #16
Closes #17
```

## Example for 0.7.1

```markdown
## Summary

- Added TOML config support for comparison and threshold settings.
- Added sample `kyvoris-profiler.toml`.
- Updated test runner, docs, release notes, and CLI tests for `0.7.1`.

## Testing

- [x] `python -m pytest`
- [x] `python -m unittest discover -s tests`
- [x] `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## Release Notes

- Added repeatable TOML config for comparison workflows.

## Risk

- Low. Config support is additive and CLI flags still override config values.

## Linked Issues

Closes #18
```
