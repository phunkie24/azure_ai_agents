"""
RAG (Retrieval-Augmented Generation) logic for SQLite (no Docker needed!)
Uses Python-based similarity search instead of database-level vector search
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
import numpy as np
from database_sqlite import MarketingContent
from embeddings import get_embedding_generator
from config import get_settings
from pydantic import BaseModel

settings = get_settings()


class ContentFilter(BaseModel):
    """Filters for content retrieval"""
    content_type: Optional[str] = None
    campaign_name: Optional[str] = None
    audience: Optional[str] = None
    compliance_status: Optional[str] = "approved"
    tags: Optional[List[str]] = None


class RetrievedContent(BaseModel):
    """Retrieved content with metadata"""
    id: int
    title: str
    content: str
    content_type: str
    campaign_name: Optional[str]
    audience: Optional[str]
    compliance_status: str
    source: Optional[str]
    tags: Optional[str]
    similarity_score: float
    
    class Config:
        from_attributes = True


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Similarity score between 0 and 1
    """
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    
    similarity = dot_product / (norm_v1 * norm_v2)
    return float(similarity)


class ContentRetriever:
    """Handle content retrieval with semantic search"""
    
    def __init__(self):
        """Initialize retriever with embedding generator"""
        self.embedding_generator = get_embedding_generator()
    
    def retrieve(
        self,
        db: Session,
        query: str,
        filters: Optional[ContentFilter] = None,
        top_k: int = None
    ) -> List[RetrievedContent]:
        """
        Retrieve relevant content using semantic search
        
        Args:
            db: Database session
            query: Search query
            filters: Optional filters to apply
            top_k: Number of results to return
            
        Returns:
            List of retrieved content with similarity scores
        """
        if top_k is None:
            top_k = settings.TOP_K_RESULTS
        
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_embedding(query)
        
        # Build base query
        db_query = db.query(MarketingContent).filter(
            MarketingContent.is_active == True
        )
        
        # Apply filters if provided
        if filters:
            if filters.content_type:
                db_query = db_query.filter(
                    MarketingContent.content_type == filters.content_type
                )
            if filters.campaign_name:
                db_query = db_query.filter(
                    MarketingContent.campaign_name.like(f"%{filters.campaign_name}%")
                )
            if filters.audience:
                db_query = db_query.filter(
                    MarketingContent.audience == filters.audience
                )
            if filters.compliance_status:
                db_query = db_query.filter(
                    MarketingContent.compliance_status == filters.compliance_status
                )
            if filters.tags:
                # Search for any of the provided tags
                tag_filters = [
                    MarketingContent.tags.like(f"%{tag}%")
                    for tag in filters.tags
                ]
                db_query = db_query.filter(or_(*tag_filters))
        
        # Get all matching content
        all_content = db_query.all()
        
        # Calculate similarity scores for each content item
        scored_content = []
        for content in all_content:
            # Calculate cosine similarity
            similarity = cosine_similarity(query_embedding, content.embedding)
            
            # Only include if above threshold
            if similarity >= settings.SIMILARITY_THRESHOLD:
                scored_content.append({
                    'content': content,
                    'similarity': similarity
                })
        
        # Sort by similarity score (highest first)
        scored_content.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Take top K results
        top_results = scored_content[:top_k]
        
        # Convert to RetrievedContent objects
        retrieved_content = []
        for item in top_results:
            content = item['content']
            retrieved_content.append(
                RetrievedContent(
                    id=content.id,
                    title=content.title,
                    content=content.content,
                    content_type=content.content_type,
                    campaign_name=content.campaign_name,
                    audience=content.audience,
                    compliance_status=content.compliance_status,
                    source=content.source,
                    tags=content.tags,
                    similarity_score=round(item['similarity'], 4)
                )
            )
        
        return retrieved_content
    
    def retrieve_by_id(self, db: Session, content_id: int) -> Optional[RetrievedContent]:
        """
        Retrieve specific content by ID
        
        Args:
            db: Database session
            content_id: Content ID
            
        Returns:
            Retrieved content or None
        """
        content = db.query(MarketingContent).filter(
            MarketingContent.id == content_id
        ).first()
        
        if content:
            return RetrievedContent(
                id=content.id,
                title=content.title,
                content=content.content,
                content_type=content.content_type,
                campaign_name=content.campaign_name,
                audience=content.audience,
                compliance_status=content.compliance_status,
                source=content.source,
                tags=content.tags,
                similarity_score=1.0
            )
        return None
    
    def get_all_content(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[RetrievedContent]:
        """
        Get all content with pagination
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of content
        """
        contents = db.query(MarketingContent).filter(
            MarketingContent.is_active == True
        ).offset(skip).limit(limit).all()
        
        return [
            RetrievedContent(
                id=content.id,
                title=content.title,
                content=content.content,
                content_type=content.content_type,
                campaign_name=content.campaign_name,
                audience=content.audience,
                compliance_status=content.compliance_status,
                source=content.source,
                tags=content.tags,
                similarity_score=0.0
            )
            for content in contents
        ]


# Global retriever instance
_retriever = None


def get_retriever() -> ContentRetriever:
    """Get or create retriever instance"""
    global _retriever
    if _retriever is None:
        _retriever = ContentRetriever()
    return _retriever
