# Nagraj - Python DDD/CQRS Project Generator

Nagraj is a command-line tool that helps you create Python projects following Domain-Driven Design (DDD) and Command Query Responsibility Segregation (CQRS) patterns. Named after the famous Indian comic book superhero, Nagraj (the Snake King), this tool aims to make DDD project setup as powerful and elegant as its namesake.

## Installation

```bash
pip install nagraj
```

## Quick Start

Create a new project with default settings:

```bash
nagraj new my-project
```

This will create a new project with:

- A core domain and main bounded context
- Standard DDD/CQRS folder structure
- Base classes for entities, value objects, and domain events
- Project configuration in `.nagraj.yaml`

## Project Structure

When you create a new project, Nagraj generates the following structure:

```
my-project/
├── src/
│   ├── shared/
│   │   └── base/
│   │       ├── base_entity.py
│   │       ├── base_value_object.py
│   │       ├── base_aggregate_root.py
│   │       └── base_domain_event.py
│   └── domains/
│       └── core/
│           └── main/
│               ├── domain/
│               │   ├── entities/
│               │   ├── value_objects/
│               │   └── domain_events/
│               ├── application/
│               │   ├── commands/
│               │   └── queries/
│               ├── infrastructure/
│               │   ├── adapters/
│               │   └── repositories/
│               └── interfaces/
│                   └── fastapi/
│                       ├── routes/
│                       ├── controllers/
│                       └── schemas/
├── pyproject.toml
└── .nagraj.yaml
```

## Commands

### Create a New Project

```bash
nagraj new <project-name> [OPTIONS]

Options:
  -o, --output-dir PATH    Directory where the project will be created
  -d, --description TEXT   Project description
  -a, --author TEXT       Project author
  --domain TEXT           Initial domain name (defaults to 'core')
  --context TEXT          Initial bounded context name (defaults to 'main')
  --debug                 Enable debug output
  --no-art               Disable ASCII art display
  --help                 Show this message and exit
```

### Add a Domain

```bash
nagraj add domain <name> [OPTIONS]

Options:
  -p, --project-dir PATH  Project root directory
  --debug                Enable debug output
  --help                 Show this message and exit
```

### Add a Bounded Context

```bash
nagraj add bc <domain-name> <context-name> [OPTIONS]

Options:
  -p, --project-dir PATH  Project root directory
  --debug                Enable debug output
  --help                 Show this message and exit
```

### Remove a Domain

```bash
nagraj remove domain <name> [OPTIONS]

Options:
  -p, --project-dir PATH  Project root directory
  --debug                Enable debug output
  --help                 Show this message and exit
```

### Remove a Bounded Context

```bash
nagraj remove bc <domain-name> <context-name> [OPTIONS]

Options:
  -p, --project-dir PATH  Project root directory
  --debug                Enable debug output
  --help                 Show this message and exit
```

## Configuration

Nagraj uses a `.nagraj.yaml` file in your project root to store configuration:

```yaml
version: "1.0"
created_at: "2024-01-18T12:00:00Z"
updated_at: "2024-01-18T12:00:00Z"
name: "my-project"
description: "A DDD/CQRS project"
author: "Your Name"

# Base class configuration
base_classes:
  entity: "pydantic.BaseModel"
  aggregate_root: "pydantic.BaseModel"
  value_object: "pydantic.BaseModel"
  orm: "sqlmodel.SQLModel"

# Domains will be added here as they are created
domains: {}
```

## Development Status

Nagraj is currently in active development. The following features are implemented:

✅ Project creation with DDD structure  
✅ Domain management (add/remove)  
✅ Bounded context management (add/remove)  
✅ Base class generation  
✅ Project configuration

Coming soon:

- Entity and value object generation
- Command and query scaffolding
- Service generation
- Interface/API scaffolding
- Extended validation rules
- Custom template support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
