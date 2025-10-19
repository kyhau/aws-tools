# Contributing

Thank you for your interest in contributing to this project!

## How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Use the issue templates when available
- Provide clear reproduction steps for bugs
- Include relevant logs, screenshots, or error messages

### Pull Requests

1. **Fork and clone** the repository
2. **Create a branch** for your changes: `git checkout -b feature/your-feature-name`
3. **Make your changes** following the project's code style
4. **Add tests** for new functionality
5. **Run tests** to ensure everything passes
6. **Update documentation** (README, CHANGELOG, etc.)
7. **Commit** with clear, descriptive messages
8. **Push** to your fork and **submit a pull request**

### Pull Request Guidelines

- Fill out the PR template completely
- Link related issues
- Keep changes focused and atomic
- Ensure all CI checks pass
- Respond to review feedback promptly

### Code Style

- Follow existing code conventions
- Run linters and formatters before committing
- Write clear, self-documenting code
- Add comments for complex logic

### Testing

- Write unit tests for new features
- Ensure existing tests pass
- Aim for good test coverage
- Test edge cases and error conditions

## Development Workflow

For Python projects using Makefile:
```bash
make setup-init        # Complete first-time setup
make pre-commit        # Run all quality checks
make test-with-coverage # Run tests with coverage
make lint-python       # Lint Python code
make format-python     # Format Python code
make clean             # Clean artifacts
```

## Questions?

If you have questions, please open an issue or reach out to the maintainers.

## Code of Conduct

Please note that this project follows a Code of Conduct. By participating, you agree to uphold this code.

