from datetime import date
import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from backend import utils

class SeleniumJobScraper:
    def __init__(self, base_url, search, location, date_range):
        self.base_url = utils.ensure_url_has_scheme(base_url) #ensure url has https:// prefix
        self.search = search
        self.location = location        
        self.pages = int(os.getenv("PAGES"))
        self.date_range = date_range
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())            
        )

    def scrape(self):
        jobs = []
        target_url = utils.build_url(self.base_url, self.search, self.location, self.date_range)
        print("Scraping with Selenium...") 
        
        try:
            for i in range(self.pages):      
                self.driver.get(target_url)
                print("Current URL:", self.driver.current_url)

                try:
                    self._wait(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon"))) 
                except Exception as E:
                    print(f'No job cards found on page {i + 1}')     
                
                cards = self.driver.find_elements(By.CSS_SELECTOR, "td.resultContent")
                print("Cards found:", len(cards))
                self.human_delay()

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
                
                if i < self.pages - 1:
                    print("Going to next page...")
                    start = i * 10
                    current_url = self.driver.current_url
                    target_url = utils.update_start_param(current_url, start)
                    self.human_delay()
        except Exception as e:
            print(e)

        return jobs

    #--------------
    # Utilities
    #--------------
    def _wait(self, condition, timeout=10):
        print("Wait for target element to appear...")
        return WebDriverWait(self.driver, timeout).until(condition)
    
    def human_delay(self, min_sec=2, max_sec=5):
        time.sleep(random.uniform(min_sec, max_sec))

    def human_scroll(self):
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        current = 0
        while current < total_height:
            self.driver.execute_script(f"window.scrollBy(0, {random.randint(200, 400)});")
            time.sleep(random.uniform(0.3, 1.0))
            current += random.randint(200, 400)

    def human_mouse_move_and_click(self, element):
        print("Attemting click...")
        actions = webdriver.ActionChains(self.driver)
        actions.move_to_element(element)
        actions.pause(random.uniform(0.3, 0.8))
        actions.click()
        actions.perform()
        
    def close(self):
        self.driver.quit()