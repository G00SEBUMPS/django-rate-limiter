# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-07-29

### Fixed
- **BREAKING FIX**: Fixed `rate_limit_class` decorator failing with `AttributeError: 'SomeView' object has no attribute 'META'`
  - The decorator was incorrectly treating the `self` parameter as the `request` parameter in class-based views
  - Completely rewrote the decorator to properly handle class method signatures `(self, request, *args, **kwargs)`
  - Enhanced `get_user_identifier` to handle cases where `request.user` is `None`
  - Added proper null checks and improved error handling

### Added
- **NEW**: `rate_limit_method` decorator for rate limiting specific methods of a class
  - Allows targeting individual HTTP methods (e.g., only `POST`) instead of all methods
  - Clean syntax: `@rate_limit_method('post', limit=50, window=3600)`
  - Can be stacked for different limits on different methods
- Better code organization with extracted helper functions (`_create_rate_limited_method`, `_handle_rate_limiting`, `_create_error_response`)

### Changed
- Refactored `rate_limit_class` decorator for better maintainability and reduced cognitive complexity
- Improved closure handling to avoid variable capture issues in loops

## [1.0.1] - 2025-07-29
### Fixed
- Bump version to 1.0.1 in `pyproject.toml`
- Updated installation instructions in README and CONFIGURATION.md
- Added MANIFEST.in to include LICENSE and README files in the package

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

