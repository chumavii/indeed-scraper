import os
from playwright.async_api import async_playwright
from backend import utils

class PlaywrightJobScraper:
    async def scrape(self, base_url: str, search: str, location:str):
        is_headless = utils.getenv_bool("HEADLESS")
        base_url = utils.ensure_url_has_scheme(base_url)
        target_url = utils.build_url(base_url, search, location)
        print(f"Launching Playwright for {target_url}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=is_headless, args=[
                "--window-size=1920,1080",
                "--disable-blink-features=AutomationControlled"
            ])
            context = await browser.new_context(
                viewport={"width":1920, "height":1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                            (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            await page.goto(target_url, wait_until="domcontentloaded")

            await page.wait_for_selector("td.resultContent", timeout=10000)


            cards = await page.query_selector_all("td.resultContent")
            print("Cards found:", len(cards))

            jobs = []

            for card in cards:
                title_el = await card.query_selector("h2.jobTitle span")
                company_el = await card.query_selector("[data-testid='company-name']")
                location_el = await card.query_selector("[data-testid='text-location']")
                salary_el = await card.query_selector("div.jobMetaDataGroup div")
                link_el = await card.query_selector("h2.jobTitle a")

                title = await title_el.evaluate("(el) => el.innerText") if title_el else None
                company = await company_el.evaluate("(el) => el.innerText") if company_el else None
                location = await location_el.evaluate("(el) => el.innerText") if location_el else None
                salary = await salary_el.evaluate("(el) => el.innerText") if salary_el else None
                url = await link_el.evaluate("(el) => el.href") if link_el else None

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "salary": salary,
                    "url": url
                })
            
            await browser.close()
            return jobs