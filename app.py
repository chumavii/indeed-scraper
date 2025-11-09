from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.scraper import JobScraper
from backend.parser import to_dataframe
from backend.normalizer import clean_basic


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
def scrape_jobs(
    search: str = Query(..., description="Job title or keyword"),
    location: str = Query(..., description="Job location")
):
    try:
        scraper = JobScraper(search, location)
        raw_jobs = scraper.scrape_with_selenium()
        scraper.close()

        df = to_dataframe(raw_jobs)
        df = clean_basic(df)
        data = df.to_dict(orient="records")
        return JSONResponse(content={"count": len(data), "jobs": data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

