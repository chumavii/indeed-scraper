import os
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.selenium_scraper import SeleniumJobScraper
from backend.playwright_scraper import PlaywrightJobScraper
from backend.parser import to_dataframe
from backend.normalizer import clean_basic


# --- FastAPI setup ---
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

# --- Routes ---
@app.get("/")
def home():
    return {"message": "Job Board Scraper API is running", "docs": "/docs"}

@app.get("/api/scrape")
async def scrape_jobs(
    search: str = Query(..., description="Job title or keyword"),
    location: str = Query(..., description="Job location"),
    engine: str = Query("play", description="Scraper engine: play or selenium")
):
    try:
        print(f"Executing with: {engine.upper()}")
        base_url = os.getenv("BASE_URL")
        if not base_url:
            raise ValueError("Base URL is not set")
        
        engine = engine.lower()
        if engine == "selenium":
            scraper = SeleniumJobScraper(base_url, search, location)
            raw_jobs = scraper.scrape()
            scraper.close()
        else:
            scraper = PlaywrightJobScraper()
            raw_jobs = await scraper.scrape(base_url, search, location)

        df = to_dataframe(raw_jobs)
        df = clean_basic(df)
        data = df.to_dict(orient="records")

        return JSONResponse(content={"engine": engine, "count": len(data), "jobs": data})
    except Exception as e:
        print("Error:", e)
        if not engine == "play":
            scraper.close()
        return JSONResponse(status_code=500, content={"error": str(e)})
