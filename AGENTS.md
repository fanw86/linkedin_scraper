# AGENTS.md

## Scope
- Applies to entire repository.
- Follow existing async Playwright + Pydantic patterns.

## Project Summary
- Async LinkedIn scraping library built on Playwright.
- Primary package: `linkedin_scraper/`
- Tests live in `tests/`

## Setup
- Python >= 3.8.
- Install deps: `pip install -r requirements.txt`
- Dev deps: `pip install -r requirements-dev.txt` or `pip install -e .[dev]`
- Install browsers: `playwright install chromium`

## Test Commands (pytest)
- All tests: `pytest tests/ -v`
- Unit only: `pytest tests/ -v -m "not integration"`
- Integration only: `pytest tests/ -v -m "integration"`
- Single file: `pytest tests/test_person_scraper.py -v`
- Single test: `pytest tests/test_person_scraper.py::test_person_model_to_dict -v`
- Filter by name: `pytest -k "person_model" -v`
- Coverage: `pytest --cov=linkedin_scraper -v`
- Verbose + print: `pytest -v -s`

### Pytest Config
- Config in `pytest.ini` and `pyproject.toml`.
- `asyncio_mode = auto` (pytest-asyncio).
- Markers: `unit`, `integration`, `slow`, `e2e`.

### Integration Test Notes
- Requires a valid session file (see README/TESTING).
- LinkedIn may block headless browsers; tests use headed mode.
- Session files expire; regenerate as needed.
- When no session is present, integration fixtures skip.

### Test Tips
- Fast loop: `pytest -m "not integration" --tb=short`
- Debug output: `pytest tests/test_person_scraper.py -v -s`
- Run just one test: `pytest tests/test_person_scraper.py::test_person_model_to_dict -v`

## Build / Package
- Build wheel/sdist: `python -m build`
- Editable install: `pip install -e .`

## Lint / Format / Type Check
- Tools listed in `requirements-dev.txt`: `black`, `flake8`, `mypy`.
- Run formatting: `black linkedin_scraper/`
- Lint: `flake8 linkedin_scraper/`
- Type check: `mypy linkedin_scraper/`
- No repo-level config files found for these tools; defaults apply.
- Line length guideline: 100 (from `CONTRIBUTING.md`).

## Code Style
- Follow PEP 8 with 100-char line length.
- Prefer explicit, readable names over abbreviations.
- Keep functions focused; avoid unrelated refactors.
- Favor small, safe changes in scrapers (LinkedIn DOM changes often).

### Imports
- Order: standard library → third-party → local.
- Use absolute or package-relative imports (e.g., `from ..models import Person`).
- Group imports with a blank line between sections.

### Typing
- Type hints are expected on public methods.
- Use `Optional[T]`, `list[T]`, `dict[str, T]` as in existing code.
- Pydantic models live in `linkedin_scraper/models/`.
- Validators use `@field_validator` where needed.
- Avoid adding new `# type: ignore` unless strictly required.

### Async Patterns
- Scrapers and browser utilities are `async`/`await`.
- Use Playwright `Page` and locators with async APIs.
- Prefer existing helpers in `scrapers/base.py` (safe_* helpers).
- Keep network waits explicit (`wait_for_selector`, `wait_for_load_state`).

### Error Handling
- Prefer custom exceptions from `linkedin_scraper/core/exceptions.py`.
- Wrap scraper flows with `try/except` and raise `ScrapingError` on failure.
- Use `logger.warning/debug` for recoverable parsing issues.
- Avoid empty `except:` unless matching existing patterns.

### Logging
- Use `logger = logging.getLogger(__name__)`.
- Keep logs informative, not noisy; prefer debug for parsing fallbacks.

### Docstrings
- Public classes and methods use Google-style docstrings.
- Include Args/Returns/Raises sections where relevant.

### Naming
- Classes: `PascalCase` (e.g., `PersonScraper`).
- Methods/vars: `snake_case`.
- Internal helpers prefixed with `_`.
- Exceptions end with `Error`.

## Tests
- New functionality should include unit tests when practical.
- Mark integration tests with `@pytest.mark.integration`.
- Keep assertions explicit and descriptive.
- Async tests rely on pytest-asyncio (`asyncio_mode=auto`).

## Samples
- Reference scripts in `samples/` for usage patterns.
- Session creation script: `python samples/create_session.py`
- Scrape demos: `python samples/scrape_person.py`, `python samples/scrape_company.py`

## Secrets & Local Files
- Do not commit `.env` or `linkedin_session.json`.
- `.env.example` shows `LINKEDIN_EMAIL`/`LINKEDIN_PASSWORD`.
- Session files are required for integration tests.

## Runtime Notes
- LinkedIn rate limits; space out requests in integrations.
- Headless mode may fail; prefer `headless=False` for real pages.
- Use callbacks to track progress if needed (`callbacks.py`).

## Repository Layout
- `linkedin_scraper/core/`: browser/auth utilities.
- `linkedin_scraper/scrapers/`: scraping logic.
- `linkedin_scraper/models/`: Pydantic data models.
- `tests/`: pytest suite.
- `samples/`: runnable examples.

## Cursor / Copilot Rules
- No `.cursorrules`, `.cursor/rules/`, or `.github/copilot-instructions.md` found.

## Notes for Agents
- Prefer minimal changes; avoid broad refactors in bugfixes.
- When in doubt, follow patterns in `scrapers/` and `models/`.
- Respect rate limits; integration tests hit LinkedIn.
- Avoid touching `samples/` unless asked.
- Update tests/docs when behavior changes.
- Keep new public APIs documented in docstrings.
- Ensure new exceptions subclass `LinkedInScraperException`.

## Pre-commit Checklist
- Run unit tests or targeted tests for changed area.
- Run formatting and lint if touching core modules.
- Keep line length <= 100.
- Ensure async functions are awaited.
- Keep session files local.
- Verify imports are ordered correctly.
- Use existing callbacks and models.
- Avoid network calls in unit tests.
- Mark slow tests with `@pytest.mark.slow`.
- Document new markers in `pytest.ini`.
