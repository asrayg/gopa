# Release Readiness Checklist

## ✅ Completed

### Documentation
- [x] README.md with logo and examples
- [x] CHANGELOG.md with version history
- [x] CONTRIBUTING.md with contribution guidelines
- [x] CODE_OF_CONDUCT.md
- [x] SECURITY.md with security policy
- [x] QUICKSTART.md for new users
- [x] RELEASE.md with release process

### Packaging
- [x] setup.py with proper metadata
- [x] pyproject.toml for modern Python packaging
- [x] MANIFEST.in for distribution files
- [x] requirements-dev.txt for development dependencies
- [x] .gitignore comprehensive

### CI/CD
- [x] GitHub Actions workflow for CI (tests on multiple OS/Python versions)
- [x] GitHub Actions workflow for releases
- [x] Issue templates (bug report, feature request)

### Code Quality
- [x] All comments removed
- [x] Consistent naming (Gopa, not GopaLang)
- [x] Test suite with 19 conformance tests
- [x] Examples directory with working examples

### Development Tools
- [x] Makefile for common tasks
- [x] Pre-commit hooks configuration
- [x] Linting configuration (ruff, black)

## 🔄 Before First Release

### Testing
- [ ] Run full test suite: `make test`
- [ ] Test on all supported Python versions (3.11, 3.12, 3.13)
- [ ] Test on all supported OS (Linux, macOS, Windows)
- [ ] Verify all examples work
- [ ] Test installation from source: `pip install -e .`
- [ ] Test CLI commands work

### Documentation Review
- [ ] Verify all links in README work
- [ ] Check that examples in README are correct
- [ ] Ensure CHANGELOG is complete
- [ ] Review CONTRIBUTING.md for clarity

### Security
- [ ] Security audit of permission system
- [ ] Review Python FFI allowlist
- [ ] Check for any hardcoded secrets
- [ ] Verify sandbox isolation

### Distribution
- [ ] Build distribution: `make build`
- [ ] Test installation from wheel: `pip install dist/*.whl`
- [ ] Test installation from source: `pip install dist/*.tar.gz`
- [ ] Verify package data (stdlib files) are included

### Release Process
- [ ] Create release branch
- [ ] Update version numbers
- [ ] Update CHANGELOG with release date
- [ ] Create git tag
- [ ] Create GitHub release
- [ ] (Optional) Publish to PyPI

## 📋 Release Commands

```bash
# 1. Run tests
make test

# 2. Format and lint
make format
make lint

# 3. Build distribution
make build

# 4. Test installation
pip install dist/gopa-lang-*.whl
gopa --help

# 5. Create release tag
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

## 🚀 Post-Release

- [ ] Announce on social media/community
- [ ] Update website if applicable
- [ ] Monitor for issues
- [ ] Plan next release

