# Job Board Scraper (FastAPI + Playwright + Selenium + React)

![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![Playwright](https://img.shields.io/badge/Playwright-45ba4b?logo=playwright&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?logo=selenium&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)

A **full-stack job search and data extraction app** that scrapes listings from **Indeed** using multiple scraping engines (Playwright and Selenium), normalizes results with **pandas**, and serves them via a **FastAPI backend**.  
The **frontend** (React + TypeScript + Vite) provides a simple interface to query, visualize, and export scraped job data.

---

## 🚀 Features

- ✅ Search jobs by **keyword** and **location**
- ✅ Dual scraping engines — **Playwright (async)** and **Selenium (fallback)**
- ✅ Data normalization with **pandas**
- ✅ CSV export of cleaned results
- ✅ REST API powered by **FastAPI**
- ✅ Frontend built with **React + TypeScript + Vite**
- ✅ Environment-based configuration via `.env`
- ✅ Modular architecture for easy engine swaps or extensions

---

## 🗂️ Project Structure

```
job-board-scraper/
│
├── app.py                      # FastAPI entrypoint
├── .env                        # Environment variables
├── requirements.txt             # Python dependencies
│
├── backend/                     # Backend (FastAPI + Scrapers)
│   ├── __init__.py
│   ├── selenium_scraper.py      # Selenium-based scraper
│   ├── playwright_scraper.py    # Playwright-based scraper
│   ├── parser.py                # Convert raw data → DataFrame
│   ├── normalizer.py            # Clean & normalize DataFrame
│   └── utils.py                 # URL helpers, env parsing, etc.
│
├── frontend/                    # Frontend (React + TypeScript + Vite)
│   ├── src/
│   │   ├── App.tsx              # Main React app
│   │   ├── components/          # UI components
│   │   ├── services/            # API calls to FastAPI
│   │   └── main.tsx             # React root
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
└── data/
    ├── raw/                     # Raw scraped data (optional)
    └── cleaned/                 # Processed CSV output
```

---

## ⚙️ Setup

### 1. **Clone the Repository**
```bash
git clone https://github.com/chumavii/job-board-scraper.git
cd job-board-scraper
```

### 2. **Create and Activate Virtual Environment**
```bash
py -3 -m venv .venv
.\.venv\Scripts\activate      # Windows
source .venv/bin/activate       # macOS/Linux
```

### 3. **Install Backend Dependencies**
```bash
pip install -r requirements.txt
```

If starting fresh:
```bash
pip install fastapi uvicorn pandas selenium playwright python-dotenv webdriver-manager
playwright install
```

### 4. **Set Up Environment Variables**
Create a `.env` file in the root:
```
BASE_URL=https://ca.indeed.com/jobs
HEADLESS=True
```

---

## ▶️ Running the App

### **Backend**
```bash
uvicorn app:app --reload
```

Server runs on:  
`http://127.0.0.1:8000`

Docs available at:  
`http://127.0.0.1:8000/docs`

### **Frontend**
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:  
`http://localhost:5173`

---

## 🧠 Usage

Open the frontend UI and enter your search term and location.  
Alternatively, call the API directly:

```
GET /api/scrape
```

**Parameters:**
- `search` — job title or keyword (required)
- `location` — location (required)
- `engine` — `play` (default) or `selenium` (optional)

---

## 🧩 Example Output

```json
{
  "engine": "play",
  "count": 15,
  "jobs": [
    {
      "title": "Python Developer",
      "company": "ABC Tech",
      "location": "Toronto, ON",
      "salary": "$90,000–$110,000 a year",
      "url": "https://ca.indeed.com/viewjob?jk=abcd1234"
    }
  ]
}
```

---

## 🧰 Tech Stack

| Layer | Stack |
|-------|--------|
| **Backend** | FastAPI, Playwright, Selenium, pandas |
| **Automation** | Python-dotenv, WebDriver Manager |
| **Frontend** | React, TypeScript, Vite, TailwindCSS |
| **Deployment** | Vercel (frontend), Railway / Render / Azure (backend) |

---

## Author

**Chuma**  
Backend Engineer • Automation Developer • Cloud Enthusiast  
[GitHub @chumavii](https://github.com/chumavii)

