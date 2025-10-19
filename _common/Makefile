.PHONY: help setup-init setup-venv lock update-deps install install-dev install-test install-all format-python lint-python lint-yaml pre-commit test test-with-coverage build clean clean-all

PACKAGE_NAME := helper
TEST_PATH := tests/
POETRY := poetry

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup-init: setup-venv lock install-all ## Complete first-time setup (configure venv, lock, install all deps)

setup-venv: ## Configure Poetry to use .venv in project directory
	$(POETRY) config virtualenvs.in-project true --local

lock: ## Regenerate poetry.lock from pyproject.toml
	$(POETRY) lock

update-deps: ## Update dependencies to latest compatible versions
	$(POETRY) update

install: ## Install main dependencies only
	$(POETRY) install --only main

install-dev: ## Install main + dev dependencies
	$(POETRY) install --only main,dev

install-test: ## Install main + test dependencies
	$(POETRY) install --only main,test

install-all: ## Install all dependencies (main + dev + test)
	$(POETRY) install

format-python: install-dev ## Format Python code with black
	@$(POETRY) run black $(PACKAGE_NAME)/ $(TEST_PATH)

lint-python: install-dev ## Lint Python code with flake8
	@$(POETRY) run flake8 --max-line-length=100 $(PACKAGE_NAME)/ $(TEST_PATH)

lint-yaml: install-dev ## Lint YAML files with yamllint
	@$(POETRY) run yamllint -c .yamllint.yml . || true

pre-commit: format-python lint-python test-with-coverage ## Run all quality checks (format, lint, test)
	@echo "✓ All pre-commit checks passed!"

test: install-test ## Run unit tests without coverage
	@$(POETRY) run pytest $(TEST_PATH) -v

test-with-coverage: install-test ## Run unit tests with coverage reporting
	@$(POETRY) run pytest --cov=$(PACKAGE_NAME) --cov-report=xml:coverage.xml --cov-report=term $(TEST_PATH)

build: install-all ## Build the Python package
	@$(POETRY) build

clean: ## Clean test artifacts, build artifacts and temporary files
	@rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov/ .tox/ junit.xml coverage.xml
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name '*.pyc' -delete
	@find . -type f -name '*.pyo' -delete

clean-all: clean ## Clean everything including virtual environment
	@rm -rf .venv/
