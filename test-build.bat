@echo off
echo 🧪 Testing Docker Build Locally...

echo 📦 Testing minimal build first...
docker build -f Dockerfile.minimal -t rl-converter:test .

if %errorlevel% equ 0 (
    echo ✅ Minimal build successful!
    echo 🚀 Testing container...
    docker run -d --name rl-test -p 8000:8000 rl-converter:test
    
    echo ⏳ Waiting for container to start...
    timeout /t 10 /nobreak > nul
    
    echo 🏥 Testing health endpoint...
    curl -f http://localhost:8000/health
    
    if %errorlevel% equ 0 (
        echo ✅ Container is working!
        echo 🧹 Cleaning up...
        docker stop rl-test
        docker rm rl-test
        echo 🎉 Ready for deployment!
    ) else (
        echo ❌ Container health check failed
        echo 📋 Container logs:
        docker logs rl-test
        docker stop rl-test
        docker rm rl-test
    )
) else (
    echo ❌ Minimal build failed
    echo 💡 Try running: cd backend ^&^& pip install -r requirements.minimal.txt
)
