from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc, asc
from typing import List, Optional

from ..database import get_db
from ..models import Lead
from ..schemas import LeadResponse

router = APIRouter()

@router.get("/leads/", response_model=List[LeadResponse])
async def get_leads(
    platform: Optional[str] = None,
    pipeline: Optional[str] = None,
    has_email: Optional[bool] = None,
    has_website: Optional[bool] = None,
    min_rating: Optional[float] = None,
    min_score: Optional[int] = None,
    search: Optional[str] = None,
    sort_by: str = "lead_score",
    sort_dir: str = "desc",
    page: int = 1,
    page_size: int = 50,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Lead)
    
    if platform:
        stmt = stmt.where(Lead.platform == platform)
    if pipeline:
        stmt = stmt.where(Lead.pipeline == pipeline)
    if has_email is not None:
        stmt = stmt.where(Lead.has_email == (1 if has_email else 0))
    if has_website is not None:
        stmt = stmt.where(Lead.has_website == (1 if has_website else 0))
    if min_rating is not None:
        stmt = stmt.where(Lead.rating >= min_rating)
    if min_score is not None:
        stmt = stmt.where(Lead.lead_score >= min_score)
    if search:
        search_term = f"%{search}%"
        stmt = stmt.where(or_(
            Lead.name.ilike(search_term),
            Lead.email.ilike(search_term),
            Lead.niche.ilike(search_term)
        ))
        
    sort_col = getattr(Lead, sort_by, Lead.lead_score)
    if sort_dir == "desc":
        stmt = stmt.order_by(desc(sort_col))
    else:
        stmt = stmt.order_by(asc(sort_col))
        
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(stmt)
    return result.scalars().all()
