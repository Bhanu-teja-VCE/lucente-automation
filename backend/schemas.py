from pydantic import BaseModel
from typing import Optional, List

class ScrapeRequest(BaseModel):
    platform: str
    pipeline: str
    query: str
    location: Optional[str] = None
    max_results: int = 20

class ScrapeResponse(BaseModel):
    session_id: str
    status: str

class LeadResponse(BaseModel):
    id: int
    platform: str
    pipeline: str
    name: Optional[str]
    location: Optional[str]
    niche: Optional[str]
    email: Optional[str]
    website: Optional[str]
    phone: Optional[str]
    rating: Optional[float]
    review_count: Optional[int]
    social_links: Optional[str]
    has_email: int
    has_website: int
    lead_score: int
    raw_bio: Optional[str]
    hourly_rate: Optional[str]
    response_rate: Optional[str]
    date_scraped: Optional[str]
    session_id: Optional[str]

    class Config:
        from_attributes = True
