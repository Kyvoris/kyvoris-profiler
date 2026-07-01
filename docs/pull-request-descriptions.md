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
