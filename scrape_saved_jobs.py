"""Scrape saved jobs - skip login detection, just try it."""

import asyncio
import json
from linkedin_scraper import BrowserManager, SavedJobsScraper, JobScraper


async def main():
    async with BrowserManager(headless=False) as browser:
        print("Loading session...")
        await browser.load_session("session.json")

        print("\n" + "=" * 60)
        print("Navigating to your saved jobs page...")
        print("If you see a login page, please log in manually")
        print("=" * 60)

        # Navigate directly to saved jobs
        await browser.page.goto("https://www.linkedin.com/my-items/saved-jobs/", timeout=30000)
        await asyncio.sleep(5)

        current_url = browser.page.url
        print(f"\nCurrent URL: {current_url}")

        # Check if we're on the login page
        if "login" in current_url or "authwall" in current_url:
            print("\n" + "=" * 60)
            print("You need to log in manually in the browser window")
            print("After logging in, the script will continue...")
            print("Waiting 2 minutes...")
            print("=" * 60)

            # Wait for navigation away from login page
            for i in range(24):  # 24 x 5 seconds = 2 minutes
                await asyncio.sleep(5)
                current_url = browser.page.url
                if "my-items/saved-jobs" in current_url or "feed" in current_url:
                    print(f"\n[{(i+1)*5}s] Login detected! Saving session...")
                    await browser.save_session("session.json")

                    # Navigate back to saved jobs
                    await browser.page.goto("https://www.linkedin.com/my-items/saved-jobs/", timeout=30000)
                    await asyncio.sleep(3)
                    break
                print(f"[{(i+1)*5}s] Waiting for login...")

        print("\nAttempting to scrape saved jobs...")
        print("(This might fail if not properly logged in)")

        try:
            # Get job URLs from all pages
            await asyncio.sleep(3)

            all_job_urls = []
            page_num = 1

            while True:
                print(f"\n=== Scraping page {page_num} ===")

                # Scroll to load jobs on current page
                await browser.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)

                # Get job links from current page
                job_links = await browser.page.locator('a[href*="/jobs/view/"]').all()
                print(f"Found {len(job_links)} job links on page {page_num}")

                # Extract unique URLs from current page
                for link in job_links:
                    try:
                        href = await link.get_attribute("href")
                        if href and "/jobs/view/" in href:
                            clean_url = href.split("?")[0] if "?" in href else href
                            if not clean_url.startswith("http"):
                                clean_url = f"https://www.linkedin.com{clean_url}"
                            if clean_url not in all_job_urls:
                                all_job_urls.append(clean_url)
                    except:
                        continue

                # Look for "Next" button
                next_button = browser.page.locator('button[aria-label="View next page"], button:has-text("Next")')
                next_button_count = await next_button.count()

                if next_button_count > 0:
                    # Check if button is enabled
                    is_disabled = await next_button.first.is_disabled()

                    if not is_disabled:
                        print(f"Clicking 'Next' button to go to page {page_num + 1}...")
                        await next_button.first.click()
                        await asyncio.sleep(3)  # Wait for next page to load
                        page_num += 1
                    else:
                        print("'Next' button is disabled - reached last page")
                        break
                else:
                    print("No 'Next' button found - only one page")
                    break

            job_urls = all_job_urls
            print(f"\n=== Total: Extracted {len(job_urls)} unique job URLs from {page_num} page(s) ===")

            if job_urls:
                print("\nYour saved jobs:")
                for i, url in enumerate(job_urls, 1):
                    print(f"{i}. {url}")

                # Save to file
                with open("saved_job_urls.txt", "w") as f:
                    f.write("\n".join(job_urls))

                print(f"\nSaved URLs to: saved_job_urls.txt")
            else:
                print("\nNo job URLs found. Make sure you:")
                print("1. Are logged in")
                print("2. Have saved jobs on LinkedIn")
                print("3. Are on the saved jobs page")

        except Exception as e:
            print(f"\nError: {e}")

        print("\nKeeping browser open for 30 seconds so you can verify...")
        await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())
