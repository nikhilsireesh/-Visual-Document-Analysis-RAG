#!/bin/bash
# Quick deployment script for Visual Document Analysis RAG

echo "🚀 Visual Document Analysis RAG - Deployment Script"
echo "=================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Set variables
IMAGE_NAME="visual-document-rag"
CONTAINER_NAME="visual-doc-rag-app"
PORT=8501

echo "📦 Building Docker image..."
docker build -t $IMAGE_NAME .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
else
    echo "❌ Docker build failed!"
    exit 1
fi

# Stop existing container if running
echo "🛑 Stopping existing container (if any)..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Check if .env file exists
if [ -f ".env" ]; then
    echo "📄 Found .env file, loading environment variables..."
    export $(cat .env | xargs)
fi

# Check for API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY not found in environment variables."
    echo "Please set it manually or create a .env file."
    echo "Example: export GEMINI_API_KEY='your-api-key-here'"
    echo ""
    echo "Starting container without API key (you can set it in the web interface)..."
    docker run -d \
        --name $CONTAINER_NAME \
        -p $PORT:$PORT \
        $IMAGE_NAME
else
    echo "🔑 Using GEMINI_API_KEY from environment"
    docker run -d \
        --name $CONTAINER_NAME \
        -p $PORT:$PORT \
        -e GEMINI_API_KEY="$GEMINI_API_KEY" \
        $IMAGE_NAME
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment successful!"
    echo "📱 Your app is running at: http://localhost:$PORT"
    echo ""
    echo "📊 Container status:"
    docker ps | grep $CONTAINER_NAME
    echo ""
    echo "📝 To view logs: docker logs $CONTAINER_NAME"
    echo "🛑 To stop: docker stop $CONTAINER_NAME"
    echo "🗑️  To remove: docker rm $CONTAINER_NAME"
else
    echo "❌ Container failed to start!"
    exit 1
fi
