.PHONY: help install install-dev test coverage lint clean build check ci all

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	poetry install --only main

install-dev: ## Install all dependencies including dev
	poetry install

test: ## Run tests
	poetry run pytest helper/tests -v

coverage: ## Run tests with coverage report
	poetry run pytest --cov=helper --cov-report=term --cov-report=html --cov-report=xml --cov-fail-under=80 helper/tests
	@echo "\nHTML coverage report: htmlcov/index.html"

lint: ## Run linting checks
	poetry run flake8 helper

clean: ## Clean build artifacts and caches
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov/ .tox/
	rm -f flake8.log coverage*.xml junit*.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete

build: clean ## Build wheel package
	poetry build

check: ## Run all checks (lint + test + coverage)
	@echo "Running linting..."
	$(MAKE) lint
	@echo "\nRunning tests with coverage..."
	$(MAKE) coverage
	@echo "\n✓ All checks passed!"

ci: ## Run CI checks (what GitHub Actions runs)
	poetry run pip check
	poetry run pytest --cov=. --cov-report=xml:coverage.xml --cov-report=term --cov-fail-under=80 --junit-xml=junit.xml helper/tests
	poetry run flake8 helper
	poetry build

all: clean install-dev check build ## Run complete workflow
