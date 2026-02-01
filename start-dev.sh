#!/bin/bash

# Stifel Chat App - Development Start Script

echo "🚀 Starting Stifel Financial Chat Application..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Node.js
if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check Python (when backend is ready)
# if ! command_exists python3; then
#     echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
#     exit 1
# fi

# Check Ollama (when backend is ready)
# if ! command_exists ollama; then
#     echo "⚠️  Ollama is not installed. Backend won't work without it."
#     echo "   Install from: https://ollama.ai"
# fi

echo "${BLUE}📦 Installing frontend dependencies...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi

echo ""
echo "${GREEN}✅ Frontend ready!${NC}"
echo ""
echo "${BLUE}🌐 Starting frontend on http://localhost:3000${NC}"
echo ""

# Start frontend
npm start

# When backend is ready, uncomment this section:
# echo "${BLUE}🐍 Starting backend on http://localhost:8000${NC}"
# cd ../backend
# if [ ! -d "venv" ]; then
#     python3 -m venv venv
#     source venv/bin/activate
#     pip install -r requirements.txt
# else
#     source venv/bin/activate
# fi
#
# # Start backend in background
# uvicorn app.main:app --reload &
# BACKEND_PID=$!
#
# # Start frontend
# cd ../frontend
# npm start
#
# # Cleanup on exit
# trap "kill $BACKEND_PID" EXIT

