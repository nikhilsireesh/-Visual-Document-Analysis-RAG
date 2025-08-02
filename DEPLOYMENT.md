# 🚀 Deployment Guide for Visual Document Analysis RAG System

This guide covers multiple deployment options for your Visual Document Analysis RAG system.

## 📋 Pre-Deployment Checklist

Before deploying, ensure:
- ✅ All dependencies are in `requirements.txt`
- ✅ Gemini API key is available
- ✅ Application runs locally without errors
- ✅ Documents can be processed and queried successfully

## 🌐 Deployment Options

### 1. 🎯 **Streamlit Cloud (Recommended - Free)**

Streamlit Cloud is the easiest and fastest way to deploy your app for free.

#### Steps:
1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Visual Document Analysis RAG"
   git branch -M main
   git remote add origin https://github.com/yourusername/visual-document-rag.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select: `main` branch, `app.py` file
   - Click "Deploy!"

3. **Add Secrets:**
   - In Streamlit Cloud dashboard, go to "Secrets"
   - Add your API key:
   ```toml
   GEMINI_API_KEY = "AIzaSyANnJSYo_Y1aU0r3nH3kir1MUxZ8S2Bf6I"
   ```

#### Pros:
- ✅ Free tier available
- ✅ Easy to deploy
- ✅ Automatic SSL
- ✅ Integrated with GitHub

#### Cons:
- ⚠️ Limited to 1GB RAM
- ⚠️ CPU-only (no GPU acceleration)

---

### 2. 🤗 **Hugging Face Spaces (Free)**

Great for ML applications with good community visibility.

#### Steps:
1. **Create Space:**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Streamlit" as framework
   - Name: `visual-document-analysis-rag`

2. **Upload Files:**
   - Upload all your project files
   - Ensure `requirements.txt` includes all dependencies

3. **Add Secrets:**
   - Go to Space settings → "Repository secrets"
   - Add: `GEMINI_API_KEY = "your-api-key"`

4. **Create `app.py` if needed:**
   Your existing `app.py` should work directly.

#### Pros:
- ✅ Free with good limits
- ✅ ML-focused platform
- ✅ Good for showcasing
- ✅ Easy sharing

---

### 3. ☁️ **Google Cloud Platform**

Best for production use with scalability.

#### Steps:
1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   # Install system dependencies
   RUN apt-get update && apt-get install -y \\
       libgl1-mesa-glx \\
       libglib2.0-0 \\
       libsm6 \\
       libxext6 \\
       libxrender-dev \\
       libgomp1 \\
       libgthread-2.0-0 \\
       && rm -rf /var/lib/apt/lists/*

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8501

   HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

   ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy visual-document-rag \\
     --source . \\
     --platform managed \\
     --region us-central1 \\
     --allow-unauthenticated \\
     --memory 4Gi \\
     --cpu 2 \\
     --set-env-vars GEMINI_API_KEY="your-api-key"
   ```

#### Pros:
- ✅ Production-ready
- ✅ Auto-scaling
- ✅ Pay-per-use
- ✅ High performance

---

### 4. 🐳 **Docker + Any Cloud Provider**

Universal deployment option.

#### Create Dockerfile:
```dockerfile
FROM python:3.11-slim

# Install system dependencies for OpenCV and OCR
RUN apt-get update && apt-get install -y \\
    libgl1-mesa-glx \\
    libglib2.0-0 \\
    libsm6 \\
    libxext6 \\
    libxrender-dev \\
    libgomp1 \\
    libgthread-2.0-0 \\
    tesseract-ocr \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run:
```bash
# Build
docker build -t visual-document-rag .

# Run locally
docker run -p 8501:8501 -e GEMINI_API_KEY="your-api-key" visual-document-rag

# Push to registry
docker tag visual-document-rag your-registry/visual-document-rag
docker push your-registry/visual-document-rag
```

---

### 5. 🔴 **Railway (Simple & Fast)**

Modern deployment platform with great developer experience.

#### Steps:
1. **Connect GitHub:**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository

2. **Add Environment Variables:**
   ```
   GEMINI_API_KEY=your-api-key
   PORT=8501
   ```

3. **Create `railway.toml`:**
   ```toml
   [build]
   builder = "NIXPACKS"

   [deploy]
   healthcheckPath = "/_stcore/health"
   healthcheckTimeout = 100
   restartPolicyType = "ON_FAILURE"
   ```

---

## 🔧 **Deployment Configuration Files**

### Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
address = "0.0.0.0"
maxUploadSize = 200

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[browser]
gatherUsageStats = false
```

### Update `requirements.txt` for deployment:
```txt
streamlit>=1.28.0
python-dotenv>=1.0.0
chromadb>=0.4.15
langchain>=0.1.0
langchain-community>=0.0.10
sentence-transformers>=2.2.2
PyPDF2>=3.0.1
pdf2image>=1.16.3
pillow>=10.0.1
python-docx>=0.8.11
pytesseract>=0.3.10
opencv-python-headless>=4.8.1.78
easyocr>=1.7.0
pandas>=2.1.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0
tabula-py>=2.8.2
google-generativeai>=0.3.0
requests>=2.31.0
python-multipart>=0.0.6
aiofiles>=23.2.1
```

### Create `app_config.py` for deployment settings:
```python
import os
import streamlit as st

# Deployment configuration
def configure_for_deployment():
    \"\"\"Configure app for deployment environment.\"\"\"
    
    # Set page config for better mobile experience
    st.set_page_config(
        page_title="Visual Document Analysis RAG",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add deployment-specific CSS
    st.markdown(\"\"\"
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stSelectbox label {
        font-weight: bold;
    }
    </style>
    \"\"\", unsafe_allow_html=True)
```

## 🎯 **Recommended Deployment Strategy**

### For Development/Demo:
1. **Streamlit Cloud** - Quick and free

### For Production:
1. **Google Cloud Run** - Scalable and reliable
2. **Docker + AWS ECS** - Enterprise-grade

### For Showcase:
1. **Hugging Face Spaces** - Great for ML community

## 🔒 **Security Considerations**

1. **API Keys:**
   - Never commit API keys to version control
   - Use environment variables or secrets management
   - Rotate keys regularly

2. **File Upload Security:**
   - Validate file types and sizes
   - Scan uploaded files for malware
   - Implement rate limiting

3. **Access Control:**
   - Add authentication if needed
   - Use HTTPS only
   - Implement proper CORS headers

## 📊 **Monitoring & Performance**

1. **Add Health Checks:**
   ```python
   @st.cache_data
   def health_check():
       return {"status": "healthy", "timestamp": datetime.now()}
   ```

2. **Monitor Resources:**
   - CPU and memory usage
   - API call limits
   - Response times

3. **Error Tracking:**
   - Implement logging
   - Use error tracking services (Sentry)
   - Monitor API quota usage

## 🚀 **Quick Deploy Commands**

Choose your preferred method and run these commands:

### Streamlit Cloud:
```bash
git init && git add . && git commit -m "Deploy Visual Document RAG"
# Push to GitHub, then deploy on share.streamlit.io
```

### Docker:
```bash
docker build -t visual-doc-rag .
docker run -p 8501:8501 -e GEMINI_API_KEY="your-key" visual-doc-rag
```

### Google Cloud:
```bash
gcloud run deploy --source . --allow-unauthenticated
```

---

**Ready to deploy? Choose the option that best fits your needs!** 🚀
