@echo off
REM Student Stress Prediction - Start Docker Containers (Windows)

echo.
echo ========================================
echo Student Stress Prediction Application
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker daemon is running
docker ps >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker daemon is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)

echo Building and starting containers...
echo.

REM Build and start containers
docker-compose up -d --build

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start containers
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✓ Containers started successfully!
echo ========================================
echo.
echo Services:
echo   - Frontend: http://localhost:5173
echo   - Backend API: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
echo To stop containers:
echo   docker-compose down
echo.
pause
