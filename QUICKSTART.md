# Quick Start Guide

## 🚀 Getting Started

Your Visual Document Analysis RAG system is now set up and ready to use!

### 1. **Set up OpenAI API Key**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-openai-api-key-here"

# Or create a .env file
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
```

### 2. **Run the Application**
The Streamlit app is already running! Access it at:
**http://localhost:8501**

### 3. **Test the System**
```bash
# Run the demo (works without API key for testing)
python demo.py

# Run system tests
python test_system.py
```

## 📖 How to Use

### Upload Documents
1. Open the web interface at http://localhost:8501
2. Use the file uploader in the left column
3. Select PDFs, images, or scanned documents
4. Configure processing options:
   - ✅ **OCR**: For scanned documents and images
   - ✅ **Tables**: Extract structured data
   - ✅ **Charts**: Detect graphs and visualizations

### Ask Questions
1. After processing, use the right column
2. Type questions about your documents:
   - "What are the key findings?"
   - "Extract data from the table"
   - "Summarize the document"
   - "What trends are shown in the charts?"

## 🔧 Supported File Types

- **PDFs**: Text-based and scanned documents
- **Images**: PNG, JPG, JPEG, TIFF, BMP
- **Content Types**: Text, tables, charts, mixed layouts

## 🎯 Features Highlights

- **Multi-modal Processing**: Handles text, tables, and visual elements
- **OCR Integration**: EasyOCR for accurate text recognition
- **Table Extraction**: Computer vision-based table detection
- **Chart Analysis**: Visual element recognition and description
- **Semantic Search**: Vector-based document retrieval
- **Source Attribution**: Clear references to original content

## 🔍 Example Queries

### For Financial Documents
- "What was the revenue growth this quarter?"
- "List all expenses from the table"
- "What trends are visible in the revenue chart?"

### For Research Papers
- "What are the main conclusions?"
- "Extract data from Figure 1"
- "Summarize the methodology section"

### For Business Documents
- "What are the action items?"
- "Extract contact information"
- "What deadlines are mentioned?"

## 🛠️ Troubleshooting

### Common Issues

1. **OCR not working**: 
   - Ensure image quality is good
   - Try different OCR settings

2. **Table extraction failed**:
   - Use higher resolution images
   - Ensure clear table borders

3. **No API key error**:
   - Set OPENAI_API_KEY environment variable
   - Or enter it in the sidebar

### Performance Tips

- Use high-resolution images for better OCR
- Enable GPU if available for faster processing
- Specific questions get better results than general ones

## 🚀 Next Steps

1. **Deploy to Cloud**: See `docs/deployment.md` for deployment options
2. **Customize Models**: Modify `src/config.py` for different models
3. **Add Features**: Extend the system with additional document types
4. **Integrate**: Use the RAG system in your own applications

## 📚 Documentation

- `README.md`: Comprehensive project overview
- `docs/deployment.md`: Deployment guide
- `examples/README.md`: Usage examples
- Source code in `src/` directory

## 🤝 Support

- Run `python test_system.py` for diagnostics
- Check logs for detailed error information
- Ensure all dependencies are installed correctly

**Happy Document Analysis! 🎉**
