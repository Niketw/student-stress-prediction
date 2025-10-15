#!/bin/bash

# Student Stress Prediction - Start Docker Containers (Linux/Mac)

echo ""
echo "========================================"
echo "Student Stress Prediction Application"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi

# Check if Docker daemon is running
if ! docker ps &> /dev/null; then
    echo "ERROR: Docker daemon is not running"
    echo "Please start Docker and try again"
    exit 1
fi

echo "Building and starting containers..."
echo ""

# Build and start containers
docker-compose up -d --build

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to start containers"
    exit 1
fi

echo ""
echo "========================================"
echo "✓ Containers started successfully!"
echo "========================================"
echo ""
echo "Services:"
echo "  - Frontend: http://localhost:5173"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop containers:"
echo "  docker-compose down"
echo ""
