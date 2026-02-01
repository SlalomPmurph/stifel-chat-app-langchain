#!/bin/bash

# Backend Setup Script for Stifel Chat App

echo "🚀 Setting up Stifel Chat App Backend..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "${RED}❌ Python 3 is not installed. Please install Python 3.10+${NC}"
    exit 1
fi

echo "${GREEN}✅ Python found: $(python3 --version)${NC}"

# Check if we're in the backend directory
if [ ! -f "requirements.txt" ]; then
    echo "${RED}❌ Error: requirements.txt not found${NC}"
    echo "Please run this script from the backend directory"
    exit 1
fi

# Create virtual environment
echo ""
echo "${BLUE}📦 Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "${GREEN}✅ Virtual environment created${NC}"
else
    echo "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "${BLUE}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo ""
echo "${BLUE}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo ""
echo "${BLUE}📚 Installing dependencies...${NC}"
echo "   This may take a few minutes..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "${GREEN}✅ Dependencies installed successfully${NC}"
else
    echo "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Setup environment file
echo ""
echo "${BLUE}⚙️  Setting up environment variables...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "${GREEN}✅ .env file created from .env.example${NC}"
else
    echo "${GREEN}✅ .env file already exists${NC}"
fi

# Check Ollama
echo ""
echo "${BLUE}🤖 Checking Ollama installation...${NC}"
if command -v ollama &> /dev/null; then
    echo "${GREEN}✅ Ollama is installed${NC}"

    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "${GREEN}✅ Ollama is running${NC}"

        # Check if Mistral model is installed
        if ollama list | grep -q "mistral"; then
            echo "${GREEN}✅ Mistral model is installed${NC}"
        else
            echo "${BLUE}⬇️  Pulling Mistral model...${NC}"
            ollama pull mistral
        fi
    else
        echo "${BLUE}ℹ️  Ollama is not running. Start it with: ollama serve${NC}"
    fi
else
    echo "${RED}⚠️  Ollama is not installed${NC}"
    echo "   Install from: https://ollama.ai"
    echo "   Or on macOS: brew install ollama"
fi

# Seed database
echo ""
echo "${BLUE}🌱 Would you like to seed the database with sample data? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python seed_db.py
fi

echo ""
echo "${GREEN}════════════════════════════════════════${NC}"
echo "${GREEN}✅ Backend Setup Complete!${NC}"
echo "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo "1. ${BLUE}source venv/bin/activate${NC} (if not already activated)"
echo "2. ${BLUE}ollama serve${NC} (in another terminal, if not running)"
echo "3. ${BLUE}uvicorn app.main:app --reload${NC}"
echo ""
echo "API will be available at:"
echo "  - http://localhost:8000"
echo "  - http://localhost:8000/docs (Swagger UI)"
echo ""
echo "Happy coding! 🚀"

