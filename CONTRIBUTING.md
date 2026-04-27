# Contributing to Duplicate Finding Tool

Thank you for considering contributing to the Duplicate Finding Tool! We welcome all kinds of contributions, including bug reports, feature requests, documentation improvements, and code contributions.

## Reporting Bugs

### Before Submitting a Bug Report

- Check the issue tracker to ensure the bug hasn't already been reported
- Check the documentation and README
- Collect relevant information about your environment

### How to Submit a Bug Report

Please use GitHub Issues with the Bug Report template. Include:
- A clear, descriptive title
- Exact steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment (OS, Python version, package version)
- Any relevant logs or error messages

## Suggesting Enhancements

Use GitHub Issues with the Feature Request template. Include:
- A clear, descriptive summary of the feature
- The motivation and use case
- Proposed implementation details
- Alternative solutions you've considered
- Any additional context

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install in development mode: `pip install -e .[dev]`

## Coding Standards

This project follows strict code quality standards:

- **Linting**: Run `ruff check .` to check for style issues
- **Type Checking**: Run `mypy src` for type safety
- **Formatting**: Run `ruff format .` to auto-format code
- **Testing**: Run `pytest` to ensure all tests pass

Before submitting a PR, ensure:
- All code passes `ruff check` and `ruff format`
- All code passes `mypy` type checking
- All tests pass with `pytest`
- New code includes appropriate unit tests

## Testing

Tests are located in the `tests/` directory and use pytest. To run tests:

```bash
pytest                  # Run all tests
pytest -v              # Verbose output
pytest tests/test_file.py  # Run specific test file
pytest -k test_name    # Run specific test
```

Aim for good test coverage of new code.

## Pull Request Process

1. Fork the repository and create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes, following the coding standards above
3. Add or update tests as needed
4. Commit your changes with clear, descriptive messages
5. Push to your fork and submit a Pull Request
6. Ensure all CI checks pass
7. Wait for review and address any feedback

### Pull Request Checklist

- [ ] My code follows the style guidelines (ruff, mypy)
- [ ] I have performed a self-review of my code
- [ ] All tests pass locally
- [ ] I have added/updated documentation if needed
- [ ] I have added/updated tests for new functionality
- [ ] My commit messages are clear and descriptive

## Commit Message Guidelines

Write clear commit messages that:
- Start with a short summary (50 characters or less)
- Use imperative mood ("Add feature" not "Added feature")
- Reference related issues (e.g., "Fixes #123")
- Provide more details in the body if needed, separated by a blank line

Example:
```
Add MinHash clustering for duplicate detection

This implements LSH-based clustering for efficient duplicate
detection. Improves performance by 10x for large datasets.

Fixes #456
```

## Questions?

Feel free to open a discussion in GitHub Discussions for questions or open an issue for bugs/features!

Thank you for contributing! 🎉
