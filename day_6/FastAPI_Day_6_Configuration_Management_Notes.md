# FastAPI Day 6 — Configuration Management with Pydantic Settings

## 1. Day 6 Overview

Day 6 focuses on **Configuration Management with Pydantic Settings**.

### Topics covered

- Configuration management
- Environment variables
- `.env`
- `os.getenv()` and the generic approach
- `pydantic-settings`
- `BaseSettings`
- `SettingsConfigDict`
- Typed configuration
- Automatic type conversion
- Environment-variable type checking
- Required configuration validation
- Centralized settings
- FastAPI integration
- Secrets masking with `SecretStr`
- Explicit secret access with `get_secret_value()`
- Development / Test-QA / Production configuration
- Staging terminology and environment-based configuration

---

# 2. Why Configuration Management Is Needed

Configuration contains values that control how an application runs.

Our current application configuration is:

```text
APP_NAME
APP_VERSION
APP_DEBUG
HOST
PORT
ENVIRONMENT
SECRET_KEY
```

A beginner might hard-code values:

```python
app = FastAPI(
    title="FastAPI practice application",
    version="0.1.0",
    debug=True
)
```

This becomes inconvenient when the same application runs in different environments.

For example:

```text
Development → PORT=8000, DEBUG=True
Test/QA     → PORT=8001, DEBUG=False
Production  → PORT=8000, DEBUG=False
```

We want the application code to remain the same while configuration changes.

The basic architecture is:

```text
Same application code
        |
        +---- Development configuration
        |
        +---- Test/QA configuration
        |
        +---- Production configuration
```

---

# 3. Environment Variables

An environment variable is a configuration value supplied to an application by its execution environment.

Examples:

```text
PORT=8000
APP_DEBUG=True
ENVIRONMENT=development
```

Environment variables are commonly used for:

- Application configuration
- Host and port
- Debug settings
- Environment names
- API keys
- Secret keys
- Database configuration

The main benefit is that environment-dependent values do not need to be hard-coded into Python source code.

---

# 4. The `.env` File

For local development, environment variables can be stored in a `.env` file.

Current project:

```text
day_6/
├── .env
├── main.py
├── config/
│   └── settings.py
└── venv/
```

Current `.env`:

```env
APP_NAME=FastAPI practice application
APP_VERSION=0.1.0
APP_DEBUG=True
HOST=127.0.0.1
ENVIRONMENT=development
PORT=8000
SECRET_KEY=my-super-secret-key
```

`.env` is configuration, not Python code.

---

# 5. Generic `os.getenv()` Approach

Before Pydantic Settings, we learned the generic/manual approach:

```python
from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")
PORT = os.getenv("PORT")
HOST = os.getenv("HOST")
APP_DEBUG = os.getenv("APP_DEBUG")
ENVIRONMENT = os.getenv("ENVIRONMENT")

print(f"APP_NAME: {APP_NAME}")
print(f"APP_VERSION: {APP_VERSION}")
print(f"PORT: {PORT}")
print(f"HOST: {HOST}")
print(f"APP_DEBUG: {APP_DEBUG}")
print(f"ENVIRONMENT: {ENVIRONMENT}")
```

## `load_dotenv()`

Python does not automatically read a `.env` file just because it exists.

`load_dotenv()` loads values from `.env` so that environment access such as:

```python
os.getenv("PORT")
```

can retrieve them.

## Problem with the generic approach

With `os.getenv()` we have to manually manage:

- Reading each variable
- Type conversion
- Missing values
- Validation
- Organization
- Sensitive values

For example, if a port must be an integer, we may need:

```python
PORT = int(os.getenv("PORT"))
```

As applications grow, manual configuration management becomes harder.

---

# 6. `pydantic-settings`

For Pydantic v2, configuration management is provided by:

```text
pydantic-settings
```

Install it with:

```powershell
pip install pydantic-settings
```

It provides:

```python
BaseSettings
```

which allows configuration to be defined as a typed settings model.

---

# 7. `BaseSettings`

Instead of manually reading:

```python
PORT = os.getenv("PORT")
```

we define:

```python
port: int
```

inside a `BaseSettings` model.

Conceptually:

```text
.env / Environment
       ↓
Pydantic Settings
       ↓
Type conversion
       ↓
Validation
       ↓
Settings object
       ↓
FastAPI application
```

---

# 8. Current `config/settings.py`

Our current implementation is:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    app_name: str
    app_version: str
    port: int
    host: str
    app_debug: bool
    environment: str
    secret_key: SecretStr


settings = Settings()

