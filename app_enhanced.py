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
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main .block-container {
        font-family: 'Inter', sans-serif;
        max-width: 1200px;
        padding-top: 2rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        font-size: 1.3rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* Feature cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0f0f0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-card h4 {
        margin: 0.5rem 0;
        color: #2c3e50;
        font-weight: 600;
    }
    
    .feature-card p {
        color: #666;
        margin: 0;
        font-size: 0.9rem;
    }
    
    /* Upload area */
    .upload-section {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0f0f0;
        margin-bottom: 2rem;
    }
    
    .upload-zone {
        border: 2px dashed #3498db;
        border-radius: 10px;
        padding: 3rem 2rem;
        text-align: center;
        background: linear-gradient(45deg, #f8f9fa, #e9ecef);
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .upload-zone:hover {
        border-color: #2980b9;
        background: linear-gradient(45deg, #e9ecef, #f8f9fa);
        transform: scale(1.02);
    }
    
    .upload-icon {
        font-size: 4rem;
        color: #3498db;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* File list */
    .file-item {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #3498db;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Status indicators */
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-processing {
        background: #fff3cd;
        color: #856404;
    }
    
    .status-success {
        background: #d4edda;
        color: #155724;
    }
    
    .status-error {
        background: #f8d7da;
        color: #721c24;
    }
    
    /* Chat interface */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0f0f0;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .chat-message {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 10px;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .bot-message {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        margin-right: 2rem;
    }
    
    /* Metrics */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0f0f0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        .main-header p {
            font-size: 1rem;
        }
        .feature-grid {
            grid-template-columns: 1fr;
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
    """Render the main header."""
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Visual Document Analysis RAG</h1>
        <p>Transform your documents into intelligent, searchable knowledge bases with AI</p>
    </div>
    """, unsafe_allow_html=True)

def render_features():
    """Render feature highlights."""
    st.markdown("### ✨ Powerful Features")
    
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <h4>Multi-Format Support</h4>
            <p>Process PDFs, images, scanned documents, and text files with ease</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h4>Advanced OCR</h4>
            <p>Extract text from images and scanned documents using state-of-the-art OCR</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h4>Table & Chart Analysis</h4>
            <p>Automatically detect and extract data from tables and visual charts</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h4>AI-Powered Q&A</h4>
            <p>Ask natural language questions and get intelligent answers with source citations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar(config):
    """Render enhanced sidebar."""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # AI Provider selection
        st.markdown("### 🤖 AI Provider")
        llm_provider = st.selectbox(
            "Choose AI Model",
            ["gemini", "openai"],
            index=0 if config.llm_provider == "gemini" else 1,
            help="Select your preferred AI model provider"
        )
        config.llm_provider = llm_provider
        
        # API Key configuration
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
        
        # Processing options
        st.markdown("### 🛠️ Processing Options")
        
        use_ocr = st.checkbox(
            "🔍 Enable OCR", 
            value=True,
            help="Extract text from images and scanned documents"
        )
        
        extract_tables = st.checkbox(
            "📊 Extract Tables", 
            value=True,
            help="Detect and extract table data"
        )
        
        extract_charts = st.checkbox(
            "📈 Extract Charts", 
            value=True,
            help="Identify charts and visual elements"
        )
        
        st.markdown("---")
        
        # Additional options
        st.markdown("### 🎛️ Advanced Settings")
        
        similarity_threshold = st.slider(
            "Similarity Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.1,
            help="Lower values return more results"
        )
        
        max_results = st.slider(
            "Max Results",
            min_value=1,
            max_value=10,
            value=5,
            help="Maximum number of sources to return"
        )
        
        return llm_provider, use_ocr, extract_tables, extract_charts, similarity_threshold, max_results

def render_upload_section(uploaded_files, use_ocr, extract_tables, extract_charts):
    """Render the file upload section."""
    st.markdown("## 📁 Document Upload")
    
    st.markdown("""
    <div class="upload-section">
        <div class="upload-zone">
            <div class="upload-icon">📁</div>
            <h3>Drag and drop your files here</h3>
            <p>Supported formats: PDF, PNG, JPG, JPEG, TIFF, BMP, TXT, MD</p>
            <p style="font-size: 0.9rem; color: #666;">Maximum file size: 50MB per file</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if uploaded_files:
        st.markdown("### 📋 Selected Files")
        for file in uploaded_files:
            file_size = len(file.getvalue()) / (1024 * 1024)
            st.markdown(f"""
            <div class="file-item">
                <div>
                    <strong>📄 {file.name}</strong><br>
                    <small style="color: #666;">Size: {file_size:.2f} MB</small>
                </div>
                <div style="color: #28a745; font-size: 1.2rem;">✓</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Processing options display
        st.markdown("### 🔧 Processing Configuration")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status = "✅ Enabled" if use_ocr else "❌ Disabled"
            st.markdown(f"**🔍 OCR:** {status}")
        
        with col2:
            status = "✅ Enabled" if extract_tables else "❌ Disabled"
            st.markdown(f"**📊 Tables:** {status}")
        
        with col3:
            status = "✅ Enabled" if extract_charts else "❌ Disabled"
            st.markdown(f"**📈 Charts:** {status}")

def process_documents(uploaded_files, doc_processor, rag_system, use_ocr, extract_tables, extract_charts):
    """Process uploaded documents with enhanced UI feedback."""
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### 🔄 Processing Documents")
        
        # Initialize progress tracking
        progress_bar = st.progress(0, text="Initializing...")
        status_placeholder = st.empty()
        
        processed_files = []
        
        for i, uploaded_file in enumerate(uploaded_files):
            # Update progress
            progress = i / len(uploaded_files)
            progress_bar.progress(progress, text=f"Processing {uploaded_file.name}...")
            
            # Show current file status
            with status_placeholder.container():
                st.markdown(f"""
                <div style="background: #e3f2fd; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <div style="display: flex; align-items: center;">
                        <div style="margin-right: 1rem; font-size: 1.5rem;">⏳</div>
                        <div>
                            <strong>Processing: {uploaded_file.name}</strong><br>
                            <small>Extracting content and building embeddings...</small>
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
                
                processed_files.append({
                    'name': uploaded_file.name,
                    'elements': len(doc_data['elements']),
                    'status': 'success'
                })
                
                # Show success
                with status_placeholder.container():
                    st.markdown(f"""
                    <div style="background: #d4edda; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                        <div style="display: flex; align-items: center;">
                            <div style="margin-right: 1rem; font-size: 1.5rem;">✅</div>
                            <div>
                                <strong>Completed: {uploaded_file.name}</strong><br>
                                <small>Extracted {len(doc_data['elements'])} elements</small>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                time.sleep(0.8)  # Brief pause for user to see status
                
            except Exception as e:
                processed_files.append({
                    'name': uploaded_file.name,
                    'error': str(e),
                    'status': 'error'
                })
                
                with status_placeholder.container():
                    st.markdown(f"""
                    <div style="background: #f8d7da; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                        <div style="display: flex; align-items: center;">
                            <div style="margin-right: 1rem; font-size: 1.5rem;">❌</div>
                            <div>
                                <strong>Error: {uploaded_file.name}</strong><br>
                                <small>{str(e)}</small>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            finally:
                # Clean up
                os.unlink(tmp_file_path)
        
        # Complete progress
        progress_bar.progress(1.0, text="✅ Processing complete!")
        
        # Summary
        success_count = len([f for f in processed_files if f['status'] == 'success'])
        error_count = len([f for f in processed_files if f['status'] == 'error'])
        
        if success_count > 0:
            st.success(f"🎉 Successfully processed {success_count} documents!")
        if error_count > 0:
            st.error(f"❌ Failed to process {error_count} documents")
        
        # Clear status after showing summary
        time.sleep(2)
        status_placeholder.empty()
        
        return processed_files

def render_chat_interface(rag_system):
    """Render the Q&A chat interface."""
    st.markdown("## 💬 Ask Questions")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Question input
    with st.container():
        question = st.text_area(
            "Ask a question about your documents:",
            placeholder="e.g., What are the key findings? What data is shown in the tables?",
            height=100
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            ask_button = st.button("🚀 Ask Question", type="primary", use_container_width=True)
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
    
    # Process question
    if ask_button and question:
        if not rag_system.has_documents():
            st.warning("⚠️ Please upload and process documents first.")
            return
        
        with st.spinner("🔍 Searching documents and generating answer..."):
            try:
                # Add user question to chat
                st.session_state.chat_history.append({
                    "type": "user",
                    "content": question,
                    "timestamp": time.time()
                })
                
                # Get answer
                result = rag_system.query(question)
                
                # Add bot response to chat
                st.session_state.chat_history.append({
                    "type": "bot",
                    "content": result['answer'],
                    "sources": result.get('sources', []),
                    "timestamp": time.time()
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💭 Conversation History")
        
        chat_container = st.container()
        with chat_container:
            for i, message in enumerate(reversed(st.session_state.chat_history[-10:])):  # Show last 10 messages
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
                    
                    # Show sources
                    if message.get('sources'):
                        with st.expander(f"📚 Sources ({len(message['sources'])} found)"):
                            for j, source in enumerate(message['sources']):
                                st.markdown(f"""
                                **Source {j+1}:** {source.get('filename', 'Unknown')}
                                - Page: {source.get('page', 'N/A')}
                                - Type: {source.get('element_type', 'N/A')}
                                - Content: {source.get('content', '')[:200]}...
                                """)

def render_stats_dashboard(rag_system):
    """Render the statistics dashboard."""
    st.markdown("### 📊 System Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        doc_count = rag_system.get_document_count()
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{doc_count}</div>
            <div class="metric-label">Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        chunk_count = rag_system.get_chunk_count()
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{chunk_count}</div>
            <div class="metric-label">Text Chunks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        chat_count = len(st.session_state.get('chat_history', []))
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{chat_count}</div>
            <div class="metric-label">Questions Asked</div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function."""
    # Render header
    render_header()
    
    # Initialize system
    config, doc_processor, rag_system = initialize_system()
    
    # Render features
    render_features()
    
    # Sidebar configuration
    llm_provider, use_ocr, extract_tables, extract_charts, similarity_threshold, max_results = render_sidebar(config)
    
    # Update config with sidebar values
    config.similarity_threshold = similarity_threshold
    config.top_k_results = max_results
    
    st.markdown("---")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📁 Upload Documents", "💬 Ask Questions", "📊 Dashboard"])
    
    with tab1:
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp', 'txt', 'md'],
            accept_multiple_files=True,
            help="Upload multiple documents to build your knowledge base"
        )
        
        # Render upload section
        render_upload_section(uploaded_files, use_ocr, extract_tables, extract_charts)
        
        # Process button
        if uploaded_files and st.button("🚀 Process Documents", type="primary", use_container_width=True):
            if not (config.openai_api_key or config.gemini_api_key):
                st.error("⚠️ Please configure your API key in the sidebar first!")
                return
            
            process_documents(uploaded_files, doc_processor, rag_system, use_ocr, extract_tables, extract_charts)
    
    with tab2:
        render_chat_interface(rag_system)
    
    with tab3:
        render_stats_dashboard(rag_system)
        
        # Additional system info
        st.markdown("### ⚙️ System Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **AI Provider:** {config.llm_provider.title()}  
            **Similarity Threshold:** {config.similarity_threshold}  
            **Max Results:** {config.top_k_results}  
            """)
        
        with col2:
            st.markdown(f"""
            **OCR Enabled:** {'✅' if use_ocr else '❌'}  
            **Table Extraction:** {'✅' if extract_tables else '❌'}  
            **Chart Extraction:** {'✅' if extract_charts else '❌'}  
            """)

if __name__ == "__main__":
    main()
