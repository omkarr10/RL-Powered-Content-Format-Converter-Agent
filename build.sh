#!/bin/bash

echo "🐳 Building RL Converter Docker Image..."

# Try the main Dockerfile first
echo "📦 Attempting full build with all dependencies..."
docker build -t rl-converter:full .

if [ $? -eq 0 ]; then
    echo "✅ Full build successful!"
    echo "🚀 You can run: docker run -p 8000:8000 rl-converter:full"
    exit 0
fi

echo "⚠️  Full build failed, trying lightweight version..."

# Try the lightweight version
echo "📦 Attempting lightweight build..."
docker build -f Dockerfile.light -t rl-converter:light .

if [ $? -eq 0 ]; then
    echo "✅ Lightweight build successful!"
    echo "🚀 You can run: docker run -p 8000:8000 rl-converter:light"
    echo "⚠️  Note: This version has limited AI features (gTTS only)"
    exit 0
fi

echo "❌ Both builds failed. Let's try a step-by-step approach..."

# Step-by-step build
echo "🔧 Building step by step..."

# Create a minimal Dockerfile for testing
cat > Dockerfile.minimal << 'EOF'
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg curl && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.minimal.txt .
RUN pip install --upgrade pip && pip install -r requirements.minimal.txt

COPY backend/ .
RUN mkdir -p logs temp

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Create minimal requirements
cat > backend/requirements.minimal.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic==1.10.13
ffmpeg-python==0.2.0
gtts==2.4.0
numpy==1.24.3
aiofiles==23.2.1
httpx==0.25.2
EOF

echo "📦 Attempting minimal build..."
docker build -f Dockerfile.minimal -t rl-converter:minimal .

if [ $? -eq 0 ]; then
    echo "✅ Minimal build successful!"
    echo "🚀 You can run: docker run -p 8000:8000 rl-converter:minimal"
    echo "⚠️  Note: This version has basic functionality only"
else
    echo "❌ All builds failed. Please check the error messages above."
    echo "💡 Try running locally first: cd backend && pip install -r requirements.txt"
    exit 1
fi
