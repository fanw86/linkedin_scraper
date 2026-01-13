# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Async LinkedIn scraper built with Playwright for extracting profile, company, and job data from LinkedIn. Version 3.0+ represents a complete rewrite from Selenium to Playwright with async/await throughout.

**Key Technologies:**
- Python 3.8+
- Playwright (async browser automation)
- Pydantic v2 (data models)
- pytest with pytest-asyncio (testing)

## Architecture

### Package Structure

```
linkedin_scraper/
├── core/              # Browser management, authentication, utilities
│   ├── browser.py     # BrowserManager - async context manager for Playwright
│   ├── auth.py        # Authentication (credentials, cookies, session)
│   ├── exceptions.py  # Custom exception hierarchy
│   └── utils.py       # Retry logic, scrolling, element extraction
├── scrapers/          # Scraping implementations
│   ├── base.py        # BaseScraper - common scraping functionality
│   ├── person.py      # PersonScraper
│   ├── company.py     # CompanyScraper
│   ├── job.py         # JobScraper (individual job)
│   ├── job_search.py  # JobSearchScraper (search results)
│   └── saved_jobs.py  # SavedJobsScraper
├── models/            # Pydantic data models
│   ├── person.py      # Person, Experience, Education, Contact, Accomplishment
│   ├── company.py     # Company, CompanySummary, Employee
│   └── job.py         # Job
└── callbacks.py       # Progress tracking (ConsoleCallback, SilentCallback, etc.)
```

### Key Design Patterns

**1. Async Context Manager Pattern**
All browser operations use `async with BrowserManager()` for lifecycle management. The BrowserManager handles Playwright startup, browser launch, context creation, and cleanup.

**2. Scraper Inheritance**
All scrapers inherit from `BaseScraper` which provides common functionality:
- Authentication checking
- Rate limit detection
- Safe element extraction with retry logic
- Scrolling and navigation helpers
- Modal handling

**3. Session Management**
LinkedIn requires authentication. Sessions are saved/loaded as JSON files containing cookies and storage state:
- `browser.save_session("session.json")` - Save authenticated session
- `browser.load_session("session.json")` - Load saved session

**4. Progress Callbacks**
Scrapers accept optional `ProgressCallback` instances for tracking scraping progress. Multiple callbacks can be chained with `MultiCallback`.

### Critical Implementation Details

**Authentication Flow:**
1. Create session file using `wait_for_manual_login()` or `login_with_credentials()`
2. Load session in subsequent runs with `browser.load_session()`
3. Sessions expire after hours/days - regenerate when integration tests fail with auth errors

**Rate Limiting:**
LinkedIn actively rate limits scrapers. The `detect_rate_limit()` function checks for rate limit pages and raises `RateLimitError`. Add delays between requests in production use.

**Headless Mode:**
LinkedIn blocks headless browsers. Use `headless=False` for real scraping. Headless mode (`headless=True`) only works for testing with mocked responses.

**Element Extraction Pattern:**
Use helper methods from `BaseScraper`:
- `safe_extract_text()` - Returns default value if element not found
- `safe_click()` - Includes retry logic
- `element_exists()` - Check presence before extraction
- `get_attribute_safe()` - Safe attribute extraction

## Development Commands

### Setup
```bash
# Clone and install
git clone https://github.com/joeyism/linkedin_scraper.git
cd linkedin_scraper
pip install -e .

# Install dev dependencies
pip install -r requirements-dev.txt
# OR
pip install -e .[dev]

# Install Playwright browsers
playwright install chromium
```

### Testing

```bash
# Run unit tests only (fast, no LinkedIn required)
pytest -m "not integration" -v

# Run all tests (requires valid session.json)
pytest -v

# Run specific test file
pytest tests/test_person_scraper.py -v

# Run specific test
pytest tests/test_person_scraper.py::test_person_model_to_dict -v

# Run with coverage
pytest --cov=linkedin_scraper -v

# Debug with print statements
pytest tests/test_person_scraper.py -v -s
```

**Test Markers:**
- `@pytest.mark.unit` - Unit tests (no network)
- `@pytest.mark.integration` - Integration tests (require LinkedIn session)
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.e2e` - End-to-end tests

### Linting & Formatting

```bash
# Format code (line length: 100)
black linkedin_scraper/

# Lint
flake8 linkedin_scraper/

# Type check
mypy linkedin_scraper/
```

### Building

```bash
# Build distribution packages
python -m build

# Install in editable mode
pip install -e .
```

### Sample Scripts

```bash
# Create authenticated session (opens browser)
python samples/create_session.py

# Test scraping with saved session
python samples/scrape_person.py
python samples/scrape_company.py
```

## Code Style Guidelines

### Async Patterns
- All scraper methods are async and use `await`
- Use `async with BrowserManager()` for browser lifecycle
- Playwright Page and locator APIs are all async
- Always await Playwright operations

### Error Handling
- Use custom exceptions from `core/exceptions.py`
- All exceptions inherit from `LinkedInScraperException`
- `AuthenticationError` - Not logged in or session expired
- `RateLimitError` - LinkedIn rate limiting detected
- `ProfileNotFoundError` - Profile not found or private
- `ScrapingError` - General scraping failures
- `NetworkError` - Browser/network issues

### Imports
Standard library → third-party → local, with blank lines between groups:
```python
import asyncio
import logging
from typing import Optional

from playwright.async_api import Page
from pydantic import BaseModel

from ..models import Person
from ..core import retry_async
```

### Type Hints
- Use type hints on all public methods
- `Optional[T]` for nullable values
- Pydantic models handle validation and serialization

### Docstrings
Use Google-style docstrings for public APIs:
```python
async def scrape(self, url: str) -> Person:
    """
    Scrape a LinkedIn profile.

    Args:
        url: LinkedIn profile URL

    Returns:
        Person object with scraped data

    Raises:
        AuthenticationError: If not logged in
        ProfileNotFoundError: If profile not found
    """
```

## Testing Strategy

### Unit Tests (Fast)
- Test data model conversions (`to_dict()`, `to_json()`)
- Test utility functions without network calls
- Test browser context management
- Run with `pytest -m "not integration"`

### Integration Tests (Slow)
- Require valid `linkedin_session.json` in root
- Make real network calls to LinkedIn
- Take 2-5 minutes per test
- May hit rate limits if run too frequently
- Sessions expire - regenerate as needed
- Run with `pytest -m integration`

### Session File Management
Integration tests check for `linkedin_session.json` in the project root. If not found, fixtures skip gracefully. Create sessions using `samples/create_session.py`.

## Important Notes

**LinkedIn DOM Changes:**
LinkedIn frequently updates their HTML structure. Scrapers use defensive selectors and fallbacks. When scraping breaks, check LinkedIn's current DOM structure and update selectors accordingly.

**Rate Limiting:**
Respect LinkedIn's rate limits. Add `await asyncio.sleep(2)` between requests. Running integration tests repeatedly may trigger temporary blocks.

**Session Security:**
Never commit session files (`.gitignore` includes `linkedin_session.json`). Sessions contain authentication tokens.

**Headless Detection:**
LinkedIn actively detects and blocks headless browsers. Always use `headless=False` for real scraping.

**Browser Lifecycle:**
Always use async context manager (`async with BrowserManager()`) to ensure proper cleanup. Manual start/close is error-prone.

**Pydantic V2:**
Models use Pydantic v2 API. Use `model_dump()` not `dict()`, and `model_validate()` not `parse_obj()`.

## Common Patterns

### Basic Scraping Flow
```python
async with BrowserManager(headless=False) as browser:
    await browser.load_session("session.json")
    scraper = PersonScraper(browser.page)
    person = await scraper.scrape("https://linkedin.com/in/username/")
```

### Adding New Scraper
1. Inherit from `BaseScraper`
2. Accept `page: Page` and optional `callback: ProgressCallback`
3. Implement async `scrape()` method
4. Call `await self.ensure_logged_in()` at start
5. Use safe extraction helpers from base class
6. Return appropriate Pydantic model
7. Add to `scrapers/__init__.py` exports

### Extending Models
1. Define in appropriate file under `models/`
2. Inherit from Pydantic `BaseModel`
3. Use `Optional[T]` for nullable fields
4. Add validation with `@field_validator` if needed
5. Export from `models/__init__.py`

## Version Information

Current version: 3.0.1 (defined in `linkedin_scraper/__init__.py`)

Major version 3.0+ is NOT backwards compatible with 2.x (Selenium-based). See README.md for migration guide.
