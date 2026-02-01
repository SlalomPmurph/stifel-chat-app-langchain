#!/bin/bash

# Quick start script for development

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "${BLUE}🚀 Starting Stifel Chat App Backend...${NC}"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "${GREEN}✅ Virtual environment activated${NC}"
else
    echo "❌ Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

# Check if Ollama is running
echo ""
echo "${BLUE}🤖 Checking Ollama...${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "${GREEN}✅ Ollama is running${NC}"
else
    echo "⚠️  Ollama is not running"
    echo "   Start it in another terminal: ollama serve"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start the server
echo ""
echo "${BLUE}🌐 Starting FastAPI server...${NC}"
echo ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

