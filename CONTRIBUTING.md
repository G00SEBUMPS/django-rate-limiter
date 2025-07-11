# Contributing to Django Rate Limiter

Thank you for your interest in contributing to Django Rate Limiter! This document provides guidelines and information for contributors.

## 🚀 Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/django-rate-limiter.git
   cd django-rate-limiter
   ```

3. **Set up development environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .[dev]
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Django 3.2+
- Redis (for Redis backend testing)

### Installation
```bash
# Install in development mode with all dependencies
pip install -e .[dev]

# Or install specific extras
pip install -e .[redis]  # For Redis support
```

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=django_rate_limiter --cov-report=html

# Run specific test file
pytest tests/test_algorithms.py -v

# Run specific test
pytest tests/test_algorithms.py::TestSlidingWindowRateLimiter::test_basic_rate_limiting -v
```

### Code Quality
```bash
# Format code with black
black django_rate_limiter tests

# Sort imports
isort django_rate_limiter tests

# Lint with flake8
flake8 django_rate_limiter tests --max-line-length=88

# Type checking with mypy
mypy django_rate_limiter --ignore-missing-imports
```

## 📋 Contribution Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use Black for code formatting (line length: 88)
- Add type hints to all functions and methods
- Write comprehensive docstrings for public APIs
- Use meaningful variable and function names

### Testing Requirements
- Write tests for all new functionality
- Maintain or improve test coverage (currently 95%+)
- Test thread safety for concurrent operations
- Include edge cases and error scenarios
- Mock external dependencies appropriately

### Documentation
- Update README.md for user-facing changes
- Add docstrings for all public methods
- Update CONFIGURATION.md for new configuration options
- Add examples for new features
- Update CHANGELOG.md

### Commit Messages
Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(algorithms): add leaky bucket rate limiter

fix(backends): resolve Redis connection timeout issue

docs(readme): update installation instructions

test(algorithms): add thread safety tests for token bucket
```

## 🔄 Pull Request Process

1. **Ensure your code follows the guidelines** above
2. **Write or update tests** for your changes
3. **Update documentation** as needed
4. **Run the full test suite** and ensure all tests pass
5. **Create a pull request** with:
   - Clear title and description
   - Reference any related issues
   - Include screenshots/examples if applicable

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Thread safety tested (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment information**:
   - Python version
   - Django version
   - Package version
   - Operating system

2. **Steps to reproduce** the issue

3. **Expected vs actual behavior**

4. **Code sample** (minimal reproduction case)

5. **Error messages/logs** (if any)

### Bug Report Template
```markdown
**Environment:**
- Python: 3.x.x
- Django: x.x.x
- django-rate-limiter: x.x.x
- OS: 

**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Behavior:**


**Actual Behavior:**


**Code Sample:**
```python
# Minimal code to reproduce the issue
```

**Error Messages:**
```
Paste any error messages here
```
```

## 💡 Feature Requests

When suggesting new features:

1. **Describe the problem** you're trying to solve
2. **Propose a solution** with examples
3. **Consider backwards compatibility**
4. **Think about performance implications**
5. **Provide use cases** and benefits

## 🏗️ Architecture Guidelines

### Adding New Algorithms

1. **Inherit from `BaseRateLimiter`**:
   ```python
   class MyRateLimiter(BaseRateLimiter):
       def is_allowed(self, identifier, limit, window, scope=""):
           # Implementation here
           pass
   ```

2. **Ensure thread safety** with proper locking
3. **Add comprehensive tests**
4. **Update factory function** in `get_rate_limiter()`
5. **Document the algorithm** with examples

### Adding New Backends

1. **Inherit from `BaseBackend`**:
   ```python
   class MyBackend(BaseBackend):
       def get(self, key):
           # Implementation
           pass
       # Implement all abstract methods
   ```

2. **Implement atomic operations**
3. **Handle connection errors gracefully**
4. **Add backend to factory function**
5. **Write backend-specific tests**

### Code Organization

- `algorithms.py`: Rate limiting algorithms
- `backends.py`: Storage backend implementations
- `decorators.py`: Django view decorators
- `middleware.py`: Django middleware
- `models.py`: Django database models
- `utils.py`: Utility functions
- `exceptions.py`: Custom exceptions

## 🎯 Areas for Contribution

### High Priority
- [ ] Additional rate limiting algorithms (leaky bucket, etc.)
- [ ] Performance optimizations
- [ ] Additional storage backends (Memcached, etc.)
- [ ] Better error handling and recovery
- [ ] Metrics and monitoring integration

### Medium Priority
- [ ] Django REST Framework integration
- [ ] Rate limiting analytics/reporting
- [ ] Custom rate limit violation handlers
- [ ] Configuration validation improvements
- [ ] More comprehensive examples

### Low Priority
- [ ] Web UI for rate limit management
- [ ] Integration with popular monitoring tools
- [ ] Rate limiting rules management API
- [ ] Advanced configuration options

## 📞 Getting Help

- **Documentation**: Check README.md and CONFIGURATION.md first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Code Review**: Maintainers will review PRs and provide feedback

## 🙏 Recognition

Contributors will be:
- Listed in the project's contributor list
- Mentioned in release notes for significant contributions
- Invited to join the maintainer team for ongoing contributors

Thank you for contributing to Django Rate Limiter! 🎉
