@echo off
REM Quick deployment script for Visual Document Analysis RAG (Windows)

echo 🚀 Visual Document Analysis RAG - Deployment Script
echo ==================================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Set variables
set IMAGE_NAME=visual-document-rag
set CONTAINER_NAME=visual-doc-rag-app
set PORT=8501

echo 📦 Building Docker image...
docker build -t %IMAGE_NAME% .

if %errorlevel% equ 0 (
    echo ✅ Docker image built successfully!
) else (
    echo ❌ Docker build failed!
    pause
    exit /b 1
)

REM Stop existing container if running
echo 🛑 Stopping existing container if any...
docker stop %CONTAINER_NAME% 2>nul
docker rm %CONTAINER_NAME% 2>nul

REM Check if API key is set
if "%GEMINI_API_KEY%"=="" (
    echo ⚠️  GEMINI_API_KEY not found in environment variables.
    echo Please set it manually or add it to your environment.
    echo Example: set GEMINI_API_KEY=your-api-key-here
    echo.
    echo Starting container without API key you can set it in the web interface...
    docker run -d --name %CONTAINER_NAME% -p %PORT%:%PORT% %IMAGE_NAME%
) else (
    echo 🔑 Using GEMINI_API_KEY from environment
    docker run -d --name %CONTAINER_NAME% -p %PORT%:%PORT% -e GEMINI_API_KEY="%GEMINI_API_KEY%" %IMAGE_NAME%
)

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Deployment successful!
    echo 📱 Your app is running at: http://localhost:%PORT%
    echo.
    echo 📊 Container status:
    docker ps | findstr %CONTAINER_NAME%
    echo.
    echo 📝 To view logs: docker logs %CONTAINER_NAME%
    echo 🛑 To stop: docker stop %CONTAINER_NAME%
    echo 🗑️  To remove: docker rm %CONTAINER_NAME%
    echo.
    echo Opening browser...
    start http://localhost:%PORT%
) else (
    echo ❌ Container failed to start!
    pause
    exit /b 1
)

pause
