#!/usr/bin/env python3
"""
Debug script to test document processing and identify extraction issues.
"""

import sys
import logging
import tempfile
from pathlib import Path

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import our modules
from src.document_processor import DocumentProcessor
from src.rag_system import RAGSystem
from src.config import Config

def test_extraction():
    """Test document extraction with detailed logging."""
    print("🔍 Starting extraction test...")
    
    # Initialize components
    config = Config()
    doc_processor = DocumentProcessor(config)
    rag_system = RAGSystem(config, doc_processor)
    
    # Create a simple test document
    test_content = """
    # Test Document
    
    This is a test document with multiple elements:
    
    ## Section 1: Introduction
    This document contains text, tables, and other elements to test extraction.
    
    ## Section 2: Data
    Here's some sample data:
    - Item 1: Value A
    - Item 2: Value B
    - Item 3: Value C
    
    ## Table Example
    | Name | Age | City |
    |------|-----|------|
    | John | 25  | NYC  |
    | Jane | 30  | LA   |
    | Bob  | 35  | CHI  |
    
    ## Conclusion
    This document should be processed successfully.
    """
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
        tmp_file.write(test_content)
        tmp_file_path = tmp_file.name
    
    try:
        print(f"📄 Processing file: {tmp_file_path}")
        
        # Process document with detailed logging
        doc_result = doc_processor.process_document(
            tmp_file_path,
            use_ocr=True,
            extract_tables=True,
            extract_charts=True
        )
        
        doc_data = doc_result['elements']
        
        print(f"✅ Document processed successfully!")
        print(f"📊 Extracted {len(doc_data)} elements:")
        
        for i, element in enumerate(doc_data):
            print(f"  {i+1}. Type: {element.element_type}")
            print(f"     Content preview: {element.content[:100]}...")
            if element.metadata:
                print(f"     Metadata: {element.metadata}")
            print()
        
        # Test adding to RAG system
        print("🔄 Adding to RAG system...")
        rag_system.add_document(doc_result, "test_document.txt")
        
        # Test querying
        print("❓ Testing query...")
        print("📊 Database stats:")
        print(f"   Documents: {rag_system.get_document_count()}")
        print(f"   Chunks: {rag_system.get_chunk_count()}")
        
        # Let's test with a more specific query that should match
        test_queries = [
            "What is in the table?",
            "test document", 
            "Section 1",
            "introduction"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: '{query}'")
            result = rag_system.query(query)
            print(f"   🤖 Answer: {result.get('answer', 'No answer')[:100]}...")
            print(f"   📚 Sources: {len(result.get('sources', []))} found")
            
            if result.get('sources'):
                for i, source in enumerate(result['sources']):
                    print(f"      Source {i+1}: {source.get('content', '')[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Clean up
        Path(tmp_file_path).unlink(missing_ok=True)

def check_dependencies():
    """Check if all required dependencies are available."""
    print("🔧 Checking dependencies...")
    
    dependencies = [
        ('easyocr', 'EasyOCR'),
        ('cv2', 'OpenCV'),
        ('PIL', 'Pillow'),
        ('PyPDF2', 'PyPDF2'),
        ('chromadb', 'ChromaDB'),
        ('sentence_transformers', 'Sentence Transformers'),
    ]
    
    missing = []
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - Missing!")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        return False
    
    print("✅ All dependencies available!")
    return True

def check_api_keys():
    """Check API key configuration."""
    print("🔑 Checking API keys...")
    
    config = Config()
    
    openai_key = config.openai_api_key
    gemini_key = config.gemini_api_key
    
    if openai_key and openai_key != "your-openai-api-key":
        print("  ✅ OpenAI API key configured")
    else:
        print("  ⚠️  OpenAI API key not configured")
    
    if gemini_key and gemini_key != "your-gemini-api-key":
        print("  ✅ Gemini API key configured")
    else:
        print("  ⚠️  Gemini API key not configured")
    
    if not openai_key and not gemini_key:
        print("  ❌ No API keys configured!")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Visual Document Analysis RAG - Debug Test")
    print("=" * 50)
    
    # Run checks
    deps_ok = check_dependencies()
    api_ok = check_api_keys()
    
    if deps_ok:
        test_ok = test_extraction()
        
        if test_ok:
            print("\n✅ All tests passed! The system should work correctly.")
        else:
            print("\n❌ Extraction test failed. Check the logs above for details.")
    else:
        print("\n❌ Missing dependencies. Please install them first:")
        print("pip install -r requirements.txt")
    
    print("\n" + "=" * 50)
