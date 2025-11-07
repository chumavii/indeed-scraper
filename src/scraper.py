from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JobScraper:
    BASE_URL = "https://ca.indeed.com/jobs"

    def __init__(self, search, location):
        self.search = search
        self.location = location

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

    def build_url(self):
        q = self.search.replace(" ", "+")
        l = self.location.replace(" ", "+")
        return f"{self.BASE_URL}?q={q}&l={l}"
    
    def scrape(self):
        self.driver.get(self.build_url())
        import pdb; pdb.set_trace()
        self._wait(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon")))
        print("Current URL:", self.driver.current_url)
        print("Page title:", self.driver.title)
        cards = self.driver.find_elements(By.CSS_SELECTOR, "td.resultContent")
        
        # if not cards:
        #     cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")

        # if not cards:
        #     cards = self.driver.find_elements(By.CSS_SELECTOR, "div.cardOutline")

        # if not cards:
        #     cards = self.driver.find_elements(By.CSS_SELECTOR, "li.css-5lfssm")

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
            print("title: ", title)

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
    
    def _wait(self, condition, timeout=10):
        """wait for a selenium expected_condition to be true."""
        return WebDriverWait(self.driver, timeout).until(condition)
    
    def close(self):
        self.driver.quit()