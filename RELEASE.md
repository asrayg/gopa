# Release Checklist

## Pre-Release

- [ ] All tests pass: `python -m gopa_lang.gopa test`
- [ ] Code is formatted: `make format`
- [ ] Linting passes: `make lint`
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated
- [ ] Version number is updated in:
  - [ ] `gopa_lang/__init__.py`
  - [ ] `setup.py`
  - [ ] `pyproject.toml`
- [ ] All examples work
- [ ] Security review completed

## Release Process

1. Create release branch: `git checkout -b release/v0.2.0`
2. Update version numbers
3. Update CHANGELOG.md with release date
4. Commit changes: `git commit -am "Release v0.2.0"`
5. Tag release: `git tag -a v0.2.0 -m "Release v0.2.0"`
6. Push branch and tags: `git push origin release/v0.2.0 && git push origin v0.2.0`
7. Merge to main
8. Create GitHub release with release notes

## Post-Release

- [ ] Build distribution: `make build`
- [ ] Test installation from source: `pip install dist/gopa-lang-*.tar.gz`
- [ ] Publish to PyPI (if applicable): `twine upload dist/*`
- [ ] Update website/docs
- [ ] Announce release

