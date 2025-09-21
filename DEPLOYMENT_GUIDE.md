# 🚀 Production Deployment Guide

## Quick Start - Deploy to Render (Recommended)

### Step 1: Prepare Repository
```bash
# Ensure all files are committed
git add .
git commit -m "Production-ready RL converter"
git push origin main
```

### Step 2: Deploy to Render
1. **Go to [Render.com](https://render.com)**
2. **Connect your GitHub repository**
3. **Create New Web Service**
4. **Configure:**
   - **Name**: `rl-converter-api`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

### Step 3: Set Environment Variables
```bash
PYTHON_VERSION=3.9.16
PYTHON_PACKAGES=numpy pandas
```

### Step 4: Deploy
- Click **"Create Web Service"**
- Wait for build to complete (~5-10 minutes)
- Your API will be live at: `https://rl-converter-api.onrender.com`

## Alternative: Docker Deployment

### Local Docker

**Option 1: Full Build (Recommended)**
```bash
# Build image with all features
docker build -t rl-converter .

# Run container
docker run -p 8000:8000 rl-converter

# Test locally
curl http://localhost:8000/health
```

**Option 2: If Full Build Fails**
```bash
# Try lightweight build (faster, limited features)
docker build -f Dockerfile.light -t rl-converter:light .
docker run -p 8000:8000 rl-converter:light

# Or use the build script
# Windows
build.bat

# Linux/Mac
chmod +x build.sh
./build.sh
```

**Option 3: Minimal Build (Basic functionality only)**
```bash
# For testing/debugging
docker build -f Dockerfile.minimal -t rl-converter:minimal .
docker run -p 8000:8000 rl-converter:minimal
```

### Docker Hub + Any Cloud Provider
```bash
# Tag and push to Docker Hub
docker tag rl-converter yourusername/rl-converter:latest
docker push yourusername/rl-converter:latest

# Deploy to any cloud provider using the image
```

## Testing Your Deployment

### 1. Health Check
```bash
curl https://your-api-url.onrender.com/health
# Expected: {"status": "healthy", "service": "rl-converter"}
```

### 2. Text to Audio Test
```bash
curl -X POST "https://your-api-url.onrender.com/convert-content" \
  -F "input_type=text" \
  -F "output_type=audio" \
  -F "input_text=Hello from production!"
```

### 3. API Documentation
Visit: `https://your-api-url.onrender.com/docs`

## Team Integration

### For Ashmit's Backend Integration
```python
import requests

# Your deployed API URL
API_URL = "https://rl-converter-api.onrender.com"

def convert_content(input_type, output_type, content=None, file_path=None):
    """Convert content using the deployed RL converter."""
    
    data = {
        "input_type": input_type,
        "output_type": output_type
    }
    
    if content:
        data["input_text"] = content
    
    files = None
    if file_path:
        with open(file_path, "rb") as f:
            files = {"input_file": f}
    
    response = requests.post(f"{API_URL}/convert-content", data=data, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Conversion failed: {response.text}")

# Example usage
result = convert_content("text", "audio", "Hello team!")
print(f"Generated audio: {result['generated_audio']}")
print(f"Metadata: {result['metadata']}")
```

### Schema Integration
The API returns data in this format for easy integration:
```json
{
  "converted_content": "path/to/file",
  "metadata": {
    "duration": 12.3,
    "clarity_score": 0.9,
    "language": "en",
    "method_used": "whisper-base"
  },
  "transcript": "transcribed text...",
  "generated_audio": "path/to/audio.mp3",
  "generated_video": null,
  "feedback": {
    "clarity_score": 0.9,
    "reward": 9.0,
    "user_rating": null
  },
  "rl": {
    "state": {...},
    "action": "text2audio",
    "exploration_epsilon": 0.1
  }
}
```

## Monitoring & Maintenance

### 1. Check Logs
```bash
# Render logs (in dashboard)
# Or check local logs
tail -f backend/logs/conversions.log
tail -f backend/logs/rl_history.json
```

### 2. RL Agent Learning
- The RL agent learns from each conversion
- Q-table is persisted in `logs/q_table.json`
- Performance history in `logs/rl_history.json`
- Parameters adapt based on performance

### 3. Performance Monitoring
- Health endpoint: `/health`
- Request logging in console
- Conversion metrics in logs

## Troubleshooting

### Common Issues

1. **Docker Build Fails with pip install error**
   ```bash
   # Try the build script which tests multiple approaches
   # Windows
   build.bat
   
   # Linux/Mac
   chmod +x build.sh
   ./build.sh
   ```
   
   **Solutions:**
   - Use `Dockerfile.light` for faster builds
   - Try `Dockerfile.minimal` for basic functionality
   - Check if you have enough disk space (AI models are large)
   - Try building without cache: `docker build --no-cache -t rl-converter .`

2. **Build Fails on Render**
   - Check Python version compatibility
   - Ensure all dependencies in `requirements.txt`
   - Check build logs for specific errors
   - Try the lightweight version first

3. **API Returns 500 Errors**
   - Check application logs
   - Verify file permissions for logs directory
   - Test locally first
   - Check if all required files are present

4. **RL Agent Not Learning**
   - Check `logs/q_table.json` exists
   - Verify write permissions
   - Check `logs/rl_history.json` for updates

5. **File Upload Issues**
   - Check file size limits
   - Verify supported formats
   - Test with smaller files first

6. **Memory Issues with AI Models**
   - Use the lightweight version: `Dockerfile.light`
   - Increase Docker memory limit
   - Consider using CPU-only PyTorch builds

### Debug Commands
```bash
# Test locally
cd backend
uvicorn main:app --reload

# Check logs
ls -la logs/
cat logs/conversions.log

# Test API
curl -X POST "http://localhost:8000/convert-content" \
  -F "input_type=text" \
  -F "output_type=audio" \
  -F "input_text=test"
```

## Production Checklist

- ✅ **Dockerfile** - Containerization ready
- ✅ **CI/CD** - GitHub Actions pipeline
- ✅ **Tests** - Comprehensive test suite
- ✅ **Health Check** - `/health` endpoint
- ✅ **Logging** - Request and conversion logs
- ✅ **RL Persistence** - Q-table and history
- ✅ **Schema Alignment** - Team integration ready
- ✅ **Error Handling** - Robust error responses
- ✅ **Documentation** - API docs and examples

## Next Steps

1. **Deploy to Render** (5 minutes)
2. **Test with team** (10 minutes)
3. **Integrate with Ashmit's backend** (30 minutes)
4. **Monitor performance** (ongoing)
5. **Collect user feedback** (ongoing)

**Your RL-powered microservice is production-ready!** 🎯
