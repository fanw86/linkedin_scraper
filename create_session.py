"""Create authenticated LinkedIn session with proper verification."""

import asyncio
from linkedin_scraper import BrowserManager, is_logged_in


async def create_session():
    async with BrowserManager(headless=False) as browser:
        print("\n" + "="* 60)
        print("Step 1: Opening LinkedIn...")
        print("=" * 60)

        await browser.page.goto("https://www.linkedin.com/login")
        await asyncio.sleep(3)

        print("\n" + "=" * 60)
        print("Step 2: Please LOG IN to LinkedIn in the browser window")
        print("IMPORTANT: After logging in, navigate to your FEED page")
        print("          (https://www.linkedin.com/feed/)")
        print("\nWaiting for 5 MINUTES for you to complete login...")
        print("=" * 60)

        # Check login status every 10 seconds for up to 5 minutes
        max_attempts = 30  # 30 x 10 seconds = 5 minutes
        logged_in = False

        for attempt in range(max_attempts):
            await asyncio.sleep(10)

            # Check if logged in
            logged_in = await is_logged_in(browser.page)

            time_elapsed = (attempt + 1) * 10
            time_remaining = (max_attempts * 10) - time_elapsed

            if logged_in:
                print(f"\n[{time_elapsed}s] LOGIN DETECTED!")
                break
            else:
                print(f"[{time_elapsed}s] Not logged in yet... ({time_remaining}s remaining)")

        if logged_in:
            print("\n" + "=" * 60)
            print("SUCCESS: You are logged in!")
            print("Saving session...")
            print("=" * 60)

            await browser.save_session("session.json")

            print("\nSession saved successfully to session.json")
            print("You can now use this session to scrape LinkedIn")
            print("\nKeeping browser open for 10 more seconds...")
            await asyncio.sleep(10)
        else:
            print("\n" + "=" * 60)
            print("WARNING: Login not detected after 5 minutes")
            print("Please make sure you:")
            print("  1. Completed the login process")
            print("  2. Navigated to https://www.linkedin.com/feed/")
            print("  3. Can see your LinkedIn feed")
            print("\nSaving session anyway (may not work)...")
            print("=" * 60)

            await browser.save_session("session.json")
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(create_session())
