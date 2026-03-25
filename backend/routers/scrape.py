from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime
import json

from ..schemas import ScrapeRequest, ScrapeResponse
from ..database import get_db
from ..models import Lead
from ..scrapers import google_maps, instagram, upwork, fiverr

router = APIRouter()

scrape_status = {}

def compute_lead_score(lead: dict) -> int:
    score = 0
    if lead.get("email"):         score += 30
    if lead.get("website"):       score += 20
    rating = lead.get("rating") or 0
    if rating >= 4.0:             score += 20
    reviews = lead.get("review_count") or 0
    if reviews >= 10:             score += 10
    if lead.get("social_links"):  score += 10
    if lead.get("phone"):         score += 5
    if lead.get("response_rate"): score += 5
    return min(score, 100)

async def run_scrape_job(session_id: str, req: ScrapeRequest, db: AsyncSession):
    scrape_status[session_id] = {"status": "running", "count": 0}
    try:
        leads_data = []
        if req.platform == "google_maps":
            leads_data = await google_maps.scrape(req.query, req.location or "", req.max_results)
        elif req.platform == "instagram":
            leads_data = await instagram.scrape(req.query, req.location or "", req.max_results)
        elif req.platform == "upwork":
            leads_data = await upwork.scrape(req.query, req.location or "", req.max_results)
        elif req.platform == "fiverr":
            leads_data = await fiverr.scrape(req.query, req.location or "", req.max_results)
            
        for lead_data in leads_data:
            lead_score = compute_lead_score(lead_data)
            has_email = 1 if lead_data.get("email") else 0
            has_website = 1 if lead_data.get("website") else 0
            
            db_lead = Lead(
                platform=req.platform,
                pipeline=req.pipeline,
                name=lead_data.get("name"),
                location=lead_data.get("location"),
                niche=lead_data.get("niche"),
                email=lead_data.get("email"),
                website=lead_data.get("website"),
                phone=lead_data.get("phone"),
                rating=lead_data.get("rating"),
                review_count=lead_data.get("review_count"),
                social_links=json.dumps(lead_data.get("social_links", [])),
                has_email=has_email,
                has_website=has_website,
                lead_score=lead_score,
                raw_bio=lead_data.get("raw_bio"),
                hourly_rate=lead_data.get("hourly_rate"),
                response_rate=lead_data.get("response_rate"),
                date_scraped=datetime.utcnow().isoformat(),
                session_id=session_id
            )
            db.add(db_lead)
            
        await db.commit()
        scrape_status[session_id] = {"status": "complete", "count": len(leads_data)}
        
    except Exception as e:
        print(f"Scrape job error: {e}")
        scrape_status[session_id] = {"status": "error", "count": 0}

@router.post("/scrape/", response_model=ScrapeResponse)
async def start_scrape(req: ScrapeRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    session_id = str(uuid.uuid4())
    background_tasks.add_task(run_scrape_job, session_id, req, db)
    return ScrapeResponse(session_id=session_id, status="started")

@router.get("/scrape/status/{session_id}")
async def get_scrape_status(session_id: str):
    return scrape_status.get(session_id, {"status": "not_found", "count": 0, "session_id": session_id})
