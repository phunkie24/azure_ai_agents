# 🚀 QUICKSTART GUIDE

Get your Content Retrieval Agent running in 5 minutes!

## Prerequisites

- ✅ Python 3.8 or higher
- ✅ Docker Desktop (for PostgreSQL)
- ✅ 2GB free RAM
- ✅ Internet connection (to download models)

## Step-by-Step Setup

### Option 1: Automated Setup (Recommended)

#### On macOS/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

#### On Windows:
```bash
setup.bat
```

The script will automatically:
1. Create virtual environment
2. Install dependencies
3. Start PostgreSQL
4. Ingest sample data

---

### Option 2: Manual Setup

#### 1. Create Virtual Environment
```bash
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Start PostgreSQL
```bash
docker-compose up -d
```

Wait 10 seconds for PostgreSQL to start.

#### 4. Configure Environment (Optional)
```bash
cp .env.example .env
# Edit .env if needed (defaults work fine)
```

#### 5. Ingest Sample Data
```bash
python ingestion.py
```

**Expected output:**
```
🚀 Starting data ingestion process...
✅ Database initialized successfully!
✅ Embedding model loaded successfully!
✅ Successfully ingested 15 content items!
```

This takes ~30 seconds (downloads embedding model first time).

---

## Running the API

### Start the Server
```bash
python api.py
```

**You should see:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test the API

**Open your browser:**
- 📖 **API Documentation**: http://localhost:8000/docs
- 🔍 **Try searches interactively**

**Or use the test script:**
```bash
# In a new terminal (keep API running)
python test_api.py
```

**Or use curl:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "email marketing tips", "top_k": 3}'
```

---

## Quick Examples

### Example 1: Search for Email Content
```python
import requests

response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "summer sale promotional email",
        "content_type": "email",
        "top_k": 3
    }
)

results = response.json()
print(f"Found {results['results_count']} relevant emails")
```

### Example 2: Search with Audience Filter
```python
response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "enterprise software solution",
        "audience": "B2B",
        "top_k": 3
    }
)
```

### Example 3: Get Content by ID
```python
response = requests.get("http://localhost:8000/content/1")
content = response.json()
print(content['title'])
```

---

## Integration with Message Generation Agent

```python
from example_client import ContentRetrieverClient

# Initialize client
client = ContentRetrieverClient()

# Search for relevant content
results = client.search_content(
    query="product launch announcement",
    content_type="social",
    audience="B2B",
    top_k=3
)

# Format for LLM context
context = client.format_results_for_llm(results)

# Now pass 'context' to your Message Generation Agent
# along with the user's request
```

See `example_client.py` for complete integration examples.

---

## API Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/search` | POST | Semantic search for content |
| `/content/{id}` | GET | Get specific content by ID |
| `/content` | GET | List all content (paginated) |
| `/stats` | GET | Get library statistics |
| `/health` | GET | Health check |

---

## Common Issues & Solutions

### ❌ "Connection refused" error
**Solution:** PostgreSQL isn't running
```bash
docker-compose up -d
```

### ❌ "Module not found" error
**Solution:** Activate virtual environment
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### ❌ Slow first search
**Solution:** Normal! Embedding model loads on first use (~30 seconds)

### ❌ Port 8000 already in use
**Solution:** Change port in `.env`
```
API_PORT=8001
```

---

## What's Next?

### 1. Add Your Own Content
Edit `sample_data.json` and run:
```bash
python ingestion.py
```

### 2. Customize Settings
Edit `.env` file:
```env
TOP_K_RESULTS=5              # Return more results
SIMILARITY_THRESHOLD=0.3     # Lower threshold for more results
EMBEDDING_MODEL=...          # Use different model
```

### 3. Integrate with Your App
See `example_client.py` for integration patterns

### 4. Deploy to Production
- Add authentication
- Use production database
- Add monitoring
- Enable HTTPS

---

## Architecture at a Glance

```
User Query
    ↓
[FastAPI Server] → [Sentence Transformers]
    ↓                   ↓
    ↓              (Generate Embeddings)
    ↓                   ↓
[PostgreSQL + pgvector] ← (Vector Search)
    ↓
[Return Top 3 Results with Citations]
```

---

## Need Help?

- 📖 Read the full README.md
- 🔍 Check API docs at http://localhost:8000/docs
- 🧪 Run test_api.py for examples
- 💻 See example_client.py for integration code

---

**🎉 You're ready to go! Happy building!**
