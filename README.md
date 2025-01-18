# **Table of Contents**

1. [Overview](#overview)
2. [DDD Coding Standard Summary](#ddd-coding-standard-summary)
   1. [Architecture Principles](#architecture-principles)
   2. [Folder & Module Structure](#folder--module-structure)
   3. [Domains, Sub-Domains, and Bounded Contexts](#domains-sub-domains-and-bounded-contexts)
   4. [Hexagonal Architecture (Ports & Adapters)](#hexagonal-architecture-ports--adapters)
   5. [CQRS (Command and Query Responsibility Segregation)](#cqrs-command-and-query-responsibility-segregation)
   6. [DTOs (Data Transfer Objects)](#dtos-data-transfer-objects)
   7. [Services, Repositories, and Adapters](#services-repositories-and-adapters)
   8. [Base Classes & Global Reusables](#base-classes--global-reusables)
   9. [Naming Conventions](#naming-conventions)
   10. [Anti-Corruption Layer (ACL)](#anti-corruption-layer-acl)
   11. [Shared Cross-Cutting Concerns](#shared-cross-cutting-concerns)
3. [Nagraj CLI Tool Requirements](#nagraj-cli-tool-requirements)
   1. [Core CLI Commands](#core-cli-commands)
   2. [Generated Artifacts & File Structures](#generated-artifacts--file-structures)
   3. [Configuration & Extensibility](#configuration--extensibility)
4. [Linter Integration (Extended Ruff)](#linter-integration-extended-ruff)
   1. [Linting Rules](#linting-rules)
   2. [Scaffolded Project Checks](#scaffolded-project-checks)
5. [Illustrative Directory Example](#illustrative-directory-example)
6. [Rationale & Best Practices](#rationale--best-practices)

---

## **1. Overview**

**Nagraj** is a **command-line tool** that automates creation of Python projects conforming to **DDD + Hexagonal + CQRS** architecture. In this **revised** standard:

- **Each domain** is **self-contained** and can be deployed as a **microservice**.
- **APIs** (FastAPI controllers, routes, schemas) reside **within** each domain’s `interfaces/` folder instead of a global `interfaces/` folder.
- **Shared** concerns (like **authentication**, **logging**, **monitoring**) go under `src/shared/<concern>/`.

### **Key Goals**

1. **Consistency**: All projects share the **same** folder structure, naming conventions, and code layout.
2. **Independent Deployability**: Each domain can stand alone as a microservice, with its own **API interfaces** and **infrastructure**.
3. **Domain-Driven Design (DDD)**: The domain remains **pure**, with distinct **bounded contexts** and minimal coupling to technical frameworks.
4. **Hexagonal Architecture**: Strict separation of **ports** and **adapters**.
5. **CQRS**: Clear distinction between **commands** and **queries**.
6. **Shared Concerns**: Are placed under `src/shared/` for cross-domain usage (e.g., authentication, security, logging).

---

## **2. DDD Coding Standard Summary**

### **2.1 Architecture Principles**

1. **Domain-Driven Design (DDD)**

   - Emphasize **Entities**, **Value Objects**, **Aggregates**, **Domain Events**, and **Bounded Contexts**.
   - Maintain a **ubiquitous language** within each bounded context.

2. **Hexagonal Architecture (Ports & Adapters)**

   - Keep domain logic isolated.
   - Expose interfaces through **ports**; implement them with **adapters** in the infrastructure layer.

3. **CQRS**

   - Commands modify domain state; queries read domain state.
   - Use additional complexity (e.g., event sourcing) only if domain demands it.

4. **Scream Architecture**

   - Immediate clarity on **where** code belongs and **why** it belongs there.

5. **Independent Microservices**
   - Each domain is **self-contained** (domain/application/infrastructure/interfaces).
   - Shared cross-cutting concerns are in `src/shared/` to avoid duplication and pollution.

---

### **2.2 Folder & Module Structure**

A **top-level** look at the revised structure:

```
src/
├── shared/                      # Cross-cutting concerns (e.g., authentication)
│   ├── auth/
│   ├── logging/
│   └── ...
├── domains/
│   └── <domain_name>/
│       ├── __init__.py
│       ├── <bounded_context_name>/
│       │   ├── __init__.py
│       │   ├── domain/
│       │   ├── application/
│       │   ├── infrastructure/
│       │   ├── interfaces/      # API layer for this bounded context (FastAPI routes, controllers, schemas)
│       │   └── ...
│       └── ...
├── config/                      # Application-level settings/config
├── main.py                      # Optional root aggregator if monolithic
└── tests/
```

Within **each bounded context**:

1. `domain/`

   - **Entities** (`entities/`), **Value Objects** (`value_objects/`), **Domain Events** (`domain_events/`), **Services** (`services/`), **Aggregates** (optional `aggregates/`), **Factories** (`factories/`).

2. `application/`

   - **Commands** (`commands/`), **Queries** (`queries/`), **DTOs** (`dto/`), **Services** (`services/`).

3. `infrastructure/`

   - **Adapters** (`adapters/`), **Repositories** (`repositories/`), **Migrations** (`migrations/`), **Anti-Corruption** logic (`anti_corruption/`).

4. `interfaces/`
   - **Routes** (e.g. `fastapi/routes/`),
   - **Controllers** (e.g. `fastapi/controllers/`),
   - **Schemas** (e.g. `fastapi/schemas/`).
   - This folder is the **API** boundary for that domain’s microservice.

**Important**:

- **No** top-level `interfaces/` folder at `src/`. Instead, each domain manages its own `interfaces/` for domain-specific endpoints.
- If you have a monolithic deployment, you can still host multiple domain-based interfaces in a single codebase. If you break them out as microservices, each domain has everything it needs (domain, application, infrastructure, interfaces) to run independently.

---

### **2.3 Domains, Sub-Domains, and Bounded Contexts**

1. **Domain**
   - Highest-level business area or microservice boundary. E.g., `orders`, `billing`.
2. **Bounded Context**
   - A cohesive part of the domain where a **specific ubiquitous language** applies.
3. **Independent Deployment**
   - Each domain folder can be packaged and deployed **on its own**, including the `interfaces/` layer (API endpoints), domain logic, and infrastructure.

---

### **2.4 Hexagonal Architecture (Ports & Adapters)**

- **Ports**
  - Defined in `domain/` or `application/` as abstract interfaces (e.g., `PaymentGatewayPort`).
- **Adapters**
  - Concrete implementations in `infrastructure/adapters/`.
  - Example: `StripePaymentAdapter` implementing `PaymentGatewayPort`.

---

### **2.5 CQRS (Command and Query Responsibility Segregation)**

1. **Commands**: In `application/commands/`, handled by dedicated **command handlers**.
2. **Queries**: In `application/queries/`, handled by **query handlers**.
3. **Optional** advanced CQRS patterns if domain complexity justifies it.

---

### **2.6 DTOs (Data Transfer Objects)**

1. **Application DTOs**

   - Internal to a bounded context (in `application/dto/`).
   - Commonly used for domain–application interactions.

2. **Interface DTOs**
   - For external or cross-context usage, typically placed in the `interfaces/fastapi/schemas/` folder.
   - Provide **anti-corruption** from external representation to domain objects.

---

### **2.7 Services, Repositories, and Adapters**

1. **Domain Services**
   - In `domain/services/`. Contains pure domain logic not belonging to a single entity.
2. **Application Services**
   - In `application/services/`. Orchestrates commands, queries, and domain interactions.
3. **Repositories**
   - **Interface** in `domain/` or `application/` (e.g., `UserRepository`).
   - **Implementation** in `infrastructure/repositories/` (e.g., `SqlUserRepository`).
4. **Adapters**
   - In `infrastructure/adapters/`, implementing external service interactions.

---

### **2.8 Base Classes & Global Reusables**

Keep **company-wide** base classes in `src/common/` or `src/shared/base/` (depending on preference). For instance:

- **BaseEntity** (`SQLModel` with shared fields)
- **BaseAggregateRoot**
- **BaseDomainEvent**, **BaseIntegrationEvent**
- **BaseCommand**, **BaseQuery**
- **BaseException** hierarchy
- **BaseRepository**, **BaseAdapter** (optional)

**Domain-Specific** base classes can live in `src/domains/<domain_name>/common/` if they apply only to that domain.

---

### **2.9 Naming Conventions**

- **Folders & Files**: `snake_case` (e.g., `create_order_command.py`).
- **Classes**: `PascalCase` (e.g., `CreateOrderCommand`).
- **Functions / Methods**: `snake_case`.
- **Variables / Attributes**: `snake_case`.
- **Prefixes / Suffixes**:
  - `UserEntity`, `AddressValueObject`, `UserRegisteredEvent`, `CreateUserCommand`, etc.

---

### **2.10 Anti-Corruption Layer (ACL)**

- Implemented in `infrastructure/anti_corruption/` or as part of an **adapter** if it includes mapping logic.
- Shields the domain from **external** or **legacy** data models.

---

### **2.11 Shared Cross-Cutting Concerns**

- Reside in `src/shared/<concern>/`. Examples:
  - **Auth**: `src/shared/auth/`
  - **Logging**: `src/shared/logging/`
  - **Monitoring**: `src/shared/monitoring/`
- This design prevents duplication across domains and keeps domain code pure.
- **Domains** can **import** from `src/shared/...` as needed without violating domain boundaries (since the code in `src/shared/` is _infrastructure or cross-cutting_ by design).

---

## **3. Nagraj CLI Tool Requirements**

Nagraj is a **command-line utility** to auto-generate domain-compliant code. It ensures each domain can **stand alone** with its own interface and infrastructure.

### **3.1 Core CLI Commands**

1. **`nagraj new <project_name>`**

   - Creates a new project with the baseline directories:
     - `src/` (containing `shared/`, `domains/`, `config/`, `tests/`),
     - `pyproject.toml` or `setup.cfg` with linter config.

2. **`nagraj add-domain <domain_name>`**

   - Generates `src/domains/<domain_name>/` with placeholders for subfolders: `common/`, `interfaces/`, `application/`, etc.

3. **`nagraj add-bc <domain_name> <bounded_context_name>`**

   - Creates the standard structure inside the domain (e.g., `domain/`, `application/`, `infrastructure/`, `interfaces/`).

4. **`nagraj add-entity <domain_name> <bounded_context_name> <entity_name>`**

   - Generates a file in `domain/entities/`, inheriting from `BaseEntity` or `BaseAggregateRoot`.

5. **`nagraj add-vo <domain_name> <bounded_context_name> <vo_name>`**

   - Generates a file in `domain/value_objects/`, inheriting from `BaseValueObject` (if used).

6. **`nagraj add-command <domain_name> <bounded_context_name> <command_name>`**

   - Creates a command + handler in `application/commands/`.

7. **`nagraj add-query <domain_name> <bounded_context_name> <query_name>`**

   - Creates a query + handler in `application/queries/`.

8. **`nagraj add-service <domain_name> <bounded_context_name> <service_scope>`**

   - Creates either a domain service or application service skeleton, depending on `service_scope`.

9. **`nagraj add-interface <domain_name> <bounded_context_name> <interface_name>`**
   - Sets up a route/controller/schema in `interfaces/fastapi/...`, ensuring the domain-based API structure is adhered to.

### **3.2 Generated Artifacts & File Structures**

- Each artifact will have docstring placeholders and correct inheritance from base classes in `src/shared/base/` or `src/common/`.
- `nagraj` ensures the code is placed in the **proper** folder with **correct** naming.

### **3.3 Configuration & Extensibility**

- **`.nagraj.toml`** or `.nagraj.yaml` can specify:
  - Default base classes, custom folder paths, or naming overrides.
- **Hooks** to add new scaffolding templates (e.g., “**add-acl**” for anti-corruption layer stubs).

---

## **4. Linter Integration (Extended Ruff)**

Nagraj’s scaffolding comes with an extended Ruff configuration to enforce DDD boundaries and naming rules.

### **4.1 Linting Rules**

1. **File & Folder Naming**
   - Must be `snake_case`.
   - No ambiguous folder names like `utils` or `helpers` in domain contexts.
2. **Location Enforcement**
   - Domain code **cannot** import from `infrastructure/`.
   - Each domain must contain its own `interfaces/` folder if it exposes an API.
3. **Class Names**
   - `PascalCase` with domain suffix or prefix (e.g., `OrderEntity`, `ShippingService`).
4. **Shared Code**
   - Must live under `src/shared/`; domain code must not replicate this.

### **4.2 Scaffolded Project Checks**

- After scaffolding, Nagraj runs Ruff in a “strict mode” to confirm compliance.
- Integration with git hooks or CI to ensure no merges happen unless checks pass.

---

## **5. Illustrative Directory Example**

Below is how the codebase might look after using Nagraj for a domain called `orders`, with bounded context `order_management`, plus a shared authentication module.

```
src/
├── shared/
│   ├── auth/
│   │   ├── jwt_service.py
│   │   └── base_auth_exception.py
│   ├── base/
│   │   ├── base_entity.py
│   │   ├── base_value_object.py
│   │   ├── base_aggregate_root.py
│   │   ├── base_domain_event.py
│   │   ├── base_command.py
│   │   ├── base_query.py
│   │   ├── base_exception.py
│   │   └── ...
│   └── logging/
│       └── logger.py
├── domains/
│   └── orders/
│       ├── order_management/
│       │   ├── domain/
│       │   │   ├── entities/
│       │   │   │   └── order_entity.py
│       │   │   ├── value_objects/
│       │   │   │   └── currency_value_object.py
│       │   │   ├── domain_events/
│       │   │   │   └── order_placed_event.py
│       │   │   ├── services/
│       │   │   │   └── order_domain_service.py
│       │   │   └── factories/
│       │   │       └── order_factory.py
│       │   ├── application/
│       │   │   ├── commands/
│       │   │   │   ├── create_order_command.py
│       │   │   │   └── create_order_command_handler.py
│       │   │   ├── queries/
│       │   │   │   ├── get_order_query.py
│       │   │   │   └── get_order_query_handler.py
│       │   │   ├── dto/
│       │   │   │   └── order_response_dto.py
│       │   │   └── services/
│       │   │       └── order_application_service.py
│       │   ├── infrastructure/
│       │   │   ├── adapters/
│       │   │   │   └── stripe_payment_adapter.py
│       │   │   ├── repositories/
│       │   │   │   └── order_repository.py
│       │   │   ├── migrations/
│       │   │   └── anti_corruption/
│       │   └── interfaces/
│       │       └── fastapi/
│       │           ├── routes/
│       │           │   └── order_routes.py
│       │           ├── controllers/
│       │           │   └── order_controller.py
│       │           └── schemas/
│       │               └── order_schemas.py
│       └── ...
├── config/
│   └── settings.py
└── tests/
    └── ...
```

With this layout:

- **`src/shared/`** handles cross-cutting concerns (auth, logging, etc.).
- **`src/domains/orders/order_management/interfaces/`** hosts the domain-specific API.
- If you deploy **`orders/order_management`** as a microservice, it has its own `interfaces/`, `application/`, `infrastructure/`, and `domain/` layers.

---

## **6. Rationale & Best Practices**

1. **Independent Deployability**
   - Ensuring each domain contains its **own interfaces** fosters microservice deployment autonomy.
2. **Shared Modules**
   - `src/shared/` prevents duplication of cross-cutting logic (e.g., auth, logging), but keeps domain code pure.
3. **Hexagonal Boundaries**
   - Strict separation between domain, application, infrastructure, and interfaces leads to maintainable code.
4. **Scream Architecture**
   - Folder and file names reveal their purpose at a glance.

---
