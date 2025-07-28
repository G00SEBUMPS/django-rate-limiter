# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-11

### Added
- Initial release of Django Rate Limiter
- Multiple rate limiting algorithms:
  - Sliding Window (precise timestamp-based)
  - Token Bucket (burst-friendly with steady refill)
  - Fixed Window (simple counter-based)
  - Sliding Window Counter (approximated sliding window)
- Multiple storage backends:
  - Memory Backend (fast, single-process)
  - Database Backend (persistent, Django ORM)
  - Redis Backend (distributed, high-performance)
- Thread-safe and deadlock-safe implementation
- Comprehensive Django integration:
  - Decorators (`@rate_limit`, `@throttle`, `@per_user_rate_limit`, etc.)
  - Middleware for automatic rate limiting
  - Django models and migrations
  - Management commands for cleanup
- Flexible configuration options:
  - Per-endpoint rate limiting
  - Per-user and per-IP rate limiting
  - Custom key functions
  - Environment-specific settings
- Complete test suite with 16+ test cases
- Comprehensive documentation and examples
- GitHub Actions CI/CD pipeline
- Support for Python 3.8+ and Django 3.2+

### Features
- **Thread Safety**: All operations are atomic and thread-safe
- **Deadlock Prevention**: Proper locking strategies prevent deadlocks
- **High Performance**: Optimized for high-throughput scenarios
- **Scalability**: Redis backend supports distributed rate limiting
- **Flexibility**: Multiple algorithms and storage options
- **Django Native**: Follows Django best practices and conventions

### Documentation
- Complete README with quick start guide
- Detailed configuration documentation (CONFIGURATION.md)
- Development setup guide (DEVELOPMENT.md)
- Working code examples and demo scripts
- API documentation with type hints

### Testing
- Comprehensive test suite covering all algorithms
- Thread safety tests with concurrent operations
- Backend-specific tests for memory, database, and Redis
- Rate limiting accuracy tests under various scenarios
- GitHub Actions workflow for automated testing

## [1.0.1] - 2025-07-29
### Fixed
- Bump version to 1.0.1 in `pyproject.toml`
- Updated installation instructions in README and CONFIGURATION.md
- Added MANIFEST.in to include LICENSE and README files in the package