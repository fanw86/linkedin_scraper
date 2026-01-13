# LinkedIn Saved Jobs Scraper - Usage Guide

This guide will help you scrape your saved jobs from LinkedIn and extract their full details.

## Overview

This toolkit consists of 3 scripts:

1. **`create_session.py`** - Create an authenticated LinkedIn session (one-time setup)
2. **`scrape_saved_jobs.py`** - Get URLs of all your saved jobs (handles pagination)
3. **`scrape_job_details.py`** - Scrape complete details for each job

## Prerequisites

- Python 3.8+ installed
- Virtual environment activated
- Playwright browsers installed

## Initial Setup (One-Time)

### Step 1: Activate Virtual Environment

**On Windows (Git Bash):**
```bash
source .venv/Scripts/activate
```

**On Windows (Command Prompt):**
```cmd
.venv\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

You'll see `(.venv)` in your prompt when activated.

### Step 2: Install Playwright Browsers (if not already done)

```bash
playwright install chromium
```

## Usage Instructions

### 1. Create LinkedIn Session (First Time Only)

```bash
python create_session.py
```

**What happens:**
- A Chrome browser window will open
- Navigate to the LinkedIn login page
- **Log in manually** with your credentials
- After logging in, navigate to your feed: `https://www.linkedin.com/feed/`
- Wait on the feed page
- The script checks every 10 seconds if you're logged in (up to 5 minutes)
- Once detected, it saves `session.json`

**Important:**
- Don't close the browser until you see "Session saved successfully"
- The session file is saved as `session.json` in the current directory
- Keep this file secure - it contains your authentication

**Session expires after a few hours/days.** When you get authentication errors, re-run this script.

---

### 2. Scrape Your Saved Jobs

```bash
python scrape_saved_jobs.py
```

**What it does:**
- Loads your saved session
- Navigates to `https://www.linkedin.com/my-items/saved-jobs/`
- Handles pagination automatically (clicks "Next" button)
- Extracts all saved job URLs
- Saves URLs to `saved_job_urls.txt`

**Output:**
- Prints all found job URLs to console
- Saves to `saved_job_urls.txt`
- Browser stays open for 30 seconds so you can verify

**If login is required:**
- The script will detect if you're on a login page
- Wait 2 minutes for you to log in manually
- Then automatically saves the new session

---

### 3. Get Full Job Details

```bash
python scrape_job_details.py
```

**What it does:**
- Reads URLs from `saved_job_urls.txt`
- Scrapes each job page for complete details:
  - Job title
  - Company name and LinkedIn URL
  - Location
  - Posted date
  - Applicant count
  - Full job description
  - Benefits (if available)
- Waits 3 seconds between requests (rate limiting)
- Saves all data to `saved_jobs_details.json`

**Output:**
- `saved_jobs_details.json` - Complete job data in JSON format
- Console shows progress for each job

**Time estimate:** ~3-4 seconds per job

---

## Files Created

| File | Description | Keep? |
|------|-------------|-------|
| `session.json` | Your LinkedIn authentication session | ✅ Yes (reusable, don't share) |
| `saved_job_urls.txt` | List of saved job URLs | Optional |
| `saved_jobs_details.json` | Complete job details | ✅ Yes (your data) |

---

## Complete Workflow

```bash
# First time setup
source .venv/Scripts/activate           # Activate venv
playwright install chromium             # Install browsers (if needed)

# Create session (one time, or when expired)
python create_session.py

# Scrape your saved jobs (run whenever you want updated data)
python scrape_saved_jobs.py             # Gets job URLs
python scrape_job_details.py            # Gets full details
```

---

## Troubleshooting

### "Not logged in" Error

**Problem:** Session has expired

**Solution:** Re-run `python create_session.py` to create a fresh session

---

### Browser Closes Immediately

**Problem:** Script timeout or error

**Solution:**
- Make sure you log in within 5 minutes
- Ensure you navigate to the feed page after logging in
- Browser window must stay open during the process

---

### Missing Some Saved Jobs

**Problem:** Pagination not working

**Solution:**
- The script automatically handles pagination
- Verify manually on LinkedIn how many jobs you have saved
- Check that `scrape_saved_jobs.py` shows it clicked through multiple pages

---

### Rate Limiting

**Problem:** LinkedIn blocks too many requests

**Solution:**
- The scripts include 2-3 second delays between requests
- If you get rate limited, wait 10-15 minutes
- Don't run scripts repeatedly in quick succession

---

## Tips

1. **Session Management:** Sessions expire. Keep `session.json` updated when you get auth errors.

2. **Rate Limiting:** LinkedIn monitors scraping activity. Space out your requests:
   - Run scripts once per day maximum
   - Built-in delays help avoid detection

3. **Data Format:** `saved_jobs_details.json` is in JSON format. Open with:
   - Any text editor (VS Code, Notepad++)
   - JSON viewer tools
   - Python script to parse and analyze

4. **Headless Mode:** Scripts run with visible browser (`headless=False`) because LinkedIn blocks headless browsers.

5. **Updates:** Re-run `scrape_saved_jobs.py` whenever you save new jobs on LinkedIn.

---

## Advanced: Running Without Activating Venv

If you prefer not to activate the virtual environment:

```bash
# Windows
.venv/Scripts/python.exe create_session.py
.venv/Scripts/python.exe scrape_saved_jobs.py
.venv/Scripts/python.exe scrape_job_details.py
```

---

## Security Notes

⚠️ **Never share or commit `session.json`** - it contains your authentication tokens

⚠️ **Respect LinkedIn's Terms of Service** - Use responsibly, don't scrape aggressively

⚠️ **Keep your session file secure** - It's equivalent to your login credentials

---

## Support

For issues with the linkedin_scraper package itself, see:
- [GitHub Repository](https://github.com/joeyism/linkedin_scraper)
- [Documentation](https://github.com/joeyism/linkedin_scraper#readme)

---

## Example Output

### saved_job_urls.txt
```
https://www.linkedin.com/jobs/view/4347409399/
https://www.linkedin.com/jobs/view/4346741766/
...
```

### saved_jobs_details.json
```json
[
  {
    "job_title": "Senior Transport Planner",
    "company": "AECOM",
    "company_url": "https://www.linkedin.com/company/aecom/",
    "location": null,
    "posted_date": "Dubai, UAE · 3 days ago · 50 applicants",
    "applicant_count": null,
    "job_description": "Full description here...",
    "benefits": null,
    "url": "https://www.linkedin.com/jobs/view/4347409399/"
  },
  ...
]
```

---

**Last Updated:** January 2026
