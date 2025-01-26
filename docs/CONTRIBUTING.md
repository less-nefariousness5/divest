# Contributing to PS SimC Parser

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/ps-simc-parser.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Unix/macOS: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Install development dependencies: `pip install -r requirements-dev.txt`

## Development Process

1. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Update documentation if needed
5. Commit your changes: `git commit -am "Add your feature"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use type hints where possible
- Format code with `black`
- Sort imports with `isort`

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_parser.py

# Run specific test class
pytest tests/test_parser.py::TestParser

# Run specific test
pytest tests/test_parser.py::TestParser::test_parse_action
```

### Writing Tests

1. Create test files in the `tests` directory
2. Name test files with `test_` prefix
3. Name test classes with `Test` prefix
4. Name test methods with `test_` prefix
5. Use descriptive test names
6. Include both positive and negative test cases
7. Test edge cases
8. Use fixtures where appropriate

Example:
```python
def test_parse_action():
    parser = Parser()
    action = "cast_spell,if=condition"
    result = parser.parse_action(action)
    assert result.type == "cast"
    assert result.condition == "condition"
```

## Documentation

### API Documentation

1. Document all public APIs
2. Include examples
3. Document parameters and return types
4. Document exceptions
5. Document any special behavior

Example:
```python
def parse_action(action: str) -> Action:
    """Parse a SimC action into an Action object.

    Args:
        action: The SimC action string to parse

    Returns:
        An Action object representing the parsed action

    Raises:
        ParseError: If the action string is invalid
    """
```

### User Documentation

1. Keep README.md up to date
2. Document new features in API.md
3. Update CHANGELOG.md
4. Add examples to docs/examples/

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Reporting Issues

1. Check existing issues first
2. Use issue templates
3. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - System information
   - Error messages
   - Code examples

## Code Review Process

1. All code must be reviewed
2. Address review comments
3. Keep discussions focused
4. Be respectful and constructive
5. Request re-review after changes

## Versioning

We use [Semantic Versioning](https://semver.org/):

- MAJOR version for incompatible API changes
- MINOR version for new functionality
- PATCH version for bug fixes

## License

By contributing, you agree that your contributions will be licensed under the project's license.
