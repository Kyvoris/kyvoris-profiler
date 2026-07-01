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
