from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from backend import utils

class SeleniumJobScraper:
    def __init__(self, base_url, search, location):
        self.base_url = utils.ensure_url_has_scheme(base_url) #ensure url has https:// prefix
        self.search = search
        self.location = location        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())            
        )

    def scrape(self):
        print("Scraping with Selenium...")
        target_url = utils.build_url(self.base_url, self.search, self.location)
        self.driver.get(target_url)
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
                url = f"{self.base_url.rstrip}{url}"

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

    def close(self):
        self.driver.quit()