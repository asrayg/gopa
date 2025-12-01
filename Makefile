.PHONY: help test lint format install clean build dist

help:
	@echo "Gopa Development Commands:"
	@echo "  make test       - Run test suite"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make install    - Install package in development mode"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make build      - Build distribution packages"
	@echo "  make dist       - Create source distribution"

test:
	python -m gopa_lang.gopa test

lint:
	ruff check gopa_lang/ tests/ || true
	mypy gopa_lang/ --ignore-missing-imports || true

format:
	ruff check --fix gopa_lang/ tests/
	black gopa_lang/ tests/

install:
	pip install -e .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	find . -type d -name __pycache__ -exec rm -r {} + || true
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

dist: build
	@echo "Distribution packages created in dist/"

