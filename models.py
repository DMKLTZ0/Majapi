from sqlalchemy import Column, Integer, String, DateTime, JSON
from database import Base
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    type = Column(String, index=True)
    module = Column(String, index=True)
    content = Column(String)
    tags = Column(String)  # np. "log,cel,analiza"
    metadata = Column(JSON, nullable=True)
