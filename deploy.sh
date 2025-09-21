#!/bin/bash

# RL Converter Deployment Script
echo "🚀 Deploying RL-Powered Content Converter..."

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Git working directory is not clean. Please commit changes first."
    exit 1
fi

# Check if we're on main branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    echo "⚠️  Not on main branch. Current branch: $current_branch"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin $current_branch

# Test locally first
echo "🧪 Running local tests..."
cd backend
python -m pytest tests/ -v

if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Please fix before deploying."
    exit 1
fi

echo "✅ Tests passed!"

# Start local server for final test
echo "🔧 Starting local server for final test..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Test health endpoint
echo "🏥 Testing health endpoint..."
curl -f http://localhost:8000/health

if [ $? -eq 0 ]; then
    echo "✅ Health check passed!"
else
    echo "❌ Health check failed!"
    kill $SERVER_PID
    exit 1
fi

# Test conversion endpoint
echo "🔄 Testing conversion endpoint..."
curl -X POST "http://localhost:8000/convert-content" \
  -F "input_type=text" \
  -F "output_type=audio" \
  -F "input_text=Deployment test"

if [ $? -eq 0 ]; then
    echo "✅ Conversion test passed!"
else
    echo "❌ Conversion test failed!"
    kill $SERVER_PID
    exit 1
fi

# Stop local server
kill $SERVER_PID

echo ""
echo "🎉 All tests passed! Ready for deployment."
echo ""
echo "📋 Next steps:"
echo "1. Go to https://render.com"
echo "2. Connect your GitHub repository"
echo "3. Create new Web Service"
echo "4. Use these settings:"
echo "   - Name: rl-converter-api"
echo "   - Runtime: Python 3"
echo "   - Build Command: pip install --upgrade pip && pip install -r requirements.txt"
echo "   - Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo "   - Root Directory: backend"
echo ""
echo "5. Deploy and get your live API URL!"
echo ""
echo "📚 See DEPLOYMENT_GUIDE.md for detailed instructions."
