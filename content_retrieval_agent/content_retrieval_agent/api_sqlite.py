"""
FastAPI application for Content Retrieval Agent (SQLite - No Docker needed!)
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

from config import get_settings
from database_sqlite import get_db, MarketingContent
from retrieval_sqlite import get_retriever, ContentFilter, RetrievedContent

settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Retrieve relevant marketing content using semantic search and RAG (SQLite - No Docker!)"
)


# Request/Response Models
class SearchRequest(BaseModel):
    """Search request model"""
    query: str = Field(..., description="Search query", min_length=1)
    content_type: Optional[str] = Field(None, description="Filter by content type (email, social, ad, blog)")
    campaign_name: Optional[str] = Field(None, description="Filter by campaign name")
    audience: Optional[str] = Field(None, description="Filter by audience (B2B, B2C, Enterprise, SMB)")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    top_k: Optional[int] = Field(3, description="Number of results to return", ge=1, le=10)


class SearchResponse(BaseModel):
    """Search response model"""
    query: str
    results_count: int
    results: List[RetrievedContent]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    embedding_model: str
    database: str


# API Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with API information"""
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION,
        embedding_model=settings.EMBEDDING_MODEL,
        database="SQLite (No Docker needed!)"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION,
        embedding_model=settings.EMBEDDING_MODEL,
        database="SQLite (No Docker needed!)"
    )


@app.post("/search", response_model=SearchResponse)
async def search_content(
    request: SearchRequest,
    db: Session = Depends(get_db)
):
    """
    Search for relevant marketing content
    
    This endpoint performs semantic search using vector embeddings
    and returns the most relevant content based on the query.
    """
    try:
        # Create filter object
        filters = ContentFilter(
            content_type=request.content_type,
            campaign_name=request.campaign_name,
            audience=request.audience,
            tags=request.tags
        )
        
        # Retrieve content
        retriever = get_retriever()
        results = retriever.retrieve(
            db=db,
            query=request.query,
            filters=filters,
            top_k=request.top_k
        )
        
        return SearchResponse(
            query=request.query,
            results_count=len(results),
            results=results
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/content/{content_id}", response_model=RetrievedContent)
async def get_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve specific content by ID
    """
    retriever = get_retriever()
    content = retriever.retrieve_by_id(db=db, content_id=content_id)
    
    if not content:
        raise HTTPException(status_code=404, detail=f"Content with ID {content_id} not found")
    
    return content


@app.get("/content", response_model=List[RetrievedContent])
async def list_content(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    List all content with pagination
    """
    retriever = get_retriever()
    contents = retriever.get_all_content(db=db, skip=skip, limit=limit)
    return contents


@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Get statistics about the content library
    """
    from sqlalchemy import func
    
    total_content = db.query(func.count(MarketingContent.id)).scalar()
    
    content_by_type = db.query(
        MarketingContent.content_type,
        func.count(MarketingContent.id).label('count')
    ).group_by(MarketingContent.content_type).all()
    
    content_by_audience = db.query(
        MarketingContent.audience,
        func.count(MarketingContent.id).label('count')
    ).group_by(MarketingContent.audience).all()
    
    return {
        "total_content": total_content,
        "by_content_type": {item[0]: item[1] for item in content_by_type},
        "by_audience": {item[0]: item[1] for item in content_by_audience},
        "embedding_dimension": settings.EMBEDDING_DIMENSION,
        "embedding_model": settings.EMBEDDING_MODEL,
        "database": "SQLite (No Docker needed!)"
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api_sqlite:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
