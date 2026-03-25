from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
import csv
import io
from datetime import datetime

from ..database import get_db
from ..models import Lead

router = APIRouter()

@router.get("/export/csv")
async def export_csv(
    platform: str = None,
    pipeline: str = None,
    has_email: bool = None,
    has_website: bool = None,
    min_rating: float = None,
    min_score: int = None,
    search: str = None,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Lead)
    
    if platform: stmt = stmt.where(Lead.platform == platform)
    if pipeline: stmt = stmt.where(Lead.pipeline == pipeline)
    if has_email is not None: stmt = stmt.where(Lead.has_email == (1 if has_email else 0))
    if has_website is not None: stmt = stmt.where(Lead.has_website == (1 if has_website else 0))
    if min_rating is not None: stmt = stmt.where(Lead.rating >= min_rating)
    if min_score is not None: stmt = stmt.where(Lead.lead_score >= min_score)
    if search:
        search_term = f"%{search}%"
        stmt = stmt.where(or_(
            Lead.name.ilike(search_term),
            Lead.email.ilike(search_term),
            Lead.niche.ilike(search_term)
        ))
        
    result = await db.execute(stmt)
    leads = result.scalars().all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    headers = ["ID", "Platform", "Pipeline", "Name", "Location", "Niche", "Email", "Website", "Phone", "Rating", "Review Count", "Lead Score", "Date Scraped"]
    writer.writerow(headers)
    
    for lead in leads:
        writer.writerow([
            lead.id, lead.platform, lead.pipeline, lead.name, lead.location, lead.niche,
            lead.email, lead.website, lead.phone, lead.rating, lead.review_count, lead.lead_score, lead.date_scraped
        ])
        
    output.seek(0)
    
    filename = f"lucente_leads_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
