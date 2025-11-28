"""
Data ingestion script to load marketing content into SQLite database (no Docker needed!)
"""
import json
from sqlalchemy.orm import Session
from database_sqlite import SessionLocal, MarketingContent, init_db
from embeddings import get_embedding_generator
from datetime import datetime
from typing import List


def load_sample_data(file_path: str = "sample_data.json") -> List[dict]:
    """Load sample data from JSON file"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def ingest_content(db: Session, content_data: dict, embedding_generator):
    """
    Ingest a single content item into database
    
    Args:
        db: Database session
        content_data: Dictionary containing content information
        embedding_generator: Embedding generator instance
    """
    # Generate embedding for the content
    text_to_embed = f"{content_data['title']} {content_data['content']}"
    embedding = embedding_generator.generate_embedding(text_to_embed)
    
    # Create MarketingContent instance
    content = MarketingContent(
        title=content_data['title'],
        content=content_data['content'],
        content_type=content_data['content_type'],
        campaign_name=content_data.get('campaign_name'),
        audience=content_data.get('audience'),
        compliance_status=content_data.get('compliance_status', 'approved'),
        source=content_data.get('source'),
        tags=content_data.get('tags'),
        embedding=embedding,  # Store as JSON list
        created_date=datetime.utcnow(),
        is_active=True
    )
    
    db.add(content)
    return content


def run_ingestion():
    """Main ingestion process"""
    print("🚀 Starting data ingestion process (SQLite - No Docker needed!)...")
    
    # Initialize database
    print("\n📊 Initializing SQLite database...")
    init_db()
    
    # Load embedding model
    print("\n🤖 Loading embedding model...")
    embedding_generator = get_embedding_generator()
    
    # Load sample data
    print("\n📥 Loading sample data...")
    sample_data = load_sample_data()
    print(f"Found {len(sample_data)} content items to ingest")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Ingest each content item
        print("\n⚙️  Ingesting content...")
        for idx, content_data in enumerate(sample_data, 1):
            content = ingest_content(db, content_data, embedding_generator)
            print(f"  [{idx}/{len(sample_data)}] Ingested: {content.title}")
        
        # Commit all changes
        db.commit()
        print(f"\n✅ Successfully ingested {len(sample_data)} content items!")
        
        # Verify ingestion
        count = db.query(MarketingContent).count()
        print(f"📈 Total content items in database: {count}")
        print(f"📁 Database location: marketing_content.db")
        
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_ingestion()
