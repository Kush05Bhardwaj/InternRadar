from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    link = Column(String)
    description = Column(Text)
    score = Column(Integer, default=0)
    reason = Column(String, default="")