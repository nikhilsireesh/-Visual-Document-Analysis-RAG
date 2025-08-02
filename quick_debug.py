#!/usr/bin/env python3
"""
Quick debug script to test the current system with actual queries.
"""

import logging
import sys

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from src.config import Config
from src.document_processor import DocumentProcessor
from src.rag_system import RAGSystem

def test_current_system():
    """Test the current system with existing documents."""
    print("🔍 Testing current system...")
    
    config = Config()
    doc_processor = DocumentProcessor(config)
    rag_system = RAGSystem(config, doc_processor)
    
    # Check current state
    doc_count = rag_system.get_document_count()
    chunk_count = rag_system.get_chunk_count()
    
    print(f"📊 Current state:")
    print(f"   Documents: {doc_count}")
    print(f"   Chunks: {chunk_count}")
    
    if chunk_count == 0:
        print("❌ No documents in database. Please upload documents first.")
        return
    
    # Test various queries
    test_queries = [
        "what is the title",
        "mathematics",
        "equation",
        "graph",
        "title",
        "content",
        "text"
    ]
    
    print("\n🔍 Testing queries:")
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        try:
            result = rag_system.query(query)
            sources_count = len(result.get('sources', []))
            answer = result.get('answer', 'No answer')[:100]
            
            print(f"   Answer: {answer}...")
            print(f"   Sources: {sources_count}")
            
            if sources_count > 0:
                print("   ✅ Query working!")
                break
            else:
                print("   ❌ No sources found")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    test_current_system()
