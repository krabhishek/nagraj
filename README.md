# Nagraj

[![Tests](https://github.com/krabhishek/nagraj/actions/workflows/test.yml/badge.svg)](https://github.com/krabhishek/nagraj/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/nagraj.svg)](https://badge.fury.io/py/nagraj)
[![codecov](https://codecov.io/gh/krabhishek/nagraj/branch/main/graph/badge.svg)](https://codecov.io/gh/krabhishek/nagraj)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/nagraj.svg)](https://pypi.org/project/nagraj/)

Nagraj is a powerful CLI tool for generating Domain-Driven Design (DDD) and Command Query Responsibility Segregation (CQRS) based microservices applications in Python. It provides a robust project structure with best practices baked in.

## Features

- 🏗️ **DDD Architecture**: Built-in support for DDD patterns including:
  - Aggregates, Entities, Value Objects
  - Domain Events and Event Handlers
  - Repositories and Specifications
  - Domain Services and Facades

- 🔄 **CQRS Pattern**: Clear separation of commands and queries with:
  - Command handlers and validators
  - Query handlers and DTOs
  - Event sourcing support

- 🔒 **Authentication & Authorization**: Pre-configured auth bounded context with:
  - JWT-based authentication
  - Role-based authorization
  - Password hashing with Argon2
  - User management APIs

- 🛠️ **Modern Tech Stack**:
  - FastAPI for high-performance APIs
  - SQLModel for type-safe ORM
  - Pydantic for data validation
  - Alembic for database migrations
  - Poetry for dependency management

- 🧪 **Testing & Quality**:
  - Pytest configuration with async support
  - Hurl for API testing
  - Coverage reporting
  - Ruff for linting and formatting

## Installation

```bash
pip install nagraj
```

## Quick Start

1. Create a new project:
```bash
nagraj init --project-name my_cool_app
```

2. Additional options:
```bash
nagraj init \
  --project-name my_cool_app \
  --project-description "My awesome microservice" \
  --project-author-name "John Doe" \
  --project-author-email "john@example.com" \
  --python-version 3.12 \
  --version 0.1.0
```

## Project Structure

The generated project follows a clean DDD/CQRS architecture:

```
my_cool_app/
├── my_cool_app/
│   ├── common/
│   │   ├── base/              # Base classes for DDD building blocks
│   │   ├── bounded_contexts/  # Shared bounded contexts (e.g., auth)
│   │   ├── core/             # Core functionality
│   │   └── exceptions/       # Exception hierarchy
│   └── example_domain_one/   # Domain-specific code
│       ├── bounded_contexts/ # Domain bounded contexts
│       ├── context_maps/    # Context mapping
│       └── interface/       # Domain interfaces
├── tests/
│   ├── unit/
│   ├── integration/
│   └── apis/               # API tests using Hurl
├── alembic.ini            # Database migration config
├── pyproject.toml         # Project dependencies
└── .nagraj.yaml          # Project configuration
```

## Configuration

The `.nagraj.yaml` file in your project root contains the complete configuration:

- Project metadata and versioning
- Base class configurations
- Infrastructure settings
- Common components
- Domain configurations
- Testing setup
- Development tools

## Development Workflow

1. **Add a New Domain**:
   - Create domain folder structure
   - Define bounded contexts
   - Implement domain models
   - Add API interfaces

2. **Testing**:
   ```bash
   # Run all tests
   pytest

   # Run API tests
   hurl tests/apis/*.hurl
   ```

3. **Database Migrations**:
   ```bash
   # Create a new migration
   alembic revision --autogenerate -m "description"

   # Apply migrations
   alembic upgrade head
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Created and maintained by Abhishek Pathak (@krabhishek)
