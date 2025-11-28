"""
Example client demonstrating how a Message Generation Agent
would interact with the Content Retrieval Agent API
"""
import requests
from typing import List, Dict, Any


class ContentRetrieverClient:
    """Client for Content Retrieval Agent API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize client
        
        Args:
            base_url: Base URL of the Content Retrieval API
        """
        self.base_url = base_url
    
    def search_content(
        self,
        query: str,
        content_type: str = None,
        audience: str = None,
        tags: List[str] = None,
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Search for relevant content
        
        Args:
            query: Search query
            content_type: Filter by content type (email, social, ad, blog)
            audience: Filter by audience (B2B, B2C, Enterprise, SMB)
            tags: List of tags to filter by
            top_k: Number of results to return
            
        Returns:
            Dictionary with search results
        """
        payload = {
            "query": query,
            "top_k": top_k
        }
        
        if content_type:
            payload["content_type"] = content_type
        if audience:
            payload["audience"] = audience
        if tags:
            payload["tags"] = tags
        
        response = requests.post(
            f"{self.base_url}/search",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        response.raise_for_status()
        return response.json()
    
    def get_content_by_id(self, content_id: int) -> Dict[str, Any]:
        """
        Get specific content by ID
        
        Args:
            content_id: Content ID
            
        Returns:
            Content details
        """
        response = requests.get(f"{self.base_url}/content/{content_id}")
        response.raise_for_status()
        return response.json()
    
    def format_results_for_llm(self, search_results: Dict[str, Any]) -> str:
        """
        Format search results as context for an LLM
        
        Args:
            search_results: Results from search_content()
            
        Returns:
            Formatted string for LLM context
        """
        results = search_results.get("results", [])
        
        if not results:
            return "No relevant content found."
        
        context = "Relevant Marketing Content:\n\n"
        
        for idx, result in enumerate(results, 1):
            context += f"--- Content {idx} ---\n"
            context += f"Title: {result['title']}\n"
            context += f"Type: {result['content_type']}\n"
            context += f"Audience: {result['audience']}\n"
            context += f"Content: {result['content']}\n"
            context += f"Source: {result['source']}\n"
            context += f"Similarity Score: {result['similarity_score']}\n"
            context += "\n"
        
        return context


def example_use_case_1():
    """Example: Search for email marketing content"""
    print("="*60)
    print("Example 1: Search for Email Marketing Content")
    print("="*60)
    
    client = ContentRetrieverClient()
    
    # Search for email content about promotions
    results = client.search_content(
        query="promotional email for sale event",
        content_type="email",
        audience="B2C",
        top_k=3
    )
    
    print(f"\nQuery: {results['query']}")
    print(f"Found {results['results_count']} results\n")
    
    for idx, result in enumerate(results['results'], 1):
        print(f"{idx}. {result['title']}")
        print(f"   Type: {result['content_type']} | Audience: {result['audience']}")
        print(f"   Similarity: {result['similarity_score']}")
        print(f"   Preview: {result['content'][:100]}...")
        print()


def example_use_case_2():
    """Example: Format results for LLM context"""
    print("="*60)
    print("Example 2: Format Results for Message Generation")
    print("="*60)
    
    client = ContentRetrieverClient()
    
    # Search for B2B content
    results = client.search_content(
        query="enterprise software solution",
        audience="B2B",
        top_k=2
    )
    
    # Format for LLM
    llm_context = client.format_results_for_llm(results)
    
    print("\nFormatted Context for LLM:")
    print("-" * 60)
    print(llm_context)
    
    # Simulate how a Message Generation Agent would use this
    print("\n📝 Message Generation Agent would now use this context to:")
    print("   1. Understand the tone and style of approved content")
    print("   2. Extract key messaging points")
    print("   3. Generate new content matching the brand voice")
    print("   4. Ensure compliance with approved templates")


def example_use_case_3():
    """Example: Multi-filter search"""
    print("="*60)
    print("Example 3: Advanced Search with Multiple Filters")
    print("="*60)
    
    client = ContentRetrieverClient()
    
    # Complex search with multiple filters
    results = client.search_content(
        query="security and data protection",
        tags=["security", "compliance"],
        audience="Enterprise",
        top_k=2
    )
    
    print(f"\nQuery: {results['query']}")
    print(f"Filters: audience=Enterprise, tags=['security', 'compliance']")
    print(f"Found {results['results_count']} results\n")
    
    for result in results['results']:
        print(f"✓ {result['title']}")
        print(f"  Campaign: {result['campaign_name']}")
        print(f"  Compliance: {result['compliance_status']}")
        print(f"  Score: {result['similarity_score']}")
        print()


def example_integration_workflow():
    """Example: Full integration workflow"""
    print("="*60)
    print("Example 4: Complete Message Generation Workflow")
    print("="*60)
    
    client = ContentRetrieverClient()
    
    # Step 1: Retrieve relevant approved content
    print("\n[Step 1] Retrieving relevant approved content...")
    results = client.search_content(
        query="product launch announcement",
        content_type="social",
        audience="B2B",
        top_k=2
    )
    
    print(f"✓ Retrieved {results['results_count']} approved content items")
    
    # Step 2: Extract key elements
    print("\n[Step 2] Extracting key messaging elements...")
    for result in results['results']:
        print(f"  - {result['title']}")
        print(f"    Tone: Professional B2B")
        print(f"    Compliance: {result['compliance_status']}")
    
    # Step 3: Format context for LLM
    print("\n[Step 3] Formatting context for Message Generation Agent...")
    context = client.format_results_for_llm(results)
    print("✓ Context prepared for LLM")
    
    # Step 4: Simulate message generation
    print("\n[Step 4] Message Generation Agent would now:")
    print("  → Analyze the retrieved content patterns")
    print("  → Maintain compliance standards")
    print("  → Generate new message using approved style")
    print("  → Include proper citations and sources")
    
    print("\n✅ Integration workflow complete!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  CONTENT RETRIEVAL AGENT - CLIENT EXAMPLES")
    print("="*60)
    print("\nMake sure the API is running: python api.py\n")
    
    try:
        # Run all examples
        example_use_case_1()
        print("\n")
        
        example_use_case_2()
        print("\n")
        
        example_use_case_3()
        print("\n")
        
        example_integration_workflow()
        
        print("\n" + "="*60)
        print("  ✅ ALL EXAMPLES COMPLETED")
        print("="*60)
        print("\nThese examples show how a Message Generation Agent")
        print("would interact with the Content Retrieval Agent API.\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server")
        print("Please start the API first: python api.py\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
