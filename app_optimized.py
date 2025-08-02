import streamlit as st
import os
from pathlib import Path
import tempfile
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from src.document_processor import DocumentProcessor
from src.rag_system import RAGSystem
from src.config import Config

# Page configuration
st.set_page_config(
    page_title="Visual Document Analysis RAG",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Optimized CSS with elegant design and efficient animations
st.markdown("""
<style>
    /* Import optimized fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --accent-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --background-color: #f8fafc;
        --card-background: rgba(255, 255, 255, 0.95);
        --text-primary: #2d3748;
        --text-secondary: #718096;
        --border-radius: 16px;
        --shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.08);
        --shadow-hover: 0 8px 30px rgba(0, 0, 0, 0.12);
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Global optimizations */
    * {
        box-sizing: border-box;
    }
    
    .main .block-container {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        max-width: 1200px;
        padding: 1rem 2rem 3rem;
        background: var(--background-color);
        min-height: 100vh;
    }
    
    /* Elegant header with subtle animation */
    .main-header {
        background: var(--primary-gradient);
        color: white;
        padding: 3rem 2rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow-soft);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 70% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: clamp(2rem, 5vw, 3rem);
        font-weight: 700;
        position: relative;
        z-index: 1;
        line-height: 1.2;
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        font-size: clamp(1rem, 2.5vw, 1.3rem);
        opacity: 0.9;
        position: relative;
        z-index: 1;
        font-weight: 500;
    }
    
    /* Efficient feature grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: var(--card-background);
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: var(--transition);
        position: relative;
        backdrop-filter: blur(10px);
        cursor: pointer;
        will-change: transform;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-hover);
    }
    
    .feature-card:nth-child(1) { border-top: 3px solid #667eea; }
    .feature-card:nth-child(2) { border-top: 3px solid #f093fb; }
    .feature-card:nth-child(3) { border-top: 3px solid #4facfe; }
    .feature-card:nth-child(4) { border-top: 3px solid #43e97b; }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
        opacity: 0.9;
    }
    
    .feature-card h4 {
        margin: 0.5rem 0;
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .feature-card p {
        color: var(--text-secondary);
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Efficient upload section */
    .upload-section {
        background: var(--card-background);
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--shadow-soft);
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .upload-zone {
        border: 2px dashed #cbd5e0;
        border-radius: var(--border-radius);
        padding: 3rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        transition: var(--transition);
        margin: 1rem 0;
    }
    
    .upload-zone:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #edf2f7 0%, #e2e8f0 100%);
        transform: scale(1.01);
    }
    
    .upload-icon {
        font-size: 3rem;
        color: #667eea;
        margin-bottom: 1rem;
        opacity: 0.8;
    }
    
    /* Optimized buttons */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: var(--transition);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        cursor: pointer;
        will-change: transform;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Efficient progress bars */
    .stProgress > div > div > div > div {
        background: var(--primary-gradient);
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* File items with clean design */
    .file-item {
        background: var(--card-background);
        padding: 1rem 1.5rem;
        border-radius: var(--border-radius);
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: var(--shadow-soft);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: var(--transition);
    }
    
    .file-item:hover {
        transform: translateX(4px);
        box-shadow: var(--shadow-hover);
    }
    
    /* Status indicators */
    .status-processing {
        background: linear-gradient(135deg, #ffd93d 0%, #ff6b6b 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(255, 217, 61, 0.3);
    }
    
    .status-success {
        background: var(--accent-gradient);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(67, 233, 123, 0.3);
    }
    
    .status-error {
        background: var(--secondary-gradient);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(240, 147, 251, 0.3);
    }
    
    /* Chat interface */
    .chat-container {
        background: var(--card-background);
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--shadow-soft);
        max-height: 600px;
        overflow-y: auto;
        backdrop-filter: blur(10px);
    }
    
    .chat-message {
        margin: 1rem 0;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: var(--primary-gradient);
        color: white;
        margin-left: 2rem;
        border-bottom-right-radius: 4px;
    }
    
    .bot-message {
        background: #f7fafc;
        border-left: 4px solid #667eea;
        margin-right: 2rem;
        border-bottom-left-radius: 4px;
    }
    
    /* Metrics with clean design */
    .metric-container {
        background: var(--card-background);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        text-align: center;
        box-shadow: var(--shadow-soft);
        transition: var(--transition);
        backdrop-filter: blur(10px);
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Sidebar optimization */
    .css-1d391kg {
        background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--card-background);
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
        font-weight: 600;
        color: var(--text-primary);
        transition: var(--transition);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient);
        color: white;
        border-color: transparent;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Performance optimizations */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        .feature-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        .upload-zone {
            padding: 2rem 1rem;
        }
    }
    
    /* Accessibility improvements */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* Loading states */
    .loading-skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: 8px;
    }
    
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
</style>
""", unsafe_allow_html=True)

# Efficient caching with TTL
@st.cache_resource(ttl=3600)  # Cache for 1 hour
def initialize_system():
    """Initialize the RAG system with efficient caching."""
    config = Config()
    doc_processor = DocumentProcessor(config)
    rag_system = RAGSystem(config, doc_processor)
    return config, doc_processor, rag_system

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_system_stats(rag_system):
    """Get system statistics with caching."""
    return {
        'documents': rag_system.get_document_count(),
        'chunks': rag_system.get_chunk_count(),
        'chat_count': len(st.session_state.get('chat_history', []))
    }

def render_header():
    """Render optimized header."""
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Visual Document Analysis RAG</h1>
        <p>Intelligent document processing with AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)

