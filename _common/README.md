# helper

[![CI](https://github.com/kyhau/aws-tools/workflows/Common%20Helper%20-%20Build/badge.svg)](https://github.com/kyhau/aws-tools/actions)
[![Codecov](https://codecov.io/gh/kyhau/aws-tools/branch/main/graph/badge.svg)](https://codecov.io/gh/kyhau/aws-tools)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://en.wikipedia.org/wiki/MIT_License)

Common helper functions for AWS development and operations.

> **Note:** The codecov badge shows repository-wide coverage. The `helper` package maintains 80%+ coverage with comprehensive tests.

**Supports Python 3.10, 3.11, 3.12, 3.13**

## ✨ Features

- **AWS Utilities** - Common AWS helper functions and operations
- **Docker Tools** - Container and image management utilities
- **File I/O** - Advanced file and configuration handling
- **Interactive Selectors** - CLI prompts with InquirerPy
- **Logging** - Standardized logging configuration
- **Serialization** - JSON and data serialization utilities

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) (recommended) or pip

### Installation

#### Using Poetry (Recommended)

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Complete first-time setup
make setup-init

# Or install manually
poetry install
```

#### Using pip

```bash
pip install -e .
```

### Available Console Scripts

After installation, the following commands are available:

- **`helper`** - Main helper CLI
- **`dockerc`** - Find and remove non-running containers
- **`dockeri`** - Find and remove dangling images

```bash
# Run commands
dockerc --help
dockeri --help
```

## 🧪 Development

### Makefile Commands

Run `make help` to see all available commands:

```bash
make help              # Show all available commands
make setup-init        # Complete first-time setup
make install           # Install main dependencies only
make install-dev       # Install main + dev dependencies
make install-test      # Install main + test dependencies
make install-all       # Install all dependencies
make format-python     # Format Python code with black
make lint-python       # Lint Python code with flake8
make test              # Run unit tests without coverage
make test-with-coverage # Run tests with coverage reporting
make pre-commit        # Run all quality checks (format, lint, test)
make build             # Build the Python package
make clean             # Clean test artifacts and temporary files
make clean-all         # Clean everything including virtual environment
```

### Quick Development Workflow

```bash
# 1. Make your code changes
# 2. Run all quality checks before committing
make pre-commit

# Or run individual checks
make format-python      # Auto-format with black
make lint-python        # Lint with flake8
make test-with-coverage # Test with coverage
```

### Using Poetry Directly

```bash
# Run tests
poetry run pytest tests/ -v

# Run tests with coverage
poetry run pytest --cov=helper --cov-report=term tests/

# Run linting
poetry run flake8 helper/

# Run specific test file
poetry run pytest tests/test_aws.py -v
```

## 📦 Usage Examples

### AWS Helpers

```python
from helper.aws import get_boto3_session, assume_role

# Get boto3 session
session = get_boto3_session()

# Assume role
credentials = assume_role(role_arn, session_name)
```

### Docker Utilities

```bash
# Find and list non-running containers
dockerc

# Find and list dangling images
dockeri
```

### File I/O

```python
from helper.file_io import read_yaml, write_yaml

# Read YAML file
config = read_yaml("config.yml")

# Write YAML file
write_yaml(data, "output.yml")
```

### Interactive Selectors

```python
from helper.selector import prompt_single_selection

# Prompt user to select from options
choice = prompt_single_selection(
    name="environment",
    options=["dev", "staging", "prod"],
    message="Select environment:"
)
```

## 🏗️ Building

```bash
# Build wheel package
make build

# Or using Poetry directly
poetry build
```

## 📋 Project Structure

```
_common/
├── helper/              # Main package
│   ├── __init__.py
│   ├── aws.py          # AWS helper functions
│   ├── date_time.py    # Date/time utilities
│   ├── docker.py       # Docker utilities
│   ├── file_io.py      # File I/O operations
│   ├── http.py         # HTTP utilities
│   ├── logger.py       # Logging configuration
│   ├── selector.py     # Interactive selectors
│   ├── ser.py          # Serialization utilities
│   └── wrappers.py     # Function wrappers
├── tests/              # Test suite
│   ├── conftest.py
│   ├── test_aws.py
│   ├── test_datetime.py
│   ├── test_docker.py
│   ├── test_file_io.py
│   ├── test_http.py
│   ├── test_init.py
│   ├── test_logger.py
│   ├── test_selector.py
│   ├── test_ser.py
│   └── test_wrappers.py
├── pyproject.toml      # Poetry configuration
├── Makefile            # Development commands
└── README.md           # This file
```

## 🔧 Configuration

### Managing Dependencies

```bash
# Update lock file from pyproject.toml
make lock

# Update dependencies to latest compatible versions
make update-deps

# Or using Poetry directly
poetry lock --no-update    # Update lock without changing versions
poetry update              # Update to latest compatible versions
poetry update boto3        # Update specific package
```

### Python Version Management

```bash
# Use specific Python version
poetry env use python3.11
poetry install

# Check current version
poetry run python --version

# List available environments
poetry env list
```

### Testing Configuration

Test and coverage configuration is in `pyproject.toml`:
- `[tool.pytest.ini_options]` - pytest settings
- `[tool.coverage.run]` - coverage settings
- `[tool.coverage.report]` - coverage reporting

### Code Quality

Linting configuration in `.flake8` file with max line length of 120.

Code formatting uses [black](https://black.readthedocs.io/) with default settings.

## 🐛 Troubleshooting

### Clear Poetry cache

```bash
poetry cache clear pypi --all
```

### Recreate virtual environment

```bash
poetry env remove python
make setup-init
```

### Check dependency conflicts

```bash
poetry check
poetry show --tree
```

## 🤝 Contributing

1. Make your changes
2. Run `make pre-commit` to ensure all checks pass
3. Commit your changes
4. Create a pull request

## 📄 License

See the [main repository](https://github.com/kyhau/aws-tools) for license information (MIT).

## 🔗 Related

- [aws-tools](https://github.com/kyhau/aws-tools) - Parent repository with AWS tools and examples
