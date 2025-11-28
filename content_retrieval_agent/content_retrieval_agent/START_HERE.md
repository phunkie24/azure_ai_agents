# 🚀 START HERE - Content Retrieval Agent

Welcome! This is a **production-ready RAG system** for retrieving marketing content using AI-powered semantic search.

## ⚡ Quick Decision

### Want the fastest setup? (Recommended for beginners)
👉 **[NO_DOCKER_SETUP.md](NO_DOCKER_SETUP.md)** - 2 minutes, Python only, SQLite

### Need production-grade performance?
👉 **[QUICKSTART.md](QUICKSTART.md)** - 5 minutes, Docker + PostgreSQL

### Not sure which?
👉 **[WHICH_VERSION.md](WHICH_VERSION.md)** - Compare and decide

---

## 🎯 What This Does

A **smart content retrieval system** that:

1. **Stores** marketing content (emails, ads, social posts, blogs)
2. **Indexes** content using AI embeddings
3. **Searches** semantically (understands meaning, not just keywords)
4. **Returns** top 3 relevant items with citations
5. **Filters** by type, audience, campaign, compliance status
6. **Provides** REST API for easy integration

### Example Query:
```
Query: "email marketing tips for B2B"
↓
Returns: Top 3 relevant approved content with similarity scores
```

---

## 📦 Two Versions Available

### 🟢 No Docker (SQLite) - **Recommended to Start**
- **Setup:** 2 minutes
- **Needs:** Python only
- **Best for:** Learning, development, testing
- **Data:** Up to 10K items
- **Guide:** [NO_DOCKER_SETUP.md](NO_DOCKER_SETUP.md)

```bash
./setup_no_docker.sh      # One command!
python api_sqlite.py      # Start API
```

### 🔵 Docker (PostgreSQL) - **Production Ready**
- **Setup:** 5 minutes
- **Needs:** Python + Docker
- **Best for:** Production, scale
- **Data:** Millions of items
- **Guide:** [QUICKSTART.md](QUICKSTART.md)

```bash
./setup.sh               # One command!
python api.py            # Start API
```

---

## 📚 Documentation Guide

| Document | Purpose | Read When |
|----------|---------|-----------|
| **START_HERE.md** | Main entry point | First! (you are here) |
| **NO_DOCKER_SETUP.md** | SQLite setup | Want simple setup |
| **QUICKSTART.md** | Docker setup | Want production setup |
| **WHICH_VERSION.md** | Compare versions | Undecided |
| **README.md** | Full documentation | Need details |
| **PROJECT_OVERVIEW.md** | Project structure | Want to understand |
| **ARCHITECTURE.md** | Technical details | Deep dive |

---

## 🚀 Get Started in 3 Steps

### Step 1: Choose Your Version
- **New to this?** → Use No Docker (SQLite)
- **Production?** → Use Docker (PostgreSQL)
- **Unsure?** → Read [WHICH_VERSION.md](WHICH_VERSION.md)

### Step 2: Follow Setup Guide
- **No Docker:** [NO_DOCKER_SETUP.md](NO_DOCKER_SETUP.md)
- **Docker:** [QUICKSTART.md](QUICKSTART.md)

### Step 3: Test It!
```bash
# Visit the API docs
http://localhost:8000/docs

# Or run tests
python test_api.py

# Or try example client
python example_client.py
```

---

## ✨ Key Features

✅ **Semantic Search** - AI understands meaning, not just keywords  
✅ **Metadata Filtering** - Filter by type, audience, campaign, tags  
✅ **Compliance Tracking** - Only returns approved content  
✅ **Source Citations** - Every result includes attribution  
✅ **REST API** - Easy integration with any application  
✅ **Open Source** - PostgreSQL or SQLite, Sentence Transformers  
✅ **Production Ready** - Modular, tested, documented  

---

## 🎯 Use Cases

### 1. Message Generation Agent Integration
```python
# Your Message Generation Agent queries this API
response = requests.post("http://localhost:8000/search", json={
    "query": "B2B software launch email",
    "audience": "B2B",
    "content_type": "email",
    "top_k": 3
})

# Use results as context for generation
results = response.json()
# → Generate new content based on approved examples
```

