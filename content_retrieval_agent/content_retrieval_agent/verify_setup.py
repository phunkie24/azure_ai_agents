"""
Setup verification script
Run this to check if your Content Retrieval Agent is properly configured
"""
import sys
import subprocess
import importlib.util


def check_item(name: str, check_func, fix_suggestion: str = ""):
    """Check a single setup item"""
    try:
        result = check_func()
        if result:
            print(f"✅ {name}")
            return True
        else:
            print(f"❌ {name}")
            if fix_suggestion:
                print(f"   Fix: {fix_suggestion}")
            return False
    except Exception as e:
        print(f"❌ {name}")
        print(f"   Error: {e}")
        if fix_suggestion:
            print(f"   Fix: {fix_suggestion}")
        return False


def check_python_version():
    """Check Python version >= 3.8"""
    version = sys.version_info
    return version.major == 3 and version.minor >= 8


def check_module(module_name: str):
    """Check if a Python module is installed"""
    return importlib.util.find_spec(module_name) is not None


def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def check_docker_compose():
    """Check if Docker Compose is available"""
    try:
        result = subprocess.run(
            ["docker-compose", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def check_postgres_running():
    """Check if PostgreSQL container is running"""
    try:
        result = subprocess.run(
            ["docker-compose", "ps"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return "marketing_content_db" in result.stdout and "Up" in result.stdout
    except:
        return False


def check_env_file():
    """Check if .env file exists"""
    import os
    return os.path.exists(".env")


def check_database_connection():
    """Check if can connect to database"""
    try:
        from config import get_settings
        from sqlalchemy import create_engine
        
        settings = get_settings()
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except:
        return False


def check_embedding_model():
    """Check if embedding model can be loaded"""
    try:
        from embeddings import get_embedding_generator
        generator = get_embedding_generator()
        # Try a simple embedding
        generator.generate_embedding("test")
        return True
    except:
        return False


def check_database_tables():
    """Check if database tables exist"""
    try:
        from database import SessionLocal, MarketingContent
        db = SessionLocal()
        count = db.query(MarketingContent).count()
        db.close()
        return count > 0
    except:
        return False


def main():
    """Run all setup checks"""
    print("="*60)
    print("  CONTENT RETRIEVAL AGENT - SETUP VERIFICATION")
    print("="*60)
    print()
    
    checks = []
    
    # Python version
    checks.append(check_item(
        "Python 3.8+",
        check_python_version,
        "Install Python 3.8 or higher"
    ))
    
    # Core dependencies
    print("\n📦 Checking Python Dependencies:")
    checks.append(check_item(
        "FastAPI installed",
        lambda: check_module("fastapi"),
        "Run: pip install -r requirements.txt"
    ))
    checks.append(check_item(
        "SQLAlchemy installed",
        lambda: check_module("sqlalchemy"),
        "Run: pip install -r requirements.txt"
    ))
    checks.append(check_item(
        "Sentence Transformers installed",
        lambda: check_module("sentence_transformers"),
        "Run: pip install -r requirements.txt"
    ))
    checks.append(check_item(
        "pgvector installed",
        lambda: check_module("pgvector"),
        "Run: pip install -r requirements.txt"
    ))
    
    # Docker
    print("\n🐳 Checking Docker:")
    checks.append(check_item(
        "Docker installed",
        check_docker,
        "Install Docker Desktop from https://docker.com"
    ))
    checks.append(check_item(
        "Docker Compose installed",
        check_docker_compose,
        "Install Docker Desktop (includes Compose)"
    ))
    
    # Configuration
    print("\n⚙️  Checking Configuration:")
    checks.append(check_item(
        ".env file exists",
        check_env_file,
        "Run: cp .env.example .env"
    ))
    
    # Database
    print("\n🐘 Checking Database:")
    checks.append(check_item(
        "PostgreSQL container running",
        check_postgres_running,
        "Run: docker-compose up -d"
    ))
    
    if checks[-1]:  # Only check connection if PostgreSQL is running
        checks.append(check_item(
            "Database connection works",
            check_database_connection,
            "Check DATABASE_URL in .env"
        ))
        checks.append(check_item(
            "Data ingested",
            check_database_tables,
            "Run: python ingestion.py"
        ))
    
    # Embedding model
    print("\n🤖 Checking AI Model:")
    checks.append(check_item(
        "Embedding model loads",
        check_embedding_model,
        "First time takes ~30s to download"
    ))
    
    # Summary
    print("\n" + "="*60)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("="*60)
        print("\n🚀 Ready to start the API!")
        print("\nNext steps:")
        print("  1. python api.py")
        print("  2. Visit http://localhost:8000/docs")
        print("  3. python test_api.py")
    else:
        print(f"⚠️  SOME CHECKS FAILED ({passed}/{total} passed)")
        print("="*60)
        print("\n📝 Follow the 'Fix' suggestions above")
        print("\nCommon fixes:")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("  • Start database: docker-compose up -d")
        print("  • Create .env: cp .env.example .env")
        print("  • Ingest data: python ingestion.py")
    
    print()


if __name__ == "__main__":
    main()
