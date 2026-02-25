#!/bin/bash
echo "Starting Private Cloud ROI Calculator..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Starting Docker Desktop..."
    open -a Docker
    echo "Waiting for Docker to start (30 seconds)..."
    sleep 30
fi

# Wait until Docker is ready
until docker info > /dev/null 2>&1; do
    sleep 2
done

echo "Docker is ready!"

# Build on first run
if ! docker image inspect vcf-roi-calculator > /dev/null 2>&1; then
    echo "First run - building the app (3-5 minutes)..."
    cd "$(dirname "$0")"
    docker compose build
fi

# Start the app
cd "$(dirname "$0")"
docker compose up -d

echo ""
echo "App is running at: http://localhost:8501"
echo ""
echo "To stop: docker compose down"
echo ""

# Open browser on Mac
sleep 5
open http://localhost:8501
