<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Django Rate Limiter - Copilot Instructions

This is a Django rate limiter package with the following key characteristics:

## Project Structure
- **Core Package**: `django_rate_limiter/` - Main package code
- **Algorithms**: Multiple rate limiting algorithms (sliding window, token bucket, fixed window)
- **Backends**: Storage backends for memory, database, and Redis
- **Django Integration**: Decorators, middleware, models, and management commands
- **Tests**: Comprehensive test suite in `tests/` directory

## Code Style Guidelines
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Implement proper error handling with custom exceptions
- Ensure thread safety with proper locking mechanisms
- Write comprehensive docstrings for all public methods

## Key Features to Maintain
- **Thread Safety**: All operations must be atomic and thread-safe
- **Deadlock Prevention**: Use proper locking strategies to avoid deadlocks
- **Performance**: Optimize for high-throughput scenarios
- **Flexibility**: Support multiple algorithms and storage backends
- **Django Integration**: Follow Django best practices for apps, models, and middleware

## Testing Requirements
- Write unit tests for all core functionality
- Test thread safety with concurrent operations
- Test rate limiting accuracy under various scenarios
- Mock external dependencies (Redis, database) appropriately

## Architecture Principles
- Use dependency injection for backends
- Implement factory patterns for creating rate limiters
- Follow single responsibility principle for each class
- Use composition over inheritance where appropriate

When suggesting code changes or new features, ensure they:
1. Maintain backward compatibility
2. Follow the existing architecture patterns
3. Include appropriate tests
4. Are properly documented
5. Handle edge cases and errors gracefully
