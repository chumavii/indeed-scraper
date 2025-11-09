import os
import random
from turtle import title
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class JobScraper:
    def __init__(self, search, location):
        base_url = os.getenv("base_url")

        if not base_url:
            raise ValueError("Base URL is not set")
            
        self.base_url = self.ensure_url_has_scheme(base_url) #ensure url has https:// prefix
        self.search = search
        self.location = location
        self.headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        ])
        }

    def scrape(self):
        try:
            print("Scraping with BeautifulSoup...")
            jobs = self.scrape_with_bs()
            if len(jobs) > 0:
                return jobs
            print("BeautifulSoup returned no data")
            return self.scrape_with_selenium()
        except Exception as e:
            print(f"An error occured.", e)
            print("Switching to Selenium...")
            return self.scrape_with_selenium()

    def scrape_with_bs(self):
        jobs = []
        url = self.build_url()
        result = requests.get(url, headers=self.headers, timeout=10)

        if result.status_code != 200:
            print(f"Failed to load page: {result}")

        soup = BeautifulSoup(result.text, "html.parser")
        cards = soup.select("td.resultContent")

        print(f"Found {len(cards)} jobs")

        for card in cards:
            title = self.safe_select_text(card, "h2.jobTitle span")
            company = self.safe_select_text(card, "[data-testid='company-name']")
            location = self.safe_select_text(card, "[data-testid='text-location']")
            salary = self.safe_select_text(card, "div.salary-snippet-container")
            snippet = self.safe_select_text(card, "div.job-snippet")
            link = card.select_one("h2.jobTitle a")

            if url and url.startswith("/"):
                url = f"https://ca.indeed.com{link}"

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "snippet": snippet,
                "url": url
            })

    def scrape_with_selenium(self):
        print("Scraping with Selenium...")
        chrome_options = Options();
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(
            options=chrome_options,
            service=Service(ChromeDriverManager().install())            
        )

        self.driver.get(self.build_url())
        #import pdb; pdb.set_trace()
        self._wait(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon")))
        print("Current URL:", self.driver.current_url)
        print("Page title:", self.driver.title)
        cards = self.driver.find_elements(By.CSS_SELECTOR, "td.resultContent")

        print("Cards found:", len(cards))

        jobs = []
        
        def safe_text(root, selector):
            try:
                return root.find_element(By.CSS_SELECTOR, selector).text.strip()
            except Exception:
                return None

        def safe_attr(root, selector, attr):
            try:
                return root.find_element(By.CSS_SELECTOR, selector).get_attribute(attr)
            except Exception:
                return None
            
        for card in cards:
            title    = safe_text(card, "h2.jobTitle span")
            company  = safe_text(card, "[data-testid='company-name']")
            location = safe_text(card, "[data-testid='text-location']")
            salary   = safe_text(card, "div.jobMetaDataGroup div")
            snippet  = safe_text(card, "div.slider_sub_item div")
            url      = safe_attr(card, "h2.jobTitle a", "href")

            if url and url.startswith("/"):
                url = f"https://ca.indeed.com{url}"

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "snippet": snippet,
                "url": url
            })

        return jobs

    #--------------
    # Utilities
    #--------------
    def _wait(self, condition, timeout=10):
        print("Wait for target element to appear...")
        return WebDriverWait(self.driver, timeout).until(condition)
    
    def ensure_url_has_scheme(self, url):
        if not url.startswith('http'):
            url = f"https://{url}"
        return url

    def build_url(self):
        s = self.search.replace(" ", "+")
        l = self.location.replace(" ", "+")
        return f"{self.base_url}?q={s}&l={l}"

    def safe_select_text(self, root, selector,):
        try:
            el = root.select_one(selector)
            return el.text.strip() if el else None
        except Exception:
            return None

    def close(self):
        self.driver.quit()