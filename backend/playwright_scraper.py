import os
import asyncio
from playwright.async_api import async_playwright
from backend import utils

class PlaywrightJobScraper:
    async def scrape(self, base_url: str, search: str, location:str):
        base_url = utils.ensure_url_has_scheme(base_url)
        target_url = utils.build_url(base_url, search, location)
        print(f"Launching Playwright for {target_url}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(target_url, wait_until="domcontentloaded")

            await page.wait_for_selector("td.resultContent, div.job_seen_beacon, li.css-5lfssm", timeout=20000)


            cards = await page.query_selector_all("td.resultContent")
            print("Cards found:", len(cards))

            jobs = []

            for card in cards:
                title = await card.query_selector_eval("h2.jobTitle span", "el => el.innerText") if await card.query_selector("h2.jobTitle span") else None
                company = await card.query_selector_eval("[data-testid='company-name']", "el => el.innerText") if await card.query_selector("[data-testid='company-name']") else None
                location = await card.query_selector_eval("[data-testid='text-location']", "el => el.innerText") if await card.query_selector("[data-testid='text-location']") else None
                salary = await card.query_selector_eval("div.jobMetaDataGroup div", "el => el.innerText") if await card.query_selector("div.jobMetaDataGroup div") else None
                url = await card.query_selector_eval("h2.jobTitle a", "el => el.href") if await card.query_selector("h2.jobTitle a") else None

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "salary": salary,
                    "url": url
                })
            
            await browser.close()
            return jobs