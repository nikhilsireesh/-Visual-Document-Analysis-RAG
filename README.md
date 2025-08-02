# Visual Document Analysis RAG System

A comprehensive Retrieval-Augmented Generation (RAG) system that processes PDFs, images, and scanned documents to extract and retrieve information from tables, charts, and mixed text-image content.

## 🚀 Features

### Multi-Format Document Processing
- **PDF Documents**: Extract text, tables, and visual elements
- **Images**: Process PNG, JPG, JPEG, TIFF, BMP formats
- **Scanned Documents**: OCR integration for text recognition

### Advanced Content Extraction
- **Text Extraction**: Multiple OCR engines (EasyOCR, Tesseract)
- **Table Recognition**: Extract structured data from tables
- **Chart Detection**: Identify and process charts and graphs
- **Layout Analysis**: Understand document structure and relationships

### Intelligent Retrieval
- **Vector Database**: ChromaDB for efficient similarity search
- **Semantic Search**: Context-aware document retrieval
- **Multi-modal Understanding**: Handle text, tables, and visual content

### User-Friendly Interface
- **Streamlit Web App**: Interactive document upload and querying
- **Real-time Processing**: Live feedback during document processing
- **Source Attribution**: Clear references to original content

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- API key for LLM provider:
  - **Gemini API** (Recommended): Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
  - **OpenAI API**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)

### Clone and Setup
```bash
git clone <repository-url>
cd nervespark-project
pip install -r requirements.txt
```

### Additional Setup for OCR
```bash
# For Tesseract OCR (optional, EasyOCR is preferred)
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Ubuntu: sudo apt-get install tesseract-ocr
```

### System Dependencies (for advanced table extraction)
```bash
# For Camelot table extraction (optional)
pip install "camelot-py[cv]"

# For layoutparser (optional, for advanced layout analysis)
pip install "layoutparser[paddlepaddle]"
```

## 🚀 Quick Start

### 1. Set up Environment
```bash
# For Gemini (Recommended)
echo "GEMINI_API_KEY=your-gemini-api-key" > .env

# Or for OpenAI
echo "OPENAI_API_KEY=your-openai-api-key" > .env
```

### 2. Test the System
```bash
python test_system.py
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Access the Web Interface
Open your browser and go to `http://localhost:8501`

## 📖 Usage

### Document Upload and Processing
1. **Upload Documents**: Drag and drop or select PDF files and images
2. **Configure Processing**: Choose OCR, table extraction, and chart detection options
3. **Process**: Click "Process Documents" to extract content
4. **Query**: Ask questions about the uploaded documents

### Example Queries
- "What are the key financial metrics shown in the quarterly report?"
- "Summarize the data from the sales table"
- "What trends are visible in the revenue chart?"
- "Extract all contact information from the scanned business cards"

## 🏗️ Architecture

### Core Components

#### Document Processor (`src/document_processor.py`)
- Multi-format document parsing
- OCR text extraction using EasyOCR/Tesseract
- Table detection and extraction using computer vision
- Chart and graph identification
- Layout analysis using LayoutParser

#### RAG System (`src/rag_system.py`)
- Vector embeddings using Sentence Transformers
- ChromaDB for persistent vector storage
- Intelligent chunking strategies
- Context-aware answer generation using OpenAI GPT

#### Configuration (`src/config.py`)
- Centralized configuration management
- Model and processing parameters
- API key management

### Processing Pipeline
1. **Document Input**: PDF/Image upload
2. **Content Extraction**: Text, tables, charts, layout analysis
3. **Chunking**: Intelligent text segmentation
4. **Vectorization**: Generate embeddings
5. **Storage**: Persist in ChromaDB
6. **Retrieval**: Semantic search for relevant content
7. **Generation**: Context-aware answer synthesis

## 🔧 Configuration

### Model Settings
```python
# Embedding model
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"

# LLM model
llm_model = "gpt-3.5-turbo"

# Chunking parameters
chunk_size = 1000
chunk_overlap = 200
```

### Processing Options
- **OCR Engine**: EasyOCR (default) or Tesseract
- **Table Extraction**: Camelot or Tabula
- **Chart Detection**: OpenCV-based computer vision
- **Layout Analysis**: LayoutParser with PubLayNet model

## 📊 Evaluation Metrics

The system tracks several performance metrics:
- **Retrieval Accuracy**: Relevance of retrieved documents
- **Query Latency**: Response time for queries
- **Processing Time**: Document processing duration
- **Extraction Quality**: OCR and table extraction accuracy

## 🔍 Technical Challenges Addressed

### OCR Accuracy
- Multiple OCR engines with fallback options
- Preprocessing for improved text recognition
- Confidence scoring for extracted text

### Table Structure Recognition
- Computer vision-based table detection
- Multiple extraction libraries (Camelot, Tabula)
- Structured data preservation

### Chart Interpretation
- Contour-based chart detection
- Aspect ratio and area filtering
- Visual element classification

### Layout Analysis
- Deep learning-based layout understanding
- Element relationship preservation
- Multi-modal content correlation

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push code to GitHub
2. Connect Streamlit Cloud to repository
3. Add OpenAI API key to secrets
4. Deploy automatically

### HuggingFace Spaces
1. Create new Space with Streamlit
2. Upload project files
3. Configure secrets
4. Deploy

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_system.py
```

Tests include:
- Dependency verification
- Document processing pipeline
- RAG system functionality
- Streamlit app integration

## 📁 Project Structure

```
nervespark-project/
├── app.py                     # Streamlit web application
├── requirements.txt           # Python dependencies
├── test_system.py            # System testing script
├── README.md                 # Project documentation
├── .env.example              # Environment variables template
├── src/                      # Core source code
│   ├── __init__.py
│   ├── config.py             # Configuration management
│   ├── document_processor.py # Document processing pipeline
│   └── rag_system.py         # RAG implementation
├── chroma_db/                # Vector database storage
├── docs/                     # Additional documentation
└── examples/                 # Example documents and usage
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain**: For RAG framework components
- **ChromaDB**: For vector database functionality
- **Streamlit**: For web interface framework
- **EasyOCR**: For optical character recognition
- **LayoutParser**: For document layout analysis
- **OpenAI**: For language model capabilities

## 📞 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Check the documentation in the `docs/` folder
- Run `python test_system.py` for system diagnostics

## 🔮 Future Enhancements

- [ ] Support for more document formats (Word, PowerPoint)
- [ ] Advanced chart data extraction and analysis
- [ ] Multi-language document support
- [ ] Real-time collaboration features
- [ ] Integration with more LLM providers
- [ ] Advanced evaluation metrics and benchmarking
- [ ] Batch processing capabilities
- [ ] API endpoint for programmatic access
