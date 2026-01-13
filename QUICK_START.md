# Quick Start - LinkedIn Saved Jobs Scraper

## 3 Simple Steps

### 1️⃣ Create Session (First Time)
```bash
python create_session.py
```
- Browser opens → Log in to LinkedIn → Wait for detection → Done!
- Creates `session.json` (reuse this, no need to log in again)

---

### 2️⃣ Get Saved Job URLs
```bash
python scrape_saved_jobs.py
```
- Gets all your saved jobs (handles pagination automatically)
- Creates `saved_job_urls.txt`

---

### 3️⃣ Get Full Job Details
```bash
python scrape_job_details.py
```
- Scrapes complete details for each job
- Creates `saved_jobs_details.json` with everything!

---

## That's It!

Your job details are now in **`saved_jobs_details.json`**

📖 For detailed instructions, see [USAGE_GUIDE.md](USAGE_GUIDE.md)

---

## Session Expired?

If you get "Not logged in" errors, just run step 1 again:
```bash
python create_session.py
```
