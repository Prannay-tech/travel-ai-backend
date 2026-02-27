# AGENTS.md

## Cursor Cloud specific instructions

This is a single-service Python/FastAPI application (Travel AI Backend). No database, Docker, or external infrastructure is required.

### Running the application

- **Dev server:** `python3 main.py` — starts Uvicorn on `0.0.0.0:8000`
- **Tests:** `python3 -m pytest test_main.py -v`
- The codebase has no dedicated linter config (no ruff, flake8, mypy). Use `python3 -m py_compile main.py` to check syntax.

### Key notes

- All external API modules (`flight_apis.py`, `weather_api.py`, `currency_api.py`) have robust mock/fallback data, so the app runs fully without any API keys.
- Use `python3` (not `python`) as `python` is not aliased in this environment.
- Installed packages go to `~/.local` — ensure `$HOME/.local/bin` is on `PATH` when running `pytest` or `uvicorn` directly.
- The app reads `.env` for API keys via `python-dotenv`; create `.env` if you need real API integrations, but it is not required for development/testing.
- See `README.md` for the full list of API endpoints and environment variables.
