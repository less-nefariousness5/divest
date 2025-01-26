# Contributing to Project Sylvanas SimC Parser

Thank you for your interest in contributing to the PS SimC Parser! This document provides guidelines and information for contributors.

## Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/ps-simc-parser.git
cd ps-simc-parser
```
3. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

## Development Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Run tests:
```bash
python -m pytest tests/
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Add type hints where appropriate

## Adding New Features

### Adding API Mappings

1. Update `api/mapping.py` with new mappings
2. Add tests in `tests/test_mapping.py`
3. Update API documentation in `docs/API.md`

### Parser Modifications

1. Make changes in relevant parser files
2. Add unit tests
3. Update documentation
4. Verify existing tests pass

## Testing

- Write unit tests for new features
- Update existing tests as needed
- Ensure all tests pass before submitting PR
- Add integration tests for complex features

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description
6. Address review comments

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
