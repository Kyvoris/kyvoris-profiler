# Release Checklist

Use this checklist before tagging a release.

## Local Validation

```powershell
python -m pytest
python -m unittest discover -s tests
powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\release-check.ps1
```

## Package Checks

- Confirm `pyproject.toml` version matches `kyvoris_profiler.__version__`.
- Confirm release notes include the new version.
- Build source and wheel artifacts with `python -m build`.
- Validate artifacts with `python -m twine check dist\*`.
- Install the built wheel into a clean virtual environment.
- Run `kyvoris-profiler --version` from the clean environment.

## Release Notes

- Summarize user-facing changes.
- Mention any CLI or report schema changes.
- Include validation commands.
- Call out optional Hugging Face checks separately when used.

## Tagging

Tag only after the release commit is pushed and the working tree is clean.

```powershell
git tag v1.0.0
git push origin v1.0.0
```
