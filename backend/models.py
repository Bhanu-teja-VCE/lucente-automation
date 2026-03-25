from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    platform = Column(String, nullable=False)
    pipeline = Column(String, nullable=False)
    name = Column(String)
    location = Column(String)
    niche = Column(String)
    email = Column(String)
    website = Column(String)
    phone = Column(String)
    rating = Column(Float)
    review_count = Column(Integer)
    social_links = Column(Text) # JSON array of URLs
    has_email = Column(Integer, default=0)
    has_website = Column(Integer, default=0)
    lead_score = Column(Integer, default=0)
    raw_bio = Column(Text)
    hourly_rate = Column(String)
    response_rate = Column(String)
    date_scraped = Column(String)
    session_id = Column(String)
