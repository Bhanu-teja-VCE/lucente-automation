# Lucente — Lead Generation Automation Dashboard

A full-stack lead generation automation tool for Lucente, a B2B2B marketplace connecting Western businesses with Indian freelance video editors.

## Features
- **Client Acquisition**: Scrape US/UK/EU businesses via Google Maps, extracting emails and contact details.
- **Talent Recruitment**: Scrape Indian freelance video editors from Instagram, Upwork, and Fiverr.
- **Premium Dashboard**: Dark-mode web dashboard with glassmorphism and smooth animations.
- **Local SQLite Database**: Data persists across sessions.
- **CSV Export**: Export filtered leads to CSV.

## Prerequisites
- Python 3.11+
- Node.js 18+
- Playwright Chromium browser

## Setup Instructions

### 1. Install Python dependencies
```bash
cd backend
pip install -r requirements.txt
playwright install chromium
```

### 2. Install frontend dependencies
```bash
cd ../frontend
npm install
```

### 3. Start the backend
```bash
cd ../backend
uvicorn main:app --reload --port 8000
```

### 4. Start the frontend
```bash
cd ../frontend
npm run dev
# Open http://localhost:5173
```

## Instagram / Upwork Session Setup
> On first run of an Instagram or Upwork scrape, a terminal prompt will ask for your login credentials. These are used once to generate a local session file (`instagram_session.json` / `upwork_session.json`) and are never stored. Subsequent scrapes reuse the saved session silently.

## Notes on Scraping Limits
> This tool uses local Playwright without proxies. Google Maps and business websites are generally stable. Instagram and Upwork may require re-login if the session expires or if the IP is temporarily rate-limited. If a scrape returns 0 results, wait 10–15 minutes and retry.
