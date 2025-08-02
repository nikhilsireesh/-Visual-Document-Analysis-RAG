# 🤖 Gemini Integration Guide

Your Visual Document Analysis RAG system now supports **Google Gemini API**! This provides a powerful alternative to OpenAI with competitive performance and pricing.

## 🚀 Quick Setup for Gemini

### 1. **Get Gemini API Key**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. **Set API Key**
```powershell
# Windows PowerShell
$env:GEMINI_API_KEY="your-gemini-api-key-here"

# Or create .env file
echo "GEMINI_API_KEY=your-gemini-api-key-here" > .env
```

### 3. **Run the Application**
```powershell
streamlit run app.py
```

## 🎯 **Using Gemini in the Web Interface**

1. **Open the app**: http://localhost:8501
2. **Select Provider**: In the sidebar, choose "gemini" from the dropdown
3. **Enter API Key**: Paste your Gemini API key in the text field
4. **Upload & Process**: Upload documents and ask questions!

## ⚡ **Gemini vs OpenAI Comparison**

| Feature | Gemini 1.5 Flash | GPT-3.5-turbo |
|---------|------------------|----------------|
| **Speed** | Very Fast | Fast |
| **Cost** | Lower cost | Moderate cost |
| **Context** | 1M tokens | 16K tokens |
| **Multimodal** | Native support | Limited |
| **Languages** | 100+ languages | 50+ languages |

## 🔧 **Configuration Options**

### Available Gemini Models:
- `gemini-1.5-flash` (Default - Fast & efficient)
- `gemini-1.5-pro` (More capable, slower)
- `gemini-1.0-pro` (Stable version)

### Switch Models:
```python
# In src/config.py, modify:
llm_model: str = "gemini-1.5-pro"  # or other model
```

## 📝 **Example Usage**

```powershell
# Set Gemini API key
$env:GEMINI_API_KEY="your-key-here"

# Run with Gemini (default)
streamlit run app.py

# Test the demo
python demo.py
```

## 🔄 **Switching Between Providers**

The system supports both OpenAI and Gemini:

1. **Use Gemini** (Default):
   - Set `GEMINI_API_KEY`
   - Select "gemini" in the web interface

2. **Use OpenAI**:
   - Set `OPENAI_API_KEY` 
   - Select "openai" in the web interface

## 🛠️ **Advanced Configuration**

### Environment Variables:
```bash
GEMINI_API_KEY=your-gemini-key
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-flash
```

### Programmatic Usage:
```python
from src.config import Config
from src.rag_system import RAGSystem

config = Config()
config.llm_provider = "gemini"
config.gemini_api_key = "your-key"
config.llm_model = "gemini-1.5-flash"

rag_system = RAGSystem(config, doc_processor)
```

## 💡 **Benefits of Using Gemini**

1. **Cost Effective**: Lower pricing than OpenAI
2. **Large Context**: 1M token context window
3. **Fast Processing**: Optimized for speed
4. **Multimodal**: Native image understanding
5. **Global**: Available in more regions

## 🔍 **Testing Gemini Integration**

```powershell
# Test with real Gemini API key
$env:GEMINI_API_KEY="your-actual-key"
python demo.py

# Verify in web interface
streamlit run app.py
```

## 🎉 **You're Ready!**

Your RAG system now supports both Gemini and OpenAI APIs. Choose the provider that best fits your needs:

- **Gemini**: Cost-effective, fast, large context
- **OpenAI**: Mature ecosystem, broad compatibility

Happy document analysis with Gemini! 🚀
