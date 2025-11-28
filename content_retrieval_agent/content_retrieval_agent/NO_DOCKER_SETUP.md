# 🚀 NO DOCKER SETUP - Super Simple!

Run the Content Retrieval Agent **without Docker** using SQLite! Perfect for quick testing and development.

## ✨ Why This Version?

- ✅ **No Docker Required** - Just Python!
- ✅ **SQLite Database** - Lightweight, file-based
- ✅ **Same Features** - All RAG functionality works
- ✅ **Faster Setup** - 2 minutes instead of 5
- ✅ **Single File** - Database is just `marketing_content.db`
- ✅ **Perfect for Development** - Easy to reset and test

## 📋 Prerequisites

**ONLY Python 3.8+ needed!**
- No Docker
- No PostgreSQL
- No containers

Check Python version:
```bash
python --version
# or
python3 --version
```

---

## 🚀 Quick Setup (2 Steps!)

### Option 1: Automated Setup

#### On macOS/Linux:
```bash
chmod +x setup_no_docker.sh
./setup_no_docker.sh
```

#### On Windows:
```bash
setup_no_docker.bat
```

**That's it!** Skip to the "Start the API" section below.

---

### Option 2: Manual Setup

#### Step 1: Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements_no_docker.txt
```

#### Step 2: Load Data
```bash
# Create .env file (optional - defaults work)
cp .env.example .env

# Load sample data into SQLite
python ingestion_sqlite.py
```

**Expected output:**
```
🚀 Starting data ingestion process (SQLite - No Docker needed!)...
📊 Initializing SQLite database...
✅ SQLite database initialized successfully!
🤖 Loading embedding model...
✅ Embedding model loaded successfully!
📥 Loading sample data...
⚙️  Ingesting content...
  [1/15] Ingested: Summer Sale Email Campaign
  ...
✅ Successfully ingested 15 content items!
📁 Database location: marketing_content.db
```

---

## 🎯 Start the API

```bash
python api_sqlite.py
```

**Output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Visit: **http://localhost:8000/docs** 🎉

---

## 🧪 Test It

### Quick Test
```bash
# In a new terminal
python test_api.py
```

### Manual Test
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "email marketing tips", "top_k": 3}'
```

### Python Test
```python
import requests

response = requests.post(
    "http://localhost:8000/search",
    json={"query": "summer sale", "top_k": 3}
)

print(response.json())
```

---

## 📂 File Structure (No Docker Version)

```
content_retrieval_agent/
│
├── 🔵 Use These Files (No Docker):
│   ├── api_sqlite.py              # API server (SQLite)
│   ├── database_sqlite.py         # Database models (SQLite)
│   ├── retrieval_sqlite.py        # RAG logic (SQLite)
│   ├── ingestion_sqlite.py        # Data loader (SQLite)
│   ├── requirements_no_docker.txt # Dependencies (no PostgreSQL)
│   ├── setup_no_docker.sh         # Setup script (Mac/Linux)
│   └── setup_no_docker.bat        # Setup script (Windows)
│
├── 📊 Shared Files:
│   ├── embeddings.py              # AI embeddings
│   ├── config.py                  # Settings
│   ├── sample_data.json           # Example data
│   ├── test_api.py                # Tests
│   └── example_client.py          # Integration examples
│
└── 📚 Documentation:
    ├── NO_DOCKER_SETUP.md         # This file
    ├── README.md                  # Full guide
    └── QUICKSTART.md              # Original Docker guide
```

---

## 🔄 Key Differences from Docker Version

| Feature | Docker Version | No Docker Version |
|---------|---------------|-------------------|
| **Database** | PostgreSQL + pgvector | SQLite + JSON |
| **Setup** | Docker Compose | Just Python |
| **Vector Search** | Database-level (fast) | Python-level (good) |
| **Best For** | Production, large scale | Development, testing |
| **Performance** | Excellent (1M+ vectors) | Good (up to 10K vectors) |
| **Deployment** | Requires Docker | Anywhere Python runs |