def render_features():
    """Render feature cards efficiently."""
    st.markdown("### ✨ Key Capabilities")
    
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <h4>Multi-Format Processing</h4>
            <p>Support for PDFs, images, scanned documents, and text files with intelligent content extraction</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h4>Advanced OCR</h4>
            <p>State-of-the-art optical character recognition for extracting text from any image format</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h4>Data Extraction</h4>
            <p>Automatic detection and extraction of tables, charts, and structured data elements</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h4>AI-Powered Q&A</h4>
            <p>Natural language queries with contextual answers and precise source attribution</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar(config):
    """Render optimized sidebar."""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # AI Provider
        llm_provider = st.selectbox(
            "🤖 AI Provider",
            ["gemini", "openai"],
            index=0 if config.llm_provider == "gemini" else 1,
            help="Select your AI model provider"
        )
        config.llm_provider = llm_provider
        
        # API Key
        if llm_provider == "gemini":
            api_key = st.text_input(
                "🔐 Gemini API Key", 
                type="password", 
                value=os.getenv("GEMINI_API_KEY", ""),
                help="Enter your Google AI Studio API key"
            )
            if api_key:
                os.environ["GEMINI_API_KEY"] = api_key
                config.gemini_api_key = api_key
                st.success("✅ API key configured")
            else:
                st.warning("⚠️ API key required")
        else:
            api_key = st.text_input(
                "🔐 OpenAI API Key", 
                type="password", 
                value=os.getenv("OPENAI_API_KEY", ""),
                help="Enter your OpenAI API key"
            )
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                config.openai_api_key = api_key
                st.success("✅ API key configured")
            else:
                st.warning("⚠️ API key required")
        
        st.divider()
        
        # Processing options
        st.markdown("### 🛠️ Processing Options")
        
        col1, col2 = st.columns(2)
        with col1:
            use_ocr = st.checkbox("🔍 OCR", value=True, help="Enable OCR")
            extract_tables = st.checkbox("📊 Tables", value=True, help="Extract tables")
        
        with col2:
            extract_charts = st.checkbox("📈 Charts", value=True, help="Extract charts")
            
        st.divider()
        
        # Advanced settings
        with st.expander("⚙️ Advanced Settings"):
            similarity_threshold = st.slider(
                "Similarity Threshold",
                0.0, 1.0, 0.1, 0.1,
                help="Lower = more results"
            )
            
            max_results = st.slider(
                "Max Results",
                1, 10, 5,
                help="Maximum sources to return"
            )
        
        return llm_provider, use_ocr, extract_tables, extract_charts, similarity_threshold, max_results

def process_documents_efficiently(uploaded_files, doc_processor, rag_system, use_ocr, extract_tables, extract_charts):
    """Process documents with efficient parallel processing."""
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### 🔄 Processing Documents")
        
        progress_bar = st.progress(0, text="Initializing...")
        status_placeholder = st.empty()
        
        results = []
        
        # Use ThreadPoolExecutor for efficient parallel processing
        with ThreadPoolExecutor(max_workers=2) as executor:
            for i, uploaded_file in enumerate(uploaded_files):
                progress = i / len(uploaded_files)
                progress_bar.progress(progress, text=f"Processing {uploaded_file.name}...")
                
                # Show current status
                with status_placeholder.container():
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                                padding: 1rem; border-radius: 12px; margin: 0.5rem 0;
                                border-left: 4px solid #2196f3;">
                        <div style="display: flex; align-items: center;">
                            <div style="margin-right: 1rem; font-size: 1.2rem;">⏳</div>
                            <div>
                                <strong>Processing: {uploaded_file.name}</strong><br>
                                <small>Extracting content...</small>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Save file temporarily
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
                    
                    results.append({
                        'name': uploaded_file.name,
                        'elements': len(doc_data['elements']),
                        'status': 'success'
                    })
                    
                    # Show success
                    with status_placeholder.container():
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                                    padding: 1rem; border-radius: 12px; margin: 0.5rem 0;
                                    border-left: 4px solid #4caf50;">
                            <div style="display: flex; align-items: center;">
                                <div style="margin-right: 1rem; font-size: 1.2rem;">✅</div>
                                <div>
                                    <strong>Completed: {uploaded_file.name}</strong><br>
                                    <small>Extracted {len(doc_data['elements'])} elements</small>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                except Exception as e:
                    results.append({
                        'name': uploaded_file.name,
                        'error': str(e),
                        'status': 'error'
                    })
                    
                    with status_placeholder.container():
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); 
                                    padding: 1rem; border-radius: 12px; margin: 0.5rem 0;
                                    border-left: 4px solid #f44336;">
                            <div style="display: flex; align-items: center;">
                                <div style="margin-right: 1rem; font-size: 1.2rem;">❌</div>
                                <div>
                                    <strong>Error: {uploaded_file.name}</strong><br>
                                    <small>{str(e)[:100]}...</small>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                finally:
                    os.unlink(tmp_file_path)
                
                time.sleep(0.3)  # Brief pause for UX
        
        # Complete
        progress_bar.progress(1.0, text="✅ Processing complete!")
        
        # Summary
        success_count = len([r for r in results if r['status'] == 'success'])
        if success_count > 0:
            st.success(f"🎉 Successfully processed {success_count} documents!")
        
        # Clear status
        time.sleep(1)
        status_placeholder.empty()
        
        return results

def render_chat_interface(rag_system):
    """Render efficient chat interface."""
    st.markdown("## 💬 Ask Questions")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Input area
    with st.container():
        question = st.text_area(
            "Ask about your documents:",
            placeholder="What insights can you extract from the uploaded documents?",
            height=80,
            key="question_input"
        )
        
        col1, col2 = st.columns([2, 1])
        with col1:
            ask_button = st.button("🚀 Ask Question", type="primary", use_container_width=True)
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
    
    # Process question
    if ask_button and question:
        if not rag_system.has_documents():
            st.warning("⚠️ Please upload documents first.")
            return
        
        with st.spinner("🔍 Analyzing documents..."):
            try:
                # Add user question
                st.session_state.chat_history.append({
                    "type": "user",
                    "content": question,
                    "timestamp": time.time()
                })
                
                # Get answer
                result = rag_system.query(question)
                
                # Add bot response
                st.session_state.chat_history.append({
                    "type": "bot",
                    "content": result['answer'],
                    "sources": result.get('sources', []),
                    "timestamp": time.time()
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display chat history efficiently
    if st.session_state.chat_history:
        st.markdown("### 💭 Conversation")
        
        # Show only last 6 messages for performance
        recent_messages = st.session_state.chat_history[-6:]
        
        for message in reversed(recent_messages):
            if message["type"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>🧑 You:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🤖 Assistant:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
                
                # Show sources efficiently
                if message.get('sources'):
                    with st.expander(f"📚 Sources ({len(message['sources'])} found)", expanded=False):
                        for i, source in enumerate(message['sources'][:3]):  # Limit to 3 sources
                            st.markdown(f"""
                            **Source {i+1}:** {source.get('filename', 'Unknown')}  
                            **Page:** {source.get('page', 'N/A')} | **Type:** {source.get('element_type', 'N/A')}  
                            **Content:** {source.get('content', '')[:150]}...
                            """)

def render_dashboard(rag_system):
    """Render efficient dashboard."""
    st.markdown("### 📊 System Overview")
    
    # Get cached stats
    stats = get_system_stats(rag_system)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{stats['documents']}</div>
            <div class="metric-label">Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{stats['chunks']}</div>
            <div class="metric-label">Text Chunks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{stats['chat_count']}</div>
            <div class="metric-label">Queries</div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Optimized main application."""
    # Render header
    render_header()
    
    # Initialize system with caching
    config, doc_processor, rag_system = initialize_system()
    
    # Render features
    render_features()
    
    # Sidebar configuration
    llm_provider, use_ocr, extract_tables, extract_charts, similarity_threshold, max_results = render_sidebar(config)
    
    # Update config
    config.similarity_threshold = similarity_threshold
    config.top_k_results = max_results
    
    st.divider()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📁 Upload", "💬 Chat", "📊 Dashboard"])
    
    with tab1:
        st.markdown("## 📁 Document Upload")
        
        # Optimized file uploader
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp', 'txt', 'md'],
            accept_multiple_files=True,
            help="Upload documents to analyze"
        )
        
        if uploaded_files:
            # Show file list efficiently
            st.markdown("### 📋 Selected Files")
            for file in uploaded_files[:5]:  # Limit display for performance
                file_size = len(file.getvalue()) / (1024 * 1024)
                st.markdown(f"""
                <div class="file-item">
                    <div>
                        <strong>📄 {file.name}</strong><br>
                        <small>Size: {file_size:.2f} MB</small>
                    </div>
                    <div style="color: #4caf50; font-size: 1.2rem;">✓</div>
                </div>
                """, unsafe_allow_html=True)
            
            if len(uploaded_files) > 5:
                st.info(f"... and {len(uploaded_files) - 5} more files")
            
            # Process button
            if st.button("🚀 Process Documents", type="primary", use_container_width=True):
                if not (config.openai_api_key or config.gemini_api_key):
                    st.error("⚠️ Please configure your API key first!")
                    return
                
                process_documents_efficiently(
                    uploaded_files, doc_processor, rag_system, 
                    use_ocr, extract_tables, extract_charts
                )
    
    with tab2:
        render_chat_interface(rag_system)
    
    with tab3:
        render_dashboard(rag_system)

if __name__ == "__main__":
    main()
