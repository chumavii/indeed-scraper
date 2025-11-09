# Indeed Scraper (Python + Selenium + Pandas)

A lightweight Python scraper that extracts job listings from **Indeed** using Selenium and normalizes the results with **pandas**. Supports multi-page scraping, structured field extraction, and CSV export for downstream analysis.

------------------------------------------------------------------------

## Features

-   ✅ Search Indeed by keyword and location\
-   ✅ Extract job title, company, location, salary, snippet, and URL\
-   ✅ Multi-page scraping (`start=0,10,20…`)\
-   ✅ Clean, normalized CSV output\
-   ✅ Modular architecture (scraper → parser → normalizer)\
-   ✅ Environment-based configuration via `.env`

------------------------------------------------------------------------

## Project Structure

    job-board-scraper/
    │
    ├── run.py
    ├── .env
    ├── requirements.txt
    │
    ├── src/
    │   ├── scraper.py        # Selenium scraper
    │   ├── parser.py         # Raw → DataFrame
    │   └── normalizer.py     # Clean & transform fields
    │
    └── data/
        ├── raw/
        └── cleaned/

------------------------------------------------------------------------

## Setup (Step-by-Step)

### 1. Clone the repository

``` bash
git clone <repo-url>
cd job-board-scraper
```

### 2. Create a virtual environment

``` bash
py -3 -m venv .venv
```

### 3. Activate the virtual environment

PowerShell:

``` bash
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

``` bash
source .venv/bin/activate
```

### 4. Upgrade pip

``` bash
python -m pip install --upgrade pip
```

### 5. Install dependencies

``` bash
pip install -r requirements.txt
```

If you're setting up from scratch:

``` bash
pip install pandas selenium webdriver-manager python-dotenv
pip freeze > requirements.txt
```

### 6. Create the `.env` file

    SEARCH_TERM=Python Developer
    LOCATION=Canada
    PAGES=5

### 7. Run the scraper

``` bash
python run.py
```

Output will be generated in:

    data/cleaned/output.csv

------------------------------------------------------------------------

## Usage

Modify search criteria in `.env`, then simply run:

``` bash
python run.py
```

------------------------------------------------------------------------
