# helper

[![githubactions](https://github.com/kyhau/aws-tools/workflows/Common%20Helper%20-%20Build/badge.svg)](https://github.com/kyhau/aws-tools/actions)
[![codecov](https://codecov.io/gh/kyhau/aws-tools/branch/main/graph/badge.svg)](https://codecov.io/gh/kyhau/aws-tools)

> **Note:** The codecov badge shows repository-wide coverage. The `helper` package maintains 80%+ coverage with comprehensive tests.

A collection of common helper functions for AWS development and operations.

**Supported Python Versions:** 3.10, 3.11, 3.12

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation)

### Installation

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Or install for production only (no dev dependencies)
poetry install --only main
```

## 📦 Usage

### Console Scripts

After installation, the following commands are available:

- `helper` - Main helper CLI
- `dockerc` - Find and remove non-running containers
- `dockeri` - Find and remove dangling images

```bash
# Activate Poetry shell
poetry shell

# Run commands
dockerc --help
dockeri --help
```

## 🧪 Development

### Running Tests

```bash
# Quick test run (uses current Python version, defaults to 3.12)
make test

# Run tests with coverage
make coverage

# Run all checks (lint + test + coverage)
make check

# Run CI checks (what GitHub Actions runs)
make ci

# Note: Multi-version testing (3.10, 3.11, 3.12) happens automatically in GitHub Actions
```

### Using Poetry Directly

```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=helper --cov-report=term --cov-report=html

# Run linting
poetry run flake8 helper

# Run specific test file
poetry run pytest helper/tests/test_aws.py -v
```

### Makefile Commands

Essential commands for development:

```bash
make help           # Show all available commands
make install        # Install production dependencies
make install-dev    # Install all dependencies including dev
make test           # Run tests
make coverage       # Run tests with coverage report
make lint           # Run linting checks
make clean          # Clean build artifacts and caches
make build          # Build wheel package
make check          # Run all checks (lint + test + coverage)
make ci             # Run CI checks (what GitHub Actions runs)
make all            # Run complete workflow
```

**Note:** Multi-version testing across Python 3.10, 3.11, and 3.12 is handled by the GitHub Actions workflow matrix.

## 🏗️ Building

```bash
# Build wheel package
make build

# Or using Poetry directly
poetry build

# Build wheel only (no sdist)
poetry build -f wheel
```

## 📋 Project Structure

```
_common/
├── helper/              # Main package
│   ├── aws.py          # AWS helper functions
│   ├── docker.py       # Docker utilities
│   ├── file_io.py      # File I/O operations
│   ├── http.py         # HTTP utilities
│   ├── logger.py       # Logging configuration
│   ├── selector.py     # Interactive selectors
│   ├── ser.py          # Serialization utilities
│   └── tests/          # Test suite
├── pyproject.toml      # Poetry configuration
├── Makefile            # Development commands
└── README.md           # This file
```

## 🔧 Configuration

### Python Version

The Makefile uses the Python version installed with Poetry (defaults to 3.12). To change:

```bash
# Use specific Python version
poetry env use 3.11
poetry install

# Check current version
poetry run python --version
```

**Multi-version testing** (3.10, 3.11, 3.12) is handled automatically by the GitHub Actions workflow matrix.

### Poetry

Dependencies and project metadata are managed in `pyproject.toml`.

To update dependencies:

```bash
# Update all dependencies
poetry update

# Update specific dependency
poetry update boto3

# Update lock file without upgrading
poetry lock --no-update
```

### Testing Configuration

Test configuration is in `pyproject.toml` under `[tool.pytest.ini_options]`.

Coverage configuration is in `pyproject.toml` under `[tool.coverage.run]`.

### Linting Configuration

Flake8 configuration is in `.flake8` file.

## 📝 Adding Dependencies

```bash
# Add production dependency
poetry add package-name

# Add dev dependency
poetry add --group dev package-name

# Add with specific version
poetry add "package-name==1.2.3"
```

## 🐛 Troubleshooting

### Check project health

```bash
make doctor
```

### Clear Poetry cache

```bash
poetry cache clear pypi --all
```

### Recreate virtual environment

```bash
poetry env remove python
poetry install
```

## 📄 License

See the main repository for license information.
