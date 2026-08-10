# Makefile for BioCognitive-AI Framework v4

.PHONY: help install install-dev clean lint format type-check test coverage run-examples docs

help:
	@echo "BioCognitive-AI Framework v4 - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install          Install core dependencies"
	@echo "  install-dev      Install dev dependencies (includes lint, test, docs)"
	@echo "  lint             Run flake8 linter"
	@echo "  format           Format code with black & isort"
	@echo "  type-check       Run mypy type checker"
	@echo "  test             Run pytest tests"
	@echo "  coverage         Run tests with coverage report"
	@echo "  run-examples     Run all examples"
	@echo "  docs             Build documentation (Sphinx)"
	@echo "  clean            Clean build artifacts and cache"
	@echo ""

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

lint:
	flake8 bio_agent_v4/ --max-line-length=100
	pylint bio_agent_v4/ --disable=C0111,C0103

format:
	black bio_agent_v4/ examples/ docs/
	isort bio_agent_v4/ examples/ docs/

type-check:
	mypy bio_agent_v4/ --ignore-missing-imports

test:
	pytest bio_agent_v4/tests/ -v

coverage:
	pytest bio_agent_v4/tests/ -v --cov=bio_agent_v4 --cov-report=html --cov-report=term
	@echo "Coverage report: htmlcov/index.html"

run-examples:
	@echo "Running Example 1: Attention Flow"
	python examples/simple_attention_flow.py
	@echo ""
	@echo "Running Example 2: Prediction Resolution"
	python examples/prediction_resolution.py
	@echo ""
	@echo "Running Example 3: Sleep Consolidation"
	python examples/sleep_consolidation.py

docs:
	cd docs && sphinx-build -b html . _build/html
	@echo "Documentation built: docs/_build/html/index.html"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name 'htmlcov' -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned up cache directories"

.DEFAULT_GOAL := help
