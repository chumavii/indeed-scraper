# 🧠 Indeed Scraper API (Python + FastAPI + Selenium + Pandas)

A lightweight **job-scraping microservice** built with **FastAPI**, **Selenium**, and **pandas**.  
It extracts job listings from **Indeed**, cleans and normalizes them for analysis, and exposes an API endpoint for integration with other apps or a React frontend.

---

## 🚀 Features

- ✅ Search Indeed by keyword and location  
- ✅ Extract job title, company, location, salary, snippet, and URL  
- ✅ Multi-page scraping (`start=0,10,20…`)  
- ✅ Headless mode support (runs silently in background)  
- ✅ REST API endpoint (`/api/scrape`) built with **FastAPI**  
- ✅ Clean, normalized CSV output in `data/cleaned/`  
- ✅ Extensible architecture: scraper → parser → normalizer  
- ✅ Environment-based configuration via `.env`  

---

## 🧱 Project Structure

```
job-board-scraper/
│
├── app.py                 # FastAPI entrypoint
├── .env                   # Environment variables
├── requirements.txt
│
├── backend/
│   ├── __init__.py
│   ├── scraper.py         # Selenium/BeautifulSoup scraper
│   ├── parser.py          # Raw → DataFrame
│   ├── normalizer.py      # Clean & transform fields
│   └── utils.py           # Helpers (URL, env handling)
│
├── data/
│   ├── raw/
│   └── cleaned/
│
└── frontend/ (optional)
    ├── vite.config.js     # React + Vite setup
    └── src/               # UI components
```

---

## ⚙️ Setup (Backend API)

### 1. Clone the repository
```bash
git clone https://github.com/chumavii/indeed-scraper.git
cd job-board-scraper
```

### 2. Create & activate a virtual environment
**PowerShell**
```bash
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```
**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
If starting fresh:
```bash
pip install fastapi uvicorn selenium pandas webdriver-manager python-dotenv beautifulsoup4 lxml
pip freeze > requirements.txt
```

### 4. Create the `.env` file
```
SEARCH_TERM=Python Developer
LOCATION=Canada
PAGES=5
BASE_URL=https://ca.indeed.com/jobs
HEADLESS=true
```

### 5. Run the FastAPI server
```bash
uvicorn app:app --reload
```
Visit ➡️ [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the auto-generated Swagger UI.

---

## 🧩 Example API Usage

**GET Request**
```
GET /api/scrape?search=Python%20Developer&location=Toronto
```

**Response**
```json
[
  {
    "title": "Intermediate Full Stack Software Engineer",
    "company": "D3 Security",
    "location": "Vancouver, BC",
    "salary": "$70,000–$100,000 a year",
    "snippet": "Experience with Python and React...",
    "url": "https://ca.indeed.com/viewjob?jk=abcdef0123456789"
  }
]
```

---

## 🧱 Frontend (Optional React UI)

If you’ve added a React interface:

```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

For Tailwind CSS (v4):
```bash
npm install -D tailwindcss @tailwindcss/vite
```

Add this to `vite.config.js`:
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

Then start the frontend:
```bash
npm run dev
```

---

## 🧾 Output

Scraped jobs are saved to:
```
data/cleaned/output.csv
```

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Python 3.12 / FastAPI |
| Scraping | Selenium, BeautifulSoup |
| Data | Pandas |
| Frontend (optional) | React + Vite + Tailwind CSS |
| Environment | python-dotenv |
| Deployment | Docker / Railway / Render / AWS Lambda (optional) |

---

## 🧑‍💻 Author
**Chuma Nwuba**  
[GitHub @chumavii](https://github.com/chumavii)
