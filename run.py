import os
from dotenv import load_dotenv
from src.scraper import JobScraper
from src.parser import to_dataframe
from src.normalizer import clean_basic

print("run.py STARTED") 

def main():
    load_dotenv()

    search = os.getenv("SEARCH_TERM")
    location = os.getenv("LOCATION")

    scraper = JobScraper(search, location)
    raw_jobs = scraper.scrape()
    scraper.close()

    df = to_dataframe(raw_jobs)
    df = clean_basic(df)

    df.to_csv("data/cleaned/output.csv", index=False)
    print("Done. File saved at data/cleaned/output.csv")

if __name__ == "__main__":
    main()