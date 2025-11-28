"""
Database connection and table setup using SQLite (no Docker needed!)
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# SQLite database file
DATABASE_FILE = "marketing_content.db"
DATABASE_URL = f"sqlite:///./{DATABASE_FILE}"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class MarketingContent(Base):
    """Marketing content model with embeddings stored as JSON"""
    __tablename__ = "marketing_content"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    content_type = Column(String(50), nullable=False)  # email, social, ad, blog
    campaign_name = Column(String(200))
    audience = Column(String(100))  # B2B, B2C, Enterprise, SMB
    compliance_status = Column(String(50), default="approved")  # approved, pending, rejected
    source = Column(String(200))
    tags = Column(String(500))  # Comma-separated tags
    created_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Vector embedding stored as JSON (list of floats)
    embedding = Column(JSON, nullable=False)
    
    def __repr__(self):
        return f"<MarketingContent(id={self.id}, title='{self.title}', type='{self.content_type}')>"


def init_db():
    """Initialize database and create tables"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ SQLite database initialized successfully!")
    print(f"📁 Database file: {DATABASE_FILE}")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
