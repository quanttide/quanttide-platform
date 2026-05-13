---
name: product-provider
description: QTData product provider service built with FastAPI and uv
---

## What I do
- Provides product data APIs via FastAPI
- Manages provider service configurations and endpoints
- Integrates with the broader QTData platform

## When to use me
Use this skill when working on the `src/provider` service, including adding new API endpoints, modifying provider logic, or managing dependencies with uv.

## Key conventions
- **Runtime**: Python 3.12+, managed via `uv`
- **Framework**: FastAPI with async endpoints
- **Entry point**: `main:app` (uvicorn)
- **Dependencies**: Declared in `pyproject.toml`, locked via `uv.lock`
- **Run**: `uv run uvicorn main:app --reload` from `src/provider`

## Init procedure
1. `mkdir -p src/<name>`
2. `uv init --name <name> --description "<desc>" --python 3.12` in `src/<name>`
3. `uv add fastapi uvicorn[standard]`
4. Write `main.py` with FastAPI app and `/health` endpoint
5. **Add `.gitignore`** — `uv init` does not generate one. Must include:
   - `.venv/` — virtual environment
   - `__pycache__/`, `*.pyc` — Python bytecode
   - `.env` — environment variables
   - `*.egg-info/`, `dist/`, `build/` — packaging artifacts