---

## 💻 Daily Workflow

### Start Working
```bash
# Activate environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Start API
python api_sqlite.py
```

### Stop Working
```bash
# Press Ctrl+C to stop API
# Deactivate environment (optional)
deactivate
```

### Reset Database
```bash
# Delete and recreate
rm marketing_content.db
python ingestion_sqlite.py
```

---

## 📊 Database Info

**File:** `marketing_content.db` (SQLite database)

**Location:** Same directory as your scripts

**Size:** ~2MB (with sample data)

**Backup:** Just copy the `.db` file!
```bash
cp marketing_content.db marketing_content_backup.db
```

**View Data:**
```bash
# Install SQLite browser or use CLI
sqlite3 marketing_content.db
sqlite> SELECT title FROM marketing_content LIMIT 5;
```

---

## 🎮 Usage Examples

### Example 1: Search
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "B2B software",
    "audience": "B2B",
    "top_k": 3
  }'
```

### Example 2: Get by ID
```bash
curl http://localhost:8000/content/1
```

### Example 3: List All
```bash
curl "http://localhost:8000/content?limit=5"
```

### Example 4: Statistics
```bash
curl http://localhost:8000/stats
```

---

## 🔧 Troubleshooting

### ❌ "Module not found"
**Fix:** Activate virtual environment
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### ❌ "Database is locked"
**Fix:** Close other connections to the database
```bash
# Stop the API and restart
```

### ❌ Port 8000 in use
**Fix:** Use different port
```bash
python api_sqlite.py --port 8001
# Or edit .env file
```

### ❌ Slow searches
**Normal:** First search loads the AI model (~5 seconds)
Subsequent searches are fast (<100ms)

---

## ⚡ Performance Tips

### For Faster Searches:
1. Keep the API running (model stays in memory)
2. Use specific filters (type, audience, tags)
3. Lower `top_k` for faster results

### For More Data:
SQLite works well up to **10,000 items**. Beyond that:
- Consider the Docker version with PostgreSQL
- Or implement pagination and caching

---

## 🚀 Upgrade to Docker Version

When ready for production:

1. **Install Docker Desktop**
2. **Use original files:**
   - `api.py` (instead of `api_sqlite.py`)
   - `database.py` (instead of `database_sqlite.py`)
   - `retrieval.py` (instead of `retrieval_sqlite.py`)
3. **Follow:** `QUICKSTART.md`

Your data model is the same, so migration is easy!

---

## 📝 Adding Your Own Content

### Method 1: Edit JSON
1. Open `sample_data.json`
2. Add your content items
3. Run: `python ingestion_sqlite.py`

### Method 2: Python Script
```python
from database_sqlite import SessionLocal, MarketingContent
from embeddings import get_embedding_generator

db = SessionLocal()
gen = get_embedding_generator()

content = MarketingContent(
    title="My New Content",
    content="Content text here...",
    content_type="email",
    audience="B2B",
    compliance_status="approved",
    embedding=gen.generate_embedding("My New Content text...")
)

db.add(content)
db.commit()
db.close()
```

---

## ✅ What Works Without Docker

✅ All API endpoints  
✅ Semantic search  
✅ Metadata filtering  
✅ Compliance tracking  
✅ Source citations  
✅ Integration with Message Gen Agent  
✅ All documentation and examples  

The **only difference** is the database technology - everything else is identical!

---

## 🎉 You're Ready!

```bash
# Start the API
python api_sqlite.py

# Open browser
http://localhost:8000/docs

# Start building!
```

**No Docker, no complexity - just Python and SQLite!** 🚀

---

## 📚 Next Steps

1. ✅ **Complete this setup**
2. 🔍 **Try searches** at `/docs`
3. 💻 **Run** `example_client.py`
4. 📖 **Read** `README.md` for integration
5. 🎯 **Add** your own content

---

**Questions?** Check `README.md` or `PROJECT_OVERVIEW.md` for more details!