print(settings.app_name)
print(settings.app_version)
print(settings.port)
print(settings.host)
print(settings.app_debug)
print(settings.environment)
print(settings.secret_key)
```

---

# 9. Line-by-Line Explanation

## Import `BaseSettings`

```python
from pydantic_settings import BaseSettings
```

`BaseSettings` is used to create the configuration model.

```python
class Settings(BaseSettings):
```

This means the `Settings` class represents application configuration.

## Import `SettingsConfigDict`

```python
from pydantic_settings import SettingsConfigDict
```

This is used to configure how the settings model loads its values.

## Import `SecretStr`

```python
from pydantic import SecretStr
```

Important:

`SecretStr` comes from **Pydantic**, not `pydantic-settings`.

---

# 10. Configuring `.env`

```python
model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8"
)
```

### `env_file`

```python
env_file=".env"
```

tells Pydantic Settings to read the `.env` file.

### `env_file_encoding`

```python
env_file_encoding="utf-8"
```

specifies the encoding used to read the file.

---

# 11. Typed Settings

We define:

```python
app_name: str
app_version: str
port: int
host: str
app_debug: bool
environment: str
secret_key: SecretStr
```

Each configuration value has a declared type.

For example:

```python
port: int
```

means the port must be an integer.

```python
app_debug: bool
```

means debug must be Boolean-compatible.

```python
secret_key: SecretStr
```

means the sensitive value uses Pydantic's secret-aware string type.

---

# 12. Lowercase Python Fields and Uppercase Environment Variables

Python:

```python
app_name
app_version
app_debug
environment
secret_key
```

`.env`:

```env
APP_NAME
APP_VERSION
APP_DEBUG
ENVIRONMENT
SECRET_KEY
```

Pydantic Settings matches these names case-insensitively by default.

Conceptually:

```text
APP_NAME      → app_name
APP_VERSION   → app_version
APP_DEBUG     → app_debug
HOST          → host
PORT          → port
ENVIRONMENT   → environment
SECRET_KEY    → secret_key
```

This lets us follow normal Python naming conventions while using conventional uppercase environment-variable names.

---

# 13. Creating the Settings Object

```python
settings = Settings()
```

This is where configuration is loaded and validated.

Conceptually:

```text
Settings()
   ↓
Read environment variables / .env
   ↓
Match fields
   ↓
Convert types
   ↓
Validate
   ↓
Create settings object
```

We can then access:

```python
settings.app_name
settings.app_version
settings.port
settings.host
settings.app_debug
settings.environment
settings.secret_key
```

---

# 14. Automatic Type Conversion

Our `.env` contains:

```env
PORT=8000
```

Environment variables are text values, but our settings model says:

```python
port: int
```

Pydantic Settings converts the value into the required Python type.

Conceptually:

```text
"8000"
   ↓
Pydantic Settings
   ↓
8000
```

Likewise:

```env
APP_DEBUG=True
```

is interpreted according to:

```python
app_debug: bool
```

---

# 15. Environment-Variable Type Checking

We tested this deliberately.

We changed:

```env
PORT=8000
```

to:

```env
PORT=hello
```

while keeping:

```python
port: int
```

Running:

```powershell
python config/settings.py
```

produced a Pydantic validation error:

```text
ValidationError: 1 validation error for Settings

port
  Input should be a valid integer, unable to parse string as an integer
```

This is expected.

The configuration is invalid because:

```text
"hello"
```

cannot become:

```text
int
```

Pydantic therefore prevents the `Settings` object from being created successfully.

After the experiment, `PORT` was restored to:

```env
PORT=8000
```

This demonstrates an important professional principle:

```text
Invalid configuration
        ↓
ValidationError
        ↓
Application does not start with bad configuration
```

---

# 16. Required Configuration

Our settings fields have no default values:

```python
port: int
secret_key: SecretStr
```

Therefore they are required.

For example:

```python
secret_key: SecretStr
```

requires:

```env
SECRET_KEY=my-super-secret-key
```

If the value is missing, Pydantic reports:

```text
secret_key
Field required
```

This is useful because an application can detect missing configuration immediately rather than failing later.

---

# 17. Centralized Configuration

Instead of scattering configuration:

```python
# file A
PORT = 8000

# file B
DEBUG = True