### 2. Content Discovery
- Search marketing library by topic
- Find similar past campaigns
- Filter by audience and compliance

### 3. Compliance Checking
- Ensure new content matches approved patterns
- Compare against compliant examples
- Verify tone and messaging

---

## 📊 Sample Data Included

**15 realistic marketing content examples:**
- 📧 Email campaigns (B2B, B2C)
- 📱 Social media posts (LinkedIn, Instagram)
- 📢 Ads (Google, Facebook)
- 📝 Blog posts and guides

All with metadata: type, audience, campaign, compliance status, tags

---

## 🔧 Tech Stack

### No Docker Version:
- **API:** FastAPI
- **Database:** SQLite
- **AI:** Sentence Transformers
- **Search:** Python-based similarity

### Docker Version:
- **API:** FastAPI
- **Database:** PostgreSQL + pgvector
- **AI:** Sentence Transformers
- **Search:** Database-level vector search

---

## 📁 Project Structure

```
content_retrieval_agent/
│
├── 🟢 No Docker Files
│   ├── api_sqlite.py
│   ├── database_sqlite.py
│   ├── retrieval_sqlite.py
│   ├── ingestion_sqlite.py
│   ├── requirements_no_docker.txt
│   └── setup_no_docker.sh/bat
│
├── 🔵 Docker Files
│   ├── api.py
│   ├── database.py
│   ├── retrieval.py
│   ├── ingestion.py
│   ├── requirements.txt
│   ├── docker-compose.yml
│   └── setup.sh/bat
│
├── 📦 Shared Files
│   ├── embeddings.py
│   ├── config.py
│   ├── sample_data.json
│   ├── test_api.py
│   ├── example_client.py
│   └── verify_setup.py
│
└── 📚 Documentation
    ├── START_HERE.md (you are here!)
    ├── NO_DOCKER_SETUP.md
    ├── QUICKSTART.md
    ├── WHICH_VERSION.md
    ├── README.md
    ├── PROJECT_OVERVIEW.md
    └── ARCHITECTURE.md
```

---

## 🧪 Quick Test After Setup

```python
import requests

# Search for content
response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "email marketing tips",
        "top_k": 3
    }
)

# Print results
results = response.json()
print(f"Found {results['results_count']} results:")
for item in results['results']:
    print(f"- {item['title']} (score: {item['similarity_score']})")
```

---

## 💡 Recommendations

### 👨‍💻 If you're learning or prototyping:
**→ Use No Docker (SQLite)** - [NO_DOCKER_SETUP.md](NO_DOCKER_SETUP.md)
- Faster setup
- Simpler to understand
- Everything in one file

### 🚀 If you're building for production:
**→ Use Docker (PostgreSQL)** - [QUICKSTART.md](QUICKSTART.md)
- Better performance
- Scales to millions
- Industry standard

### 🎯 If you want both:
**→ Start with No Docker, upgrade when needed**
- Learn quickly with SQLite
- Upgrade to PostgreSQL later
- Data model is compatible

---

## ✅ Next Steps

1. **Read** [WHICH_VERSION.md](WHICH_VERSION.md) to compare options
2. **Follow** either:
   - [NO_DOCKER_SETUP.md](NO_DOCKER_SETUP.md) ← Recommended!
   - [QUICKSTART.md](QUICKSTART.md)
3. **Test** with `python test_api.py`
4. **Explore** `example_client.py` for integration
5. **Customize** with your own content

---

## 🎉 You're Ready!

Pick your version and get started:

### 🟢 Simple & Fast (Recommended)
```bash
./setup_no_docker.sh
python api_sqlite.py
```
→ **[NO_DOCKER_SETUP.md](NO_DOCKER_SETUP.md)**

### 🔵 Production Grade
```bash
./setup.sh
python api.py
```
→ **[QUICKSTART.md](QUICKSTART.md)**

---

**Need Help?** All documentation is in the folder. Start with the setup guide for your chosen version!

**Questions?** Check [README.md](README.md) for comprehensive documentation.

---

<div align="center">

**Built with ❤️ using FastAPI, SQLite/PostgreSQL, and Sentence Transformers**

🚀 **Start your RAG journey now!** 🚀

</div>
