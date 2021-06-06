from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Style(Base):
    __tablename__ = 'style'

    id = Column(Integer, primary_key=True, nullable=False) 
    gender = Column(String(50))
    masterCategory = Column(String(100))
    subCategory = Column(String(100))
    articleType = Column(String(100))
    baseColour = Column(String(100))
    season = Column(String(100))
    year = Column(Integer)
    usage = Column(String(100))
    productDisplayName = Column(String(300))
    file_url = Column(String(250))