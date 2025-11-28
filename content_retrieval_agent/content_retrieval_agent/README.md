# 🧩 Content Retrieval Agent

A production-ready RAG (Retrieval-Augmented Generation) system for retrieving marketing content using semantic search with vector embeddings.

## 🏗️ Architecture

```
┌─────────────────┐
│  FastAPI Server │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼───┐  ┌──▼──────────┐
│ Search│  │ PostgreSQL  │
│ Logic │  │ + pgvector  │
└───┬───┘  └─────────────┘
    │
┌───▼──────────────┐
│ Sentence         │
│ Transformers     │
│ (Embeddings)     │
└──────────────────┘
```

## ✨ Features

- **Semantic Search**: Vector-based similarity search using embeddings
- **Metadata Filtering**: Filter by content type, campaign, audience, tags
- **Compliance Tracking**: Track approval status of content
- **RESTful API**: Clean FastAPI interface for integration
- **Modular Design**: Easy to extend and customize
- **Production Ready**: PostgreSQL with pgvector for scalable vector search

## 📋 Prerequisites

- Python 3.8+
- Docker & Docker Compose (for PostgreSQL)
- 2GB RAM minimum
- 5GB disk space (for models and data)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Start PostgreSQL

```bash
# Start PostgreSQL with pgvector
docker-compose up -d

# Check if running
docker-compose ps
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit if needed (defaults work out of the box)
```

### 4. Ingest Sample Data

```bash
# This will:
# - Initialize database with pgvector extension
# - Create tables
# - Load embedding model
# - Ingest 15 sample marketing content items
python ingestion.py
```

Expected output:
```
🚀 Starting data ingestion process...
📊 Initializing database...
✅ Database initialized successfully!
🤖 Loading embedding model...
✅ Embedding model loaded successfully!
📥 Loading sample data...
Found 15 content items to ingest
⚙️  Ingesting content...
  [1/15] Ingested: Summer Sale Email Campaign
  ...
✅ Successfully ingested 15 content items!
```

### 5. Start API Server

```bash
# Start the FastAPI server
python api.py

# Or use uvicorn directly
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test the API

Open your browser: **http://localhost:8000/docs**

Or use curl:
```bash
# Health check
curl http://localhost:8000/health

# Search for content
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "email marketing tips",
    "top_k": 3
  }'

# Get statistics
curl http://localhost:8000/stats
```

## 📚 API Endpoints

### `POST /search`
Search for relevant content using semantic search.

**Request:**
```json
{
  "query": "email campaign for summer sale",
  "content_type": "email",
  "audience": "B2C",
  "tags": ["sale", "promotion"],
  "top_k": 3
}
```

**Response:**
```json
{
  "query": "email campaign for summer sale",
  "results_count": 3,
  "results": [
    {
      "id": 1,
      "title": "Summer Sale Email Campaign",
      "content": "🌞 Summer Savings Are Here!...",
      "content_type": "email",
      "campaign_name": "Summer 2024 Promotion",
      "audience": "B2C",
      "compliance_status": "approved",
      "source": "Marketing Team - Q2 Campaign",
      "tags": "sale, promotion, discount, summer",
      "similarity_score": 0.8523
    }
  ]
}
```

### `GET /content/{id}`
Get specific content by ID.

### `GET /content?skip=0&limit=10`
List all content with pagination.

### `GET /stats`
Get statistics about the content library.

### `GET /health`
Health check endpoint.

## 🔧 Configuration

Edit `.env` file to customize:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/marketing_content

# Embedding Model (Options: all-MiniLM-L6-v2, bge-large-en-v1.5, etc.)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# Retrieval
TOP_K_RESULTS=3
SIMILARITY_THRESHOLD=0.5  # Minimum similarity score (0-1)
```

## 📂 Project Structure

```
content_retrieval_agent/
├── api.py                 # FastAPI application & endpoints
├── config.py              # Configuration management
├── database.py            # Database models & connection
├── embeddings.py          # Embedding generation logic
├── ingestion.py           # Data ingestion script
├── retrieval.py           # RAG retrieval logic
├── sample_data.json       # Sample marketing content
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # PostgreSQL setup
├── .env.example          # Environment configuration template
└── README.md             # This file
```

## 🎯 Use Cases

1. **Message Generation Agent Integration**
   - Call `/search` endpoint with topic/audience
   - Get top 3 relevant approved content
   - Use as context for message generation

2. **Content Discovery**
   - Search marketing library by keywords
   - Filter by campaign, audience, content type
   - Find compliant, approved content only

3. **Campaign Research**
   - Find similar past campaigns
   - Analyze successful content patterns
   - Reuse proven messaging

## 🔄 Adding New Content

### Via Python:
```python
from database import SessionLocal, MarketingContent
from embeddings import get_embedding_generator

db = SessionLocal()
embedding_gen = get_embedding_generator()

# Create new content
text = "Your new marketing content..."
embedding = embedding_gen.generate_embedding(text)

content = MarketingContent(
    title="New Campaign",
    content=text,
    content_type="email",
    audience="B2B",
    compliance_status="approved",
    embedding=embedding
)

db.add(content)
db.commit()
```

### Via JSON:
Add to `sample_data.json` and run `python ingestion.py`

## 🧪 Testing Examples

```bash
# Search for email content
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "promotional email", "content_type": "email"}'

# Search for B2B content
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "enterprise software", "audience": "B2B"}'

# Search with tags
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "social media", "tags": ["linkedin", "B2B"]}'
```

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
docker-compose ps

# Restart PostgreSQL
docker-compose restart
```

### Embedding Model Download Issues
```bash
# Models download automatically on first run
# Check internet connection and disk space
# Default model size: ~80MB
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 📊 Performance

- **Ingestion**: ~2 seconds per content item (including embedding generation)
- **Search**: <100ms for semantic search on 1000 items
- **Memory**: ~500MB (model loaded in memory)
- **Scalability**: PostgreSQL pgvector handles millions of vectors

## 🔐 Security Notes

- Change default PostgreSQL credentials in production
- Add authentication to API endpoints
- Use HTTPS in production
- Validate and sanitize all inputs
- Implement rate limiting

## 🚀 Production Deployment

1. Use production-grade database credentials
2. Set up proper logging
3. Add authentication (OAuth2, API keys)
4. Use a reverse proxy (Nginx)
5. Enable CORS properly
6. Add monitoring (Prometheus, Grafana)
7. Implement caching (Redis)

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

This is a modular template. Extend it by:
- Adding more metadata fields
- Implementing custom ranking algorithms
- Adding cache layers
- Creating admin endpoints
- Building a frontend interface

## 📧 Support

For issues or questions, check the FastAPI docs at `/docs` endpoint!

---

**Built with ❤️ using FastAPI, PostgreSQL, pgvector, and Sentence Transformers**
