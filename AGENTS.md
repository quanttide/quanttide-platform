# AGENTS.md - quanttide-platform

## Project Overview

QuantTide Platform (`qtapps`) is a monorepo containing architecture documentation (Jupyter Book) and multiple independent subprojects under `src/`. Each subproject is a self-contained monorepo with up to three modules: `provider` (Python/FastAPI backend), `cli` (Python/Typer CLI), and `studio` (Flutter/Dart frontend).

```
src/
  qtadmin/              # 量潮管理后台 - Admin platform (payroll → second-brain)
  qtcloud-data/         # 量潮数据云 - Dataset management service
  qtcloud-finance/      # 量潮财务云 - Beancount smart bookkeeping TUI
  qtcloud-think/        # 量潮思考云 - Thought collection & clarification
  qtcloud-read/         # 量潮阅读 (placeholder, no code yet)
  qtcloud-write/        # 量潮写作 (placeholder, no code yet)
```

## Build/Lint/Test Commands

All subprojects use **pytest** for Python testing and **flutter test** for Dart testing.

### Quick Reference

| Subproject | Module | Setup | Run All Tests | Run Single Test |
|------------|--------|-------|---------------|-----------------|
| qtadmin | provider | `cd src/provider && pdm install` | `pdm run pytest` | `pdm run pytest tests/test_file.py::test_func` |
| qtadmin | cli | `cd src/cli && uv sync` | `uv run pytest` | `uv run pytest tests/test_file.py` |
| qtcloud-data | provider | `cd src/provider && uv sync` | `uv run pytest -v` | `uv run pytest tests/test_file.py::test_func` |
| qtcloud-think | provider | `cd src/provider && uv sync` | `uv run pytest` | `uv run pytest tests/test_file.py::TestClass::test_method` |
| qtcloud-think | cli | `cd src/cli && uv sync` | `uv run pytest` | `uv run pytest tests/test_file.py -k "pattern"` |
| qtcloud-finance | cli | `cd src/cli && uv sync` | `uv run pytest tests/` | `uv run pytest tests/test_file.py::test_func` |
| Any | studio | `cd src/studio && flutter pub get` | `flutter test` | `flutter test test/widget_test.dart` |

### Lint & Format

```bash
# Ruff (recommended for all Python modules)
ruff check . --fix
ruff format .

# Black + isort (qtcloud-think convention)
black .
isort .

# Mypy
mypy src/

# Pre-commit (if configured)
pre-commit run --all-files

# Flutter/Dart
flutter analyze
dart format .
```

## Code Style Guidelines

### Python

**Naming**: Files `snake_case.py`. Classes `PascalCase`. Functions/variables `snake_case`. Constants `UPPER_SNAKE_CASE`. Boolean prefixes: `is_`, `has_`, `can_`, `should_`.

**Imports** (3 groups, separated by blank lines):
```python
# 1. stdlib
import os
from typing import List, Optional, TYPE_CHECKING

# 2. third-party
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

# 3. local (absolute imports preferred)
from app.models.employee import Employee
from app.database import get_session
```

**Type Hints**: Always annotate function params and returns. Use `TYPE_CHECKING` for circular import avoidance:
```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.salary import Salary
```

**Python version varies**: qtadmin >=3.10, qtcloud-think >=3.11, qtcloud-finance >=3.12, qtcloud-data >=3.9. Match style to target version.

**Line length**: 100 characters (Black/Ruff config).

**Docstrings/comments**: Use Chinese (项目惯例).

### FastAPI Providers

Follow the Base/Create/Read pattern for SQLModel models:
```python
class ItemBase(SQLModel):
    name: str

class Item(ItemBase, table=True):
    id: int = Field(default=None, primary_key=True)

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
```

**Routes**: Plural nouns (`/items`). Proper HTTP methods. `HTTPException` with Chinese detail messages for errors.

**DB sessions**: Use `Depends(get_session)`. Always `session.commit()` after writes, then `session.refresh()`.

### Testing

- Use `pytest` with `TestClient` for API tests
- Use `unittest.mock.patch` for mocking external services (LLM APIs, etc.)
- Use `conftest.py` for shared fixtures
- Place tests in `tests/` mirroring app structure
- Coverage: `pytest --cov=app --cov-report=html`

### Flutter/Dart

Follow standard Flutter conventions. Linting via `analysis_options.yaml` with `flutter_lints`.

## Versioning & Release

- **SemVer**: `v{major}.{minor}.{patch}`
- **Phase conventions**: Exploration (0.0.x) → Validation (0.x.y) → Release (x.y.z)
- **Monorepo tags**: `{module}/v{version}` (e.g., `provider/v0.0.1`, `cli/v0.0.1`)
- **Changelog**: [Keep a Changelog](https://keepachangelog.com/) format in each module's `CHANGELOG.md`
- **Commits**: Conventional Commits `type(scope): description` (e.g., `feat(provider): add salary calc`)

## Key Dependencies

| Category | Packages |
|----------|----------|
| Web Framework | FastAPI |
| ORM | SQLModel (qtadmin), SQLAlchemy (qtcloud-data) |
| CLI | Typer |
| LLM | OpenAI SDK |
| Testing | pytest, httpx, pytest-asyncio |
| Frontend | Flutter/Dart |
| Package Mgr | uv (qtcloud-*), PDM (qtadmin provider) |

## Environment

- `.env` files for secrets (never commit). `.env.example` for templates.
- Alibaba Cloud PyPI mirror used for some projects.