# file C
HOST = "127.0.0.1"
```

we have one centralized settings object:

```python
settings = Settings()
```

Then any application component that needs configuration can use:

```python
settings.port
settings.host
settings.app_debug
settings.environment
```

Architecture:

```text
             .env / Environment
                     ↓
                 Settings
                     ↓
            Central configuration
                     ↓
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       main.py    routers    services
```

---

# 18. FastAPI Integration

Our current `main.py` uses:

```python
from config.settings import settings
```

and:

```python
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.app_debug
)
```

The complete current integration is:

```python
from fastapi import FastAPI, HTTPException, Request

from login import router as login_router
from config.settings import settings
from routers.products import router as product_router
from routers.orders import router as order_router
from Middleware.middleware import Http_middleware
from Exception_handler.exception_handler import (
    global_http_exception_handler,
    global_general_exception_handler
)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.app_debug
)


@app.middleware("http")
async def Application_middleware(request: Request, call_next):
    return await Http_middleware(request, call_next)


app.add_exception_handler(
    HTTPException,
    global_http_exception_handler
)

app.add_exception_handler(
    Exception,
    global_general_exception_handler
)


app.include_router(
    product_router,
    prefix="/products",
    tags=["products"]
)

app.include_router(
    order_router,
    prefix="/orders",
    tags=["orders"]
)

app.include_router(
    login_router,
    prefix="/login",
    tags=["login"]
)
```

The existing middleware, exception handlers, and routers remain unchanged.

---

# 19. Configuration Flow into FastAPI

```text
.env
 │
 ├── APP_NAME
 ├── APP_VERSION
 ├── APP_DEBUG
 ├── HOST
 ├── PORT
 ├── ENVIRONMENT
 └── SECRET_KEY
       │
       ↓
Settings()
       │
       ↓
settings object
       │
       ↓
main.py
       │
       ↓
FastAPI(...)
```

This separates configuration from application logic.

---

# 20. Secrets Masking

Some configuration values can be sensitive.

Examples in real applications include:

```text
SECRET_KEY
DATABASE_PASSWORD
API_KEY
TOKEN_SECRET
```

Our current project does not have a database or external API, so we use:

```text
SECRET_KEY
```

only to demonstrate secret handling.

---

# 21. `SecretStr`

Import:

```python
from pydantic import SecretStr
```

Define:

```python
secret_key: SecretStr
```

`.env`:

```env
SECRET_KEY=my-super-secret-key
```

Then:

```python
print(settings.secret_key)
```

produces:

```text
**********
```

Our actual test produced:

```text
FastAPI practice application
0.1.0
8000
127.0.0.1
True
development
**********
```

---

# 22. `SecretStr` Does Not Encrypt

This is important.

`SecretStr` is **not encryption**.

It does not turn:

```text
my-super-secret-key
```

into an encrypted value.

Its purpose is to prevent casual exposure through its representation.

Think:

```text
Actual secret
     ↓
SecretStr
     ↓
Printed representation
     ↓
**********
```

The raw value still exists in memory.

---

# 23. Getting the Raw Secret

If the application genuinely needs the raw secret:

```python
settings.secret_key.get_secret_value()
```

Example:

```python
secret = settings.secret_key.get_secret_value()
```

Now `secret` contains:

```text
my-super-secret-key
```

This should be done deliberately.

---

# 24. Why Secret Masking Matters

Secrets can accidentally appear in:

- Terminal output
- Logs
- Debug output
- Error reports
- Configuration dumps
- Screenshots
- Monitoring systems

`SecretStr` helps reduce accidental exposure when the value is represented or printed.

In production, sensitive values should also be supplied through appropriate environment/secret-management mechanisms and should not be committed to source control.

---

# 25. Environment-Based Configuration

The same application can run in different environments.

A simplified flow is:

```text
Development
      ↓
Test / QA
      ↓
Staging / Pre-production
      ↓
Production
```

Not every organization uses exactly this pipeline.

For our Day 6 roadmap, the main environments discussed are:

```text
development
test
production
```

The central principle is:

> Keep application code stable while environment-specific configuration changes.

---

# 26. Development Environment

Development is typically where developers work locally.

Example:

```env
APP_DEBUG=True
HOST=127.0.0.1
PORT=8000
ENVIRONMENT=development
```

Meaning:

```text
Environment → development
Debug       → enabled
Host        → local machine
Port        → 8000
```

A typical local command can be:

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The exact command depends on the project structure and deployment setup.

---

# 27. Test / QA Environment

A Test/QA environment separates testing from ordinary development.

Example:

```env
APP_DEBUG=False
HOST=127.0.0.1
PORT=8001
ENVIRONMENT=test
```

Conceptually:

```text
Development:
DEBUG=True
PORT=8000

