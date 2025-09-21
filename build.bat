@echo off
echo 🐳 Building RL Converter Docker Image...

REM Try the main Dockerfile first
echo 📦 Attempting full build with all dependencies...
docker build -t rl-converter:full .

if %errorlevel% equ 0 (
    echo ✅ Full build successful!
    echo 🚀 You can run: docker run -p 8000:8000 rl-converter:full
    exit /b 0
)

echo ⚠️  Full build failed, trying lightweight version...

REM Try the lightweight version
echo 📦 Attempting lightweight build...
docker build -f Dockerfile.light -t rl-converter:light .

if %errorlevel% equ 0 (
    echo ✅ Lightweight build successful!
    echo 🚀 You can run: docker run -p 8000:8000 rl-converter:light
    echo ⚠️  Note: This version has limited AI features (gTTS only)
    exit /b 0
)

echo ❌ Both builds failed. Let's try a step-by-step approach...

REM Create a minimal Dockerfile for testing
echo 🔧 Creating minimal Dockerfile...
(
echo FROM python:3.9-slim
echo.
echo WORKDIR /app
echo.
echo RUN apt-get update ^&^& apt-get install -y ffmpeg curl ^&^& rm -rf /var/lib/apt/lists/*
echo.
echo COPY backend/requirements.minimal.txt .
echo RUN pip install --upgrade pip ^&^& pip install -r requirements.minimal.txt
echo.
echo COPY backend/ .
echo RUN mkdir -p logs temp
echo.
echo ENV PYTHONPATH=/app
echo ENV PYTHONUNBUFFERED=1
echo.
echo EXPOSE 8000
echo CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
) > Dockerfile.minimal

REM Create minimal requirements
echo 🔧 Creating minimal requirements...
(
echo fastapi==0.104.1
echo uvicorn[standard]==0.24.0
echo python-multipart==0.0.6
echo pydantic==1.10.13
echo ffmpeg-python==0.2.0
echo gtts==2.4.0
echo numpy==1.24.3
echo aiofiles==23.2.1
echo httpx==0.25.2
) > backend/requirements.minimal.txt

echo 📦 Attempting minimal build...
docker build -f Dockerfile.minimal -t rl-converter:minimal .

if %errorlevel% equ 0 (
    echo ✅ Minimal build successful!
    echo 🚀 You can run: docker run -p 8000:8000 rl-converter:minimal
    echo ⚠️  Note: This version has basic functionality only
) else (
    echo ❌ All builds failed. Please check the error messages above.
    echo 💡 Try running locally first: cd backend ^&^& pip install -r requirements.txt
    exit /b 1
)
