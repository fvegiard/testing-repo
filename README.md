# Testing Repository

A comprehensive Python testing repository with modern development dependencies and best practices for 2026.

## Features

- **Testing Framework**: pytest with plugins for coverage, parallel execution, mocking, and async support
- **Type Checking**: mypy with strict type checking
- **Linting**: ruff (modern, fast linter) and pylint
- **Formatting**: black with consistent code style
- **Security**: bandit for security vulnerability scanning
- **Pre-commit Hooks**: Automated code quality checks before commits
- **CI/CD**: GitHub Actions workflow for automated testing
- **Documentation**: Sphinx for documentation generation

## Quick Start

### Installation

```bash
# Install the project with dev dependencies
pip install -e ".[dev]"

# Or using uv (recommended for 2026)
uv pip install -e ".[dev]"
```

### Setup Pre-commit Hooks

```bash
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run in parallel
pytest -n auto

# Run specific test markers
pytest -m "not slow"
pytest -m unit
```

### Code Quality Checks

```bash
# Linting
ruff check .
ruff format .

# Type checking
mypy src

# Security scanning
bandit -r src

# Format code
black src tests
```

## Project Structure

```
testing-repo/
├── src/              # Source code
├── tests/            # Test files
├── docs/             # Documentation
├── pyproject.toml    # Project configuration
├── .pre-commit-config.yaml
├── .gitignore
└── README.md
```

## Development Workflow

1. Create a feature branch
2. Make your changes
3. Pre-commit hooks will run automatically
4. Run tests: `pytest`
5. Check coverage: `pytest --cov=src`
6. Commit and push

## CI/CD

GitHub Actions workflow runs on:
- Push to main/master
- Pull requests
- Scheduled runs (optional)

## Dependencies

All development dependencies are listed in `pyproject.toml` under `[project.optional-dependencies.dev]`.

## License

MIT
