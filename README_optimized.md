# 🔍 Visual Document Analysis RAG System

A beautiful, high-performance RAG (Retrieval-Augmented Generation) system for processing and analyzing visual documents including PDFs, images, and scanned documents.

![System Overview](https://img.shields.io/badge/Status-Optimized-brightgreen)
![Performance](https://img.shields.io/badge/Performance-High-blue)
![UI](https://img.shields.io/badge/UI-Beautiful-purple)

## ✨ Features

### 🚀 **High Performance**
- **Optimized Processing**: Multi-threaded document processing with intelligent caching
- **Efficient Memory Usage**: Smart memory management and garbage collection
- **GPU Acceleration**: Optional GPU support for OCR and embeddings
- **Batch Processing**: Efficient batch operations for large document sets

### 🎨 **Beautiful Interface**
- **Modern Design**: Clean, elegant interface with smooth animations
- **Responsive Layout**: Works perfectly on desktop and mobile devices
- **Real-time Feedback**: Live progress indicators and status updates
- **Dark/Light Themes**: Adaptive theming for comfortable viewing

### 📄 **Document Processing**
- **Multi-Format Support**: PDFs, images (PNG, JPG, TIFF), text files
- **Advanced OCR**: EasyOCR and Tesseract integration with high accuracy
- **Table Extraction**: Automatic detection and extraction of tables
- **Chart Recognition**: Smart chart and graph detection
- **Layout Analysis**: Intelligent document structure understanding

### 🤖 **AI-Powered Analysis**
- **Vector Search**: Advanced similarity search with ChromaDB
- **Smart Chunking**: Intelligent text segmentation for optimal retrieval
- **Multi-LLM Support**: OpenAI GPT-4 and Google Gemini integration
- **Context-Aware Answers**: Precise responses with source attribution

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd nervespark-project

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your API keys:

```env
# Choose your preferred AI provider
GEMINI_API_KEY=your_gemini_api_key_here
# OR
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application

**Option 1: Optimized Version (Recommended)**
```bash
streamlit run app_optimized.py
```

**Option 2: Standard Version**
```bash
streamlit run app.py
```

### 4. Access the Interface

Open your browser and navigate to: `http://localhost:8501`

## 🎯 How to Use

### 📤 **Upload Documents**
1. Go to the **"Upload"** tab
2. Configure your AI provider and API key in the sidebar
3. Select processing options (OCR, Tables, Charts)
4. Drag and drop your documents or click to browse
5. Click **"Process Documents"** to analyze

### 💬 **Ask Questions**
1. Switch to the **"Chat"** tab
2. Type your question about the uploaded documents
3. Click **"Ask Question"** to get AI-powered answers
4. View sources and citations for each response

### 📊 **Monitor Performance**
1. Check the **"Dashboard"** tab for system metrics
2. View processing statistics and performance data
3. Monitor memory usage and optimization suggestions

## ⚙️ Configuration Options

### **Processing Settings**
- **OCR Engine**: Choose between EasyOCR (GPU-accelerated) or Tesseract
- **Table Extraction**: Enable automatic table detection and extraction
- **Chart Detection**: Enable chart and graph recognition
- **Similarity Threshold**: Adjust search sensitivity (0.1 - 1.0)

### **Performance Optimization**
- **Batch Size**: Configure batch processing size (50-200)
- **Concurrent Files**: Set parallel processing limit (1-5)
- **Caching**: Enable/disable result caching for faster responses
- **Memory Optimization**: Automatic memory management and cleanup

### **Advanced Settings**
- **Chunk Size**: Text segmentation size (500-1500 characters)
- **Chunk Overlap**: Overlap between text chunks (100-300 characters)
- **GPU Acceleration**: Enable GPU for OCR and embeddings (if available)

## 🔧 System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Document      │    │   RAG System     │    │   AI Models     │
│   Processor     │───▶│   (ChromaDB)     │───▶│   (GPT/Gemini)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   OCR Engine    │    │   Vector Store   │    │   Web Interface │
│   (EasyOCR)     │    │   (Embeddings)   │    │   (Streamlit)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📈 Performance Metrics

The system provides comprehensive performance monitoring:

- **Processing Speed**: Documents/minute
- **Memory Usage**: Real-time memory consumption
- **Cache Efficiency**: Hit rate for cached operations
- **Query Response Time**: Average response latency
- **System Load**: CPU and memory utilization

## 🛠️ Optimization Features

### **Automatic Optimizations**
- Intelligent hardware detection and optimization
- Adaptive batch sizing based on available memory
- Smart caching with TTL (Time-To-Live) management
- Memory cleanup and garbage collection

### **Manual Optimizations**
- Configurable processing parameters
- GPU acceleration toggle
- Cache size limits
- Concurrent processing limits

## 📝 Supported File Types

| Format | Extensions | Processing Method |
|--------|------------|-------------------|
| PDF | `.pdf` | PyPDF2 + OCR fallback |
| Images | `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp` | Direct OCR processing |
| Text | `.txt`, `.md` | Direct text extraction |

## 🔍 Troubleshooting

### **Common Issues**

**1. API Key Not Working**
- Verify your API key is correct
- Check environment variables
- Ensure sufficient API credits

**2. Slow Processing**
- Enable GPU acceleration if available
- Reduce image resolution
- Lower concurrent file processing
- Enable caching for repeated operations

**3. Memory Issues**
- Reduce batch size
- Enable memory optimization
- Process fewer files simultaneously
- Clear cache periodically

**4. OCR Accuracy**
- Use higher DPI for image conversion
- Ensure good image quality
- Try different OCR engines
- Adjust confidence thresholds

### **Performance Tips**

1. **Hardware Optimization**
   - Use GPU-enabled hardware for faster OCR
   - Ensure sufficient RAM (8GB+ recommended)
   - SSD storage for faster file access

2. **Configuration Tuning**
   - Adjust similarity threshold based on needs
   - Optimize chunk size for your document types
   - Enable caching for repeated queries

3. **File Preparation**
   - Use high-quality scanned documents
   - Optimize file sizes before upload
   - Consider text-based PDFs over scanned images

## 🚀 Advanced Usage

### **Batch Processing**
```python
# Process multiple documents efficiently
from src.document_processor_optimized import OptimizedDocumentProcessor
from src.config_optimized import Config

config = Config()
config.optimize_for_hardware()
processor = OptimizedDocumentProcessor(config)

# Process multiple files
for file_path in file_paths:
    result = processor.process_document(file_path)
```

### **Custom Configuration**
```python
# Create custom configuration
config = Config()
config.chunk_size = 1000
config.ocr_workers = 4
config.enable_caching = True
config.easyocr_gpu = True
```

## 📊 Benchmarks

Performance on a typical system (8GB RAM, 4-core CPU):

| Operation | Time | Throughput |
|-----------|------|------------|
| PDF Processing (10 pages) | 15-30s | 2-4 pages/min |
| Image OCR (1MB image) | 3-8s | 8-20 images/min |
| Vector Search | 100-500ms | 2-10 queries/sec |
| Text Extraction | 1-3s | 20-60 pages/min |

*Results may vary based on document complexity and hardware specifications.*

## 🤝 Contributing

We welcome contributions! Please see our contribution guidelines for:
- Code style and formatting
- Testing requirements
- Documentation standards
- Performance considerations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Acknowledgments

- **Streamlit** for the beautiful web framework
- **ChromaDB** for efficient vector storage
- **EasyOCR** for accurate text recognition
- **Google Gemini** and **OpenAI** for powerful AI capabilities

---

<div align="center">
<strong>🔍 Ready to analyze your documents? Start now!</strong><br>
<code>streamlit run app_optimized.py</code>
</div>
