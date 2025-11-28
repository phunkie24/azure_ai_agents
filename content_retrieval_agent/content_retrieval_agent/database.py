"""
Database connection and table setup
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from datetime import datetime
from config import get_settings

settings = get_settings()

# Create engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class MarketingContent(Base):
    """Marketing content model with vector embeddings"""
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
    
    # Vector embedding for semantic search
    embedding = Column(Vector(settings.EMBEDDING_DIMENSION))
    
    def __repr__(self):
        return f"<MarketingContent(id={self.id}, title='{self.title}', type='{self.content_type}')>"


def init_db():
    """Initialize database and create tables"""
    # Enable pgvector extension
    with engine.connect() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.commit()
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