Test/QA:
DEBUG=False
PORT=8001
```

These are example values. A real organization may use completely different ports or infrastructure.

The important concept is the separation of configuration.

---

# 28. Production Environment

Production is where the real application is served.

Example:

```env
APP_DEBUG=False
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
```

Debug should normally be disabled in production.

For the host:

```text
127.0.0.1
```

generally means listening only on the local machine/interface.

```text
0.0.0.0
```

commonly means listening on available network interfaces.

The exact production setup depends on the hosting platform, reverse proxy, container, network, and infrastructure.

---

# 29. Development vs Test vs Production

| Configuration | Development | Test/QA | Production |
|---|---|---|---|
| `ENVIRONMENT` | `development` | `test` | `production` |
| `APP_DEBUG` | `True` | `False` | `False` |
| `HOST` | `127.0.0.1` | `127.0.0.1` | commonly `0.0.0.0` |
| `PORT` | `8000` | `8001` | `8000` example |

These values are examples, not universal company standards.

---

# 30. Is Changing `ENVIRONMENT` and `APP_DEBUG` Alone Staging?

No.

They are configuration values used to identify and configure an environment.

For example:

```env
ENVIRONMENT=development
```

identifies the current environment as development.

Other configuration values can then differ:

```text
PORT
HOST
APP_DEBUG
```

Environment-based configuration means:

```text
                 SAME CODE
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
   Development     Test     Production
        │           │           │
        ↓           ↓           ↓
     config       config       config
```

---

# 31. What Is Staging Specifically?

In many professional development pipelines, **staging** means a pre-production environment.

A common flow is:

```text
Development
      ↓
Test / QA
      ↓
Staging
      ↓
Production
```

Typical meaning:

### Development

Developers build and change features.

### Test / QA

The application is tested.

### Staging

The application is tested in an environment designed to be close to production.

### Production

The application serves real users.

However, exact environment names and deployment pipelines vary between organizations.

The important Day 6 lesson is environment-based configuration.

---

# 32. Do We Need to Configure All Environments Now?

No.

Our current project is being developed locally.

Therefore the current `.env` can remain:

```env
APP_NAME=FastAPI practice application
APP_VERSION=0.1.0
APP_DEBUG=True
HOST=127.0.0.1
ENVIRONMENT=development
PORT=8000
SECRET_KEY=my-super-secret-key
```

We do not need to create an actual QA or production server for this learning exercise.

We are learning the architecture now.

Later, deployment environments can provide their own configuration.

---

# 33. We Normally Do Not Change Python Code When the Environment Changes

Avoid scattering environment-specific code like:

```python
if developer:
    port = 8000

if qa:
    port = 8001

if production:
    port = 8000
```

Instead:

```text
Environment
    ↓
Settings
    ↓
Application
```

The application consumes:

```python
settings.port
settings.host
settings.environment
settings.app_debug
```

---

# 34. `.env` vs Real Deployment

For local development:

```text
.env
```

is convenient.

In real deployments, configuration may be supplied through:

- Environment variables
- Container environment configuration
- Hosting-platform settings
- CI/CD systems
- Secret-management systems

Therefore, the application should be written to consume configuration rather than depending on manually editing a local `.env` file for every environment.

---

# 35. Complete Current `.env`

```env
APP_NAME=FastAPI practice application
APP_VERSION=0.1.0
APP_DEBUG=True
HOST=127.0.0.1
ENVIRONMENT=development
PORT=8000
SECRET_KEY=my-super-secret-key
```

---

# 36. Complete Current `config/settings.py`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    app_name: str
    app_version: str
    port: int
    host: str
    app_debug: bool
    environment: str
    secret_key: SecretStr


settings = Settings()

print(settings.app_name)
print(settings.app_version)
print(settings.port)
print(settings.host)
print(settings.app_debug)
print(settings.environment)
print(settings.secret_key)
```

---

# 37. Expected Settings Output

Run:

```powershell
python config/settings.py
```

Expected:

```text
FastAPI practice application
0.1.0
8000
127.0.0.1
True
development
**********
```

---

# 38. Experiments Completed

## Experiment 1 — Normal configuration

```env
PORT=8000
```

Result:

```text
8000
```

## Experiment 2 — Invalid type

```env
PORT=hello
```

with:

```python
port: int
```

Result:

```text
ValidationError
```

This demonstrated environment-variable type validation.

## Experiment 3 — Missing required secret

Without:

```env
SECRET_KEY=...
```

the settings model reported:

```text
secret_key
Field required
```

This demonstrated required configuration.

## Experiment 4 — Secret masking

With:

```python
secret_key: SecretStr
```

printing:

```python
settings.secret_key
```

produced:

```text
**********
```

## Experiment 5 — Environment configuration

We studied how values can differ between:

```text
development
test
production
```

while the application code remains the same.

---

# 39. Common Errors We Encountered

## Error 1 — Wrong `SecretStr` import

Incorrect:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict, SecretStr
```

Correct:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
```

Reason:

```text
BaseSettings       → pydantic-settings
SettingsConfigDict → pydantic-settings
SecretStr          → pydantic
```

---

## Error 2 — Missing `SECRET_KEY`

We defined:

```python
secret_key: SecretStr
```

but did not provide:

```env
SECRET_KEY=...
```

Pydantic correctly reported:

```text
Field required
```

The solution was:

```env
SECRET_KEY=my-super-secret-key
```

---

## Error 3 — Invalid `PORT`

We tested:

```env
PORT=hello
```

while requiring:

```python
port: int
```

Pydantic correctly rejected the configuration.

---

# 40. Professional Lessons From Day 6

### 1. Configuration is not business logic

```text
Business logic → how the application behaves

Configuration → how/where the application runs
```

### 2. Centralize configuration

Use:

```python
settings = Settings()
```

instead of scattering configuration.

### 3. Prefer typed configuration

Use:

```python
port: int
```

instead of manually handling everything with strings.

### 4. Validate configuration early

Bad configuration should be detected during startup.

### 5. Required settings should be explicit

If a value is essential, do not silently allow it to be missing.

### 6. Protect sensitive values

Use:

```python
SecretStr
```

for secret-string representation.

### 7. Secret masking is not encryption

`SecretStr` reduces accidental exposure but does not encrypt the secret.

### 8. Keep environment-specific configuration outside application logic

The same application code can run with different configuration.

---

# 41. Day 6 Architecture

```text
                  .env / Environment Variables
                              │
                              ↓
                    ┌───────────────────┐
                    │     Settings      │
                    │   BaseSettings    │
                    └─────────┬─────────┘
                              │
                   Type conversion
                   + validation
                   + secret handling
                              │
                              ↓
                    ┌───────────────────┐
                    │     settings      │
                    │      object       │
                    └─────────┬─────────┘
                              │
                              ↓
                         FastAPI app
                              │
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
           Routers         Middleware      Exceptions
```

---

# 42. Day 6 Mental Model

Remember:

```text
WHERE?
   ↓
Environment variables / .env

HOW?
   ↓
Pydantic Settings

WHAT?
   ↓
Typed configuration fields

CHECK?
   ↓
Pydantic validation

PROTECT?
   ↓
SecretStr

CENTRALIZE?
   ↓
settings object

USE?
   ↓
FastAPI application
```

---

# 43. Day 6 Final Checklist

- [x] Understand configuration
- [x] Understand environment variables
- [x] Understand `.env`
- [x] Learn the generic `os.getenv()` approach
- [x] Understand why manual configuration becomes difficult
- [x] Use `pydantic-settings`
- [x] Understand `BaseSettings`
- [x] Understand `SettingsConfigDict`
- [x] Load `.env`
- [x] Use lowercase Python setting names
- [x] Understand uppercase environment-variable mapping
- [x] Use typed settings
- [x] Understand automatic type conversion
- [x] Test invalid environment-variable types
- [x] Understand required configuration
- [x] Test missing required configuration
- [x] Create a centralized `settings` object
- [x] Integrate settings with FastAPI
- [x] Understand sensitive configuration
- [x] Use `SecretStr`
- [x] Understand masking
- [x] Understand `get_secret_value()`
- [x] Understand that masking is not encryption
- [x] Understand development configuration
- [x] Understand test/QA configuration
- [x] Understand production configuration
- [x] Understand staging terminology
- [x] Understand environment-based configuration
- [x] Understand that code can remain the same while environment configuration changes

---

# 44. Day 6 Completion

## DAY 6 — COMPLETE ✅

The core principle learned today is:

> **Application code should describe how the application works, while configuration should describe the environment in which the application runs.**

Our implementation follows:

```text
Environment / .env
        ↓
Pydantic Settings
        ↓
Type conversion + validation
        ↓
Secret handling
        ↓
Centralized settings object
        ↓
FastAPI
```

We intentionally did **not** add database, Redis, authentication infrastructure, external APIs, or other unrelated configuration because they are not required for the current Day 6 roadmap topic.

The configuration foundation is now ready for later FastAPI development.

**DAY 6 COMPLETE ✅**
