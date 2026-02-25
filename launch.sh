#!/bin/bash
echo "🚀 Starting Private Cloud ROI Calculator..."
echo ""

if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

if ! docker image inspect vcf-roi-calculator > /dev/null 2>&1; then
    echo "📦 First run — building the app (this takes ~2 minutes)..."
    docker-compose build
fi

echo "✅ Starting the app..."
docker-compose up -d

echo ""
echo "🌐 App is running at: http://localhost:8501"
echo ""
echo "To stop the app run: docker-compose down"
echo ""

if [[ "$OSTYPE" == "darwin"* ]]; then
    sleep 3
    open http://localhost:8501
fi