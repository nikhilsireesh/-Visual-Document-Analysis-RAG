"""
Demo script for Visual Document Analysis RAG System
This script demonstrates the core functionality without requiring file uploads.
"""

import os
import sys
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.config import Config
from src.document_processor import DocumentProcessor
from src.rag_system import RAGSystem

def create_sample_document():
    """Create a sample document with text and table for testing."""
    # Create a simple image with text and table
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        small_font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
        small_font = font
    
    # Add title
    draw.text((50, 50), "Quarterly Sales Report Q3 2024", fill='black', font=font)
    
    # Add some body text
    text_lines = [
        "Executive Summary:",
        "Our Q3 2024 performance exceeded expectations with",
        "significant growth in all major product categories.",
        "",
        "Key Highlights:",
        "• Revenue increased by 25% compared to Q2",
        "• Customer satisfaction score: 4.8/5.0",
        "• Market share expanded to 15.2%",
        "",
        "Financial Data (in thousands USD):"
    ]
    
    y_pos = 100
    for line in text_lines:
        draw.text((50, y_pos), line, fill='black', font=small_font)
        y_pos += 25
    
    # Add a simple table
    table_data = [
        ["Product", "Q2 Sales", "Q3 Sales", "Growth"],
        ["Widget A", "$120", "$150", "25%"],
        ["Widget B", "$200", "$240", "20%"],
        ["Widget C", "$180", "$225", "25%"],
        ["Total", "$500", "$615", "23%"]
    ]
    
    # Draw table
    table_x = 50
    table_y = y_pos + 20
    cell_width = 120
    cell_height = 30
    
    for row_idx, row in enumerate(table_data):
        for col_idx, cell in enumerate(row):
            x = table_x + col_idx * cell_width
            y = table_y + row_idx * cell_height
            
            # Draw cell border
            draw.rectangle([x, y, x + cell_width, y + cell_height], outline='black')
            
            # Draw cell text
            draw.text((x + 5, y + 5), cell, fill='black', font=small_font)
    
    return img

def run_demo():
    """Run the complete demo."""
    print("🚀 Visual Document Analysis RAG System Demo")
    print("=" * 50)
    
    # Check if API keys are available
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not gemini_key and not openai_key:
        print("⚠️  No API keys found. Setting dummy key for demo purposes.")
        os.environ["GEMINI_API_KEY"] = "dummy-key-for-demo"
    
    try:
        # Initialize system
        print("\n📋 Initializing system components...")
        config = Config()
        doc_processor = DocumentProcessor(config)
        rag_system = RAGSystem(config, doc_processor)
        print("✅ System initialized successfully!")
        
        # Create sample document
        print("\n📄 Creating sample document...")
        sample_image = create_sample_document()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            sample_image.save(tmp_file.name)
            tmp_file_path = tmp_file.name
        
        print(f"✅ Sample document created: {tmp_file_path}")
        
        # Process document
        print("\n🔍 Processing document...")
        doc_data = doc_processor.process_document(
            tmp_file_path,
            use_ocr=True,
            extract_tables=True,
            extract_charts=False
        )
        
        print(f"✅ Document processed successfully!")
        print(f"   - Found {len(doc_data['elements'])} elements")
        print(f"   - Element types: {doc_data['metadata']['element_types']}")
        
        # Add to RAG system
        print("\n💾 Adding document to knowledge base...")
        rag_system.add_document(doc_data, "sample_sales_report.png")
        print("✅ Document added to vector database!")
        
        # Test queries
        print("\n❓ Testing queries...")
        test_queries = [
            "What is the total revenue growth?",
            "What are the key highlights of the report?",
            "Which product had the highest sales in Q3?",
            "What was the customer satisfaction score?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔎 Query {i}: {query}")
            
            if (not gemini_key or gemini_key.startswith("dummy")) and (not openai_key or openai_key.startswith("sk-dummy")):
                print("   ⚠️  Skipping query (no valid API key)")
                continue
            
            try:
                result = rag_system.query(query)
                print(f"   💡 Answer: {result['answer'][:200]}...")
                print(f"   📚 Sources: {len(result['sources'])} relevant chunks found")
            except Exception as e:
                print(f"   ❌ Query failed: {e}")
        
        # Display system statistics
        print("\n📊 System Statistics:")
        print(f"   - Documents in knowledge base: {rag_system.get_document_count()}")
        print(f"   - Total text chunks: {rag_system.get_chunk_count()}")
        
        # Cleanup
        os.unlink(tmp_file_path)
        print("\n🧹 Cleanup completed")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n🎉 Demo completed successfully!")
    print("\nNext steps:")
    print("1. Set your API key:")
    print("   - Gemini: GEMINI_API_KEY=your-key")
    print("   - OpenAI: OPENAI_API_KEY=your-key")
    print("2. Run the Streamlit app: streamlit run app.py")
    print("3. Upload your own documents and start querying!")
    
    return True

if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
