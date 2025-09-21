@echo off
echo 🚀 Deploying RL-Powered Content Converter...

REM Check if git is clean
git status --porcelain > temp_status.txt
if %errorlevel% neq 0 (
    echo ❌ Git not available or not in a git repository
    exit /b 1
)

for /f %%i in (temp_status.txt) do (
    echo ❌ Git working directory is not clean. Please commit changes first.
    del temp_status.txt
    exit /b 1
)
del temp_status.txt

REM Check if we're on main branch
for /f %%i in ('git branch --show-current') do set current_branch=%%i
if not "%current_branch%"=="main" (
    echo ⚠️  Not on main branch. Current branch: %current_branch%
    set /p continue="Continue anyway? (y/N): "
    if /i not "%continue%"=="y" exit /b 1
)

REM Push to GitHub
echo 📤 Pushing to GitHub...
git push origin %current_branch%

REM Test locally first
echo 🧪 Running local tests...
cd backend
python -m pytest tests/ -v

if %errorlevel% neq 0 (
    echo ❌ Tests failed. Please fix before deploying.
    exit /b 1
)

echo ✅ Tests passed!

REM Start local server for final test
echo 🔧 Starting local server for final test...
start /b uvicorn main:app --host 0.0.0.0 --port 8000

REM Wait for server to start
timeout /t 5 /nobreak > nul

REM Test health endpoint
echo 🏥 Testing health endpoint...
curl -f http://localhost:8000/health

if %errorlevel% neq 0 (
    echo ❌ Health check failed!
    taskkill /f /im python.exe > nul 2>&1
    exit /b 1
)

echo ✅ Health check passed!

REM Test conversion endpoint
echo 🔄 Testing conversion endpoint...
curl -X POST "http://localhost:8000/convert-content" -F "input_type=text" -F "output_type=audio" -F "input_text=Deployment test"

if %errorlevel% neq 0 (
    echo ❌ Conversion test failed!
    taskkill /f /im python.exe > nul 2>&1
    exit /b 1
)

echo ✅ Conversion test passed!

REM Stop local server
taskkill /f /im python.exe > nul 2>&1

echo.
echo 🎉 All tests passed! Ready for deployment.
echo.
echo 📋 Next steps:
echo 1. Go to https://render.com
echo 2. Connect your GitHub repository
echo 3. Create new Web Service
echo 4. Use these settings:
echo    - Name: rl-converter-api
echo    - Runtime: Python 3
echo    - Build Command: pip install --upgrade pip ^&^& pip install -r requirements.txt
echo    - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
echo    - Root Directory: backend
echo.
echo 5. Deploy and get your live API URL!
echo.
echo 📚 See DEPLOYMENT_GUIDE.md for detailed instructions.
