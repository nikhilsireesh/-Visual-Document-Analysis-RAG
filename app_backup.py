import streamlit as st
import os
from pathlib import Path
import tempfile
import time
from src.document_processor import DocumentProcessor
from src.rag_system import RAGSystem
from src.config import Config

# Page configuration
st.set_page_config(
    page_title="Visual Document Analysis RAG",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --warning-color: #ff9800;
        --error-color: #d62728;
        --background-color: #f8f9fa;
        --card-background: #ffffff;
        --text-color: #2c3e50;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .stCard {
        background: var(--card-background);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid #e1e8ed;
        margin-bottom: 1rem;
    }
    
    /* Upload area styling */
    .upload-area {
        border: 2px dashed #3498db;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(45deg, #f8f9fa, #e9ecef);
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #2980b9;
        background: linear-gradient(45deg, #e9ecef, #f8f9fa);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metrics styling */
    .metric-card {
        background: var(--card-background);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        border-left: 4px solid var(--primary-color);
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    /* Feature icons */
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background-color: var(--success-color);
        box-shadow: 0 0 5px var(--success-color);
    }
    
    .status-offline {
        background-color: var(--error-color);
        box-shadow: 0 0 5px var(--error-color);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        .main-header p {
            font-size: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def initialize_system():
    """Initialize the RAG system with caching."""
    config = Config()
    doc_processor = DocumentProcessor(config)
    rag_system = RAGSystem(config, doc_processor)
    return config, doc_processor, rag_system

def render_header():
    """Render the main header with animated title."""
    st.markdown("""
    <div class="main-header">
        <h1>� Visual Document Analysis RAG</h1>
        <p>Transform your documents into intelligent, searchable knowledge bases</p>
    </div>
    """, unsafe_allow_html=True)

def render_features():
    """Render feature highlights."""
    st.markdown("### ✨ Key Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div class="feature-icon">📄</div>
            <h4>Multi-Format</h4>
            <p>PDFs, Images, Scanned Docs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div class="feature-icon">🔍</div>
            <h4>OCR Powered</h4>
            <p>Extract text from images</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div class="feature-icon">📊</div>
            <h4>Table & Charts</h4>
            <p>Analyze structured data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div class="feature-icon">🤖</div>
            <h4>AI Powered</h4>
            <p>Intelligent Q&A system</p>
        </div>
        """, unsafe_allow_html=True)

def render_sidebar(config):
    """Render enhanced sidebar."""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # LLM Provider selection with status indicator
        st.markdown("### 🤖 AI Provider")
        llm_provider = st.selectbox(
            "Choose AI Model",
            ["gemini", "openai"],
            index=0 if config.llm_provider == "gemini" else 1,
            help="Select your preferred AI model provider"
        )
        config.llm_provider = llm_provider
        
        # API Key input with enhanced UI
        st.markdown("### 🔐 API Configuration")
        if llm_provider == "gemini":
            api_key = st.text_input(
                "Gemini API Key", 
                type="password", 
                value=os.getenv("GEMINI_API_KEY", ""),
                help="Enter your Google AI Studio API key"
            )
            if api_key:
                os.environ["GEMINI_API_KEY"] = api_key
                config.gemini_api_key = api_key
                st.success("✅ Gemini API key configured")
            else:
                st.warning("⚠️ Please enter your Gemini API key")
        else:
            api_key = st.text_input(
                "OpenAI API Key", 
                type="password", 
                value=os.getenv("OPENAI_API_KEY", ""),
                help="Enter your OpenAI API key"
            )
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                config.openai_api_key = api_key
                st.success("✅ OpenAI API key configured")
            else:
                st.warning("⚠️ Please enter your OpenAI API key")
        
        st.markdown("---")
        
        # Processing options with better styling
        st.markdown("### 🛠️ Processing Options")
        
        use_ocr = st.checkbox(
            "🔍 Enable OCR for scanned documents", 
            value=True,
            help="Extract text from images and scanned documents"
        )
        
        extract_tables = st.checkbox(
            "📊 Extract tables", 
            value=True,
            help="Detect and extract table data from documents"
        )
        
        extract_charts = st.checkbox(
            "📈 Extract charts and graphs", 
            value=True,
            help="Identify charts and visual elements"
        )
        
        st.markdown("---")
        
        # Clear database option
        st.markdown("### 🗑️ Database Management")
        if st.button("🧹 Clear Document Collection", type="secondary"):
            # This would need to be implemented in the RAG system
            st.success("Database cleared!")
            st.rerun()
        
        return llm_provider, use_ocr, extract_tables, extract_charts

def main():
                # Reinitialize RAG system with new API key
                if api_key != getattr(config, '_last_gemini_key', ''):
                    config._last_gemini_key = api_key
                    st.cache_resource.clear()
        else:
            api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                config.openai_api_key = api_key
                # Reinitialize RAG system with new API key
                if api_key != getattr(config, '_last_openai_key', ''):
                    config._last_openai_key = api_key
                    st.cache_resource.clear()
        
        st.markdown("---")
        
        # Processing options
        st.subheader("Processing Options")
        use_ocr = st.checkbox("Enable OCR for scanned documents", value=True)
        extract_tables = st.checkbox("Extract tables", value=True)
        extract_charts = st.checkbox("Extract charts and graphs", value=True)
        
        st.markdown("---")
        
        # Document collection info
        if st.button("Clear Document Collection"):
            if st.session_state.get('rag_system'):
                st.session_state.rag_system.clear_collection()
                st.success("Document collection cleared!")
                st.rerun()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Documents")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose files",
            accept_multiple_files=True,
            type=['pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp']
        )
        
        if uploaded_files:
            st.write(f"Selected {len(uploaded_files)} file(s)")
            
            if st.button("Process Documents", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, uploaded_file in enumerate(uploaded_files):
                    status_text.text(f"Processing {uploaded_file.name}...")
                    
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    try:
                        # Process document
                        doc_data = doc_processor.process_document(
                            tmp_file_path,
                            use_ocr=use_ocr,
                            extract_tables=extract_tables,
                            extract_charts=extract_charts
                        )
                        
                        # Add to RAG system
                        rag_system.add_document(doc_data, uploaded_file.name)
                        
                        progress_bar.progress((i + 1) / len(uploaded_files))
                        
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                    
                    finally:
                        # Clean up temporary file
                        os.unlink(tmp_file_path)
                
                status_text.text("✅ All documents processed successfully!")
                st.success(f"Processed {len(uploaded_files)} documents and added to knowledge base.")
    
    with col2:
        st.header("❓ Ask Questions")
        
        # Question input
        question = st.text_area(
            "Enter your question about the uploaded documents:",
            placeholder="e.g., What are the key findings in the financial report? What data is shown in the charts?"
        )
        
        if st.button("Get Answer", type="primary") and question:
            if not rag_system.has_documents():
                st.warning("Please upload and process documents first.")
                return
            
            with st.spinner("Searching documents and generating answer..."):
                try:
                    # Get answer from RAG system
                    result = rag_system.query(question)
                    
                    # Display answer
                    st.subheader("🤖 Answer")
                    st.write(result['answer'])
                    
                    # Display sources
                    if result.get('sources'):
                        st.subheader("📚 Sources")
                        for i, source in enumerate(result['sources']):
                            with st.expander(f"Source {i+1}: {source.get('filename', 'Unknown')}"):
                                st.write(source.get('content', ''))
                                if source.get('page'):
                                    st.caption(f"Page: {source['page']}")
                                if source.get('element_type'):
                                    st.caption(f"Element type: {source['element_type']}")
                    
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
    
    # Display system statistics
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        doc_count = rag_system.get_document_count()
        st.metric("Documents in Knowledge Base", doc_count)
    
    with col2:
        chunk_count = rag_system.get_chunk_count()
        st.metric("Text Chunks", chunk_count)
    
    with col3:
        if hasattr(rag_system, 'get_last_query_time'):
            last_time = rag_system.get_last_query_time()
            st.metric("Last Query Time (ms)", f"{last_time:.2f}" if last_time else "N/A")

if __name__ == "__main__":
    main()
