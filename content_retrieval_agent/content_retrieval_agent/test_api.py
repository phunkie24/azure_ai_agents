"""
Test script for Content Retrieval Agent API
Run this after starting the API server to test functionality
"""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def print_section(title: str):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_result(response: requests.Response):
    """Print formatted API response"""
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")


def test_health_check():
    """Test health check endpoint"""
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_result(response)


def test_stats():
    """Test statistics endpoint"""
    print_section("2. Content Statistics")
    response = requests.get(f"{BASE_URL}/stats")
    print_result(response)


def test_search_email_marketing():
    """Test search for email marketing content"""
    print_section("3. Search: Email Marketing Tips")
    
    payload = {
        "query": "email marketing tips and best practices",
        "top_k": 3
    }
    
    response = requests.post(
        f"{BASE_URL}/search",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_result(response)


def test_search_summer_sale():
    """Test search for summer sale content"""
    print_section("4. Search: Summer Sale Campaign")
    
    payload = {
        "query": "summer promotion discount sale",
        "content_type": "email",
        "top_k": 2
    }
    
    response = requests.post(
        f"{BASE_URL}/search",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_result(response)


def test_search_b2b_content():
    """Test search for B2B content"""
    print_section("5. Search: B2B Enterprise Software")
    
    payload = {
        "query": "enterprise business software solutions",
        "audience": "B2B",
        "top_k": 3
    }
    
    response = requests.post(
        f"{BASE_URL}/search",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_result(response)


def test_search_social_media():
    """Test search for social media content"""
    print_section("6. Search: Social Media Posts")
    
    payload = {
        "query": "social media marketing post",
        "content_type": "social",
        "top_k": 3
    }
    
    response = requests.post(
        f"{BASE_URL}/search",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_result(response)


def test_search_with_tags():
    """Test search with tag filtering"""
    print_section("7. Search: Content with Security Tags")
    
    payload = {
        "query": "data protection and privacy",
        "tags": ["security", "compliance"],
        "top_k": 2
    }
    
    response = requests.post(
        f"{BASE_URL}/search",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_result(response)


def test_get_content_by_id():
    """Test retrieving content by ID"""
    print_section("8. Get Content by ID")
    
    content_id = 1
    response = requests.get(f"{BASE_URL}/content/{content_id}")
    print_result(response)


def test_list_content():
    """Test listing all content with pagination"""
    print_section("9. List All Content (First 5)")
    
    response = requests.get(f"{BASE_URL}/content?skip=0&limit=5")
    print_result(response)


def run_all_tests():
    """Run all test cases"""
    print("\n" + "="*60)
    print("  CONTENT RETRIEVAL AGENT - API TESTS")
    print("="*60)
    print(f"\nTesting API at: {BASE_URL}")
    print("Make sure the API server is running!")
    print("Start with: python api.py")
    
    try:
        test_health_check()
        test_stats()
        test_search_email_marketing()
        test_search_summer_sale()
        test_search_b2b_content()
        test_search_social_media()
        test_search_with_tags()
        test_get_content_by_id()
        test_list_content()
        
        print("\n" + "="*60)
        print("  ✅ ALL TESTS COMPLETED")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server")
        print("Please make sure the API is running:")
        print("  python api.py")
        print()


if __name__ == "__main__":
    run_all_tests()
