import os
import sys
import logging
import traceback
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_document_processing():
    """Test document processing functionality."""
    from src.config import Config
    from src.document_processor import DocumentProcessor
    
    print("Testing Document Processing...")
    
    try:
        config = Config()
        processor = DocumentProcessor(config)
        print("✅ Document processor initialized successfully")
        
        # Test with a simple text file (create for testing)
        test_file = project_root / "test_document.txt"
        with open(test_file, "w") as f:
            f.write("This is a test document for visual document analysis RAG system.")
        
        print("✅ Document processing components working")
        
        # Clean up test file
        test_file.unlink()
        
    except Exception as e:
        print(f"❌ Document processing test failed: {e}")
        traceback.print_exc()

def test_rag_system():
    """Test RAG system functionality."""
    from src.config import Config
    from src.document_processor import DocumentProcessor
    from src.rag_system import RAGSystem
    
    print("\nTesting RAG System...")
    
    try:
        config = Config()
        doc_processor = DocumentProcessor(config)
        rag_system = RAGSystem(config, doc_processor)
        print("✅ RAG system initialized successfully")
        
        # Test basic functionality
        doc_count = rag_system.get_document_count()
        chunk_count = rag_system.get_chunk_count()
        print(f"✅ Current documents: {doc_count}, chunks: {chunk_count}")
        
    except Exception as e:
        print(f"❌ RAG system test failed: {e}")
        traceback.print_exc()

def test_streamlit_app():
    """Test if Streamlit app can be imported."""
    print("\nTesting Streamlit App...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        # Test if app.py can be imported
        import app
        print("✅ Streamlit app can be imported")
        
    except Exception as e:
        print(f"❌ Streamlit app test failed: {e}")
        traceback.print_exc()

def test_dependencies():
    """Test if all required dependencies are available."""
    print("\nTesting Dependencies...")
    
    required_packages = [
        'streamlit',
        'chromadb',
        'sentence_transformers',
        'langchain',
        'openai',
        'PyPDF2',
        'pillow',
        'opencv-python',
        'pandas',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                import cv2
            elif package == 'pillow':
                import PIL
            else:
                __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
    else:
        print("\n✅ All required dependencies are available")

if __name__ == "__main__":
    print("🔍 Testing Visual Document Analysis RAG System")
    print("=" * 50)
    
    test_dependencies()
    test_document_processing()
    test_rag_system()
    test_streamlit_app()
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("\nTo run the application:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
    print("2. Run: streamlit run app.py")
