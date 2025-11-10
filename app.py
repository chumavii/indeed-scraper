from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.selenium_scraper import SeleniumJobScraper
from backend.playwright_scraper import PlaywrightJobScraper
from backend.parser import to_dataframe
from backend.normalizer import clean_basic
import os


load_dotenv()
app = FastAPI(
    title="Indeed Scraper API",
    description="Scrapes Indeed job listings via Selenium or BeautifulSoup",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message": "Job Board Scraper API is running", "docs": "/docs"}

@app.get("/api/scrape")
async def scrape_jobs(
    search: str = Query(..., description="Job title or keyword"),
    location: str = Query(..., description="Job location")
):
    try:
        base_url = os.getenv("BASE_URL")
        if not base_url:
            raise ValueError("Base URL is not set")

        scraper = PlaywrightJobScraper()
        raw_jobs = await scraper.scrape(base_url, search, location)
        #scraper.close()

        df = to_dataframe(raw_jobs)
        df = clean_basic(df)
        data = df.to_dict(orient="records")
        return JSONResponse(content={"count": len(data), "jobs": data})
    except Exception as e:
        #scraper.close()
        return JSONResponse(status_code=500, content={"error": str(e)})

