"""Scrape full details for saved jobs."""

import asyncio
import json
from linkedin_scraper import BrowserManager, JobScraper


async def main():
    # Read the job URLs
    with open("saved_job_urls.txt", "r") as f:
        job_urls = [line.strip() for line in f if line.strip()]

    print(f"Found {len(job_urls)} saved jobs to scrape\n")

    async with BrowserManager(headless=False) as browser:
        print("Loading session...")
        await browser.load_session("session.json")

        job_scraper = JobScraper(browser.page)
        jobs_data = []

        for i, url in enumerate(job_urls, 1):
            try:
                print(f"\n[{i}/{len(job_urls)}] Scraping: {url}")

                job = await job_scraper.scrape(url)

                # Display job info
                print(f"  Title: {job.job_title}")
                print(f"  Company: {job.company}")
                print(f"  Location: {job.location}")
                print(f"  Posted: {job.posted_date}")
                print(f"  Applicants: {job.applicant_count}")

                # Save to list
                jobs_data.append({
                    "job_title": job.job_title,
                    "company": job.company,
                    "company_url": job.company_linkedin_url,
                    "location": job.location,
                    "posted_date": job.posted_date,
                    "applicant_count": job.applicant_count,
                    "job_description": job.job_description,
                    "benefits": job.benefits,
                    "url": job.linkedin_url
                })

                # Rate limiting - wait between requests
                if i < len(job_urls):  # Don't wait after last one
                    print("  Waiting 3 seconds...")
                    await asyncio.sleep(3)

            except Exception as e:
                print(f"  ERROR: {e}")
                continue

        # Save to JSON
        output_file = "saved_jobs_details.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(jobs_data, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 60)
        print(f"SUCCESS! Scraped {len(jobs_data)}/{len(job_urls)} jobs")
        print(f"Results saved to: {output_file}")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
