from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from ..database import get_db
from ..models import Lead

router = APIRouter()

@router.get("/analytics/")
async def get_analytics(db: AsyncSession = Depends(get_db)):
    total_leads = await db.scalar(select(func.count(Lead.id))) or 0
    
    week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
    leads_this_week = await db.scalar(select(func.count(Lead.id)).where(Lead.date_scraped >= week_ago)) or 0
    
    platforms_result = await db.execute(select(Lead.platform, func.count(Lead.id)).group_by(Lead.platform))
    by_platform = {row[0]: row[1] for row in platforms_result.all()}
    
    leads_with_email = await db.scalar(select(func.count(Lead.id)).where(Lead.has_email == 1)) or 0
    email_rate = leads_with_email / total_leads if total_leads > 0 else 0.0
    
    avg_score = await db.scalar(select(func.avg(Lead.lead_score))) or 0.0
    
    sessions_result = await db.execute(
        select(Lead.session_id, Lead.platform, func.count(Lead.id), func.max(Lead.date_scraped))
        .group_by(Lead.session_id, Lead.platform)
        .order_by(func.max(Lead.date_scraped).desc())
        .limit(5)
    )
    
    sessions = [
        {"session_id": row[0], "platform": row[1], "count": row[2], "date": row[3]}
        for row in sessions_result.all() if row[0]
    ]
    
    return {
        "total_leads": total_leads,
        "leads_this_week": leads_this_week,
        "by_platform": by_platform,
        "email_rate": round(email_rate, 2),
        "avg_lead_score": round(avg_score),
        "sessions": sessions
    }
