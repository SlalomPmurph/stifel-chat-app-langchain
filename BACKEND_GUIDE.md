# Backend Development Guide

## Overview

This guide will help you set up the Python/FastAPI/LangChain backend for the Stifel Financial Chat Application.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Ollama installed locally
- PostgreSQL (optional for now, can use SQLite)

## Directory Structure (To Be Created)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py         # Chat endpoints
│   │   │   ├── customers.py    # Customer endpoints
│   │   │   └── charts.py       # Chart endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration
│   │   └── security.py         # Auth/security
│   ├── models/
│   │   ├── __init__.py
│   │   ├── customer.py         # Customer model
│   │   ├── account.py          # Account model
│   │   └── chat.py             # Chat session model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── langchain_service.py    # LangChain integration
│   │   ├── ollama_service.py       # Ollama integration
│   │   ├── customer_service.py     # Customer business logic
│   │   └── chart_service.py        # Chart generation
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── chat.py             # Pydantic schemas for chat
│   │   ├── customer.py         # Pydantic schemas for customer
│   │   └── chart.py            # Pydantic schemas for chart
│   └── database/
│       ├── __init__.py
│       └── session.py          # Database session
├── tests/
│   ├── __init__.py
│   ├── test_chat.py
│   └── test_customer.py
├── .env                        # Environment variables
├── .env.example                # Example env file
├── requirements.txt            # Python dependencies
└── README.md                   # Backend documentation
```

## Step-by-Step Setup

### 1. Install Ollama

```bash
# Download and install from https://ollama.ai
# Or use homebrew on macOS:
brew install ollama

# Pull the Mistral model
ollama pull mistral

# Verify installation
ollama run mistral
```

### 2. Create Backend Directory

```bash
cd /Users/patrickmurphy/Workspace/stifel-chat-app-langchain
mkdir backend
cd backend
```

### 3. Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows
```

### 4. Create requirements.txt

Create a file with these dependencies:

```txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# LangChain
langchain==0.1.0
langchain-community==0.0.10

# Ollama
ollama==0.1.6

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9  # For PostgreSQL
# OR
# aiosqlite==0.19.0  # For SQLite (simpler for development)

# Data Processing
pandas==2.1.3
numpy==1.26.2

# Utilities
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0

# CORS
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Create .env File

```env
# Application
APP_NAME=Stifel Financial Chat App
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
OLLAMA_TEMPERATURE=0.7

# Database
DATABASE_URL=postgresql://user:password@localhost/stifel_db
# OR for SQLite during development:
# DATABASE_URL=sqlite:///./stifel.db

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

### 7. Create Basic FastAPI App

**backend/app/main.py**:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="Stifel Financial Chat API",
    description="AI-powered chat for financial advisors",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Stifel Financial Chat API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import and include routers here
# from app.api.routes import chat, customers, charts
# app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
# app.include_router(customers.router, prefix="/api/v1/customers", tags=["customers"])
# app.include_router(charts.router, prefix="/api/v1/charts", tags=["charts"])
```

### 8. Create Config File

**backend/app/core/config.py**:

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Stifel Financial Chat App"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral"
    OLLAMA_TEMPERATURE: float = 0.7
    
    DATABASE_URL: str = "sqlite:///./stifel.db"
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 9. Create LangChain Service

**backend/app/services/langchain_service.py**:

```python
from langchain.llms import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from app.core.config import settings

class LangChainService:
    def __init__(self):
        self.llm = Ollama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=settings.OLLAMA_TEMPERATURE
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
    def create_agent(self, tools: list):
        """Create a LangChain agent with custom tools"""
        agent = initialize_agent(
            tools,
            self.llm,
            agent="conversational-react-description",
            memory=self.memory,
            verbose=True
        )
        return agent
    
    def chat(self, message: str, agent):
        """Send a message to the agent"""
        response = agent.run(message)
        return response

# Initialize service
langchain_service = LangChainService()
```

### 10. Create Chat Endpoint

**backend/app/api/routes/chat.py**:

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.langchain_service import langchain_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    advisor_id: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    chart_data: dict = None

@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    try:
        # Create tools for the agent
        tools = []  # Define your custom tools here
        
        # Create agent
        agent = langchain_service.create_agent(tools)
        
        # Get response
        response = langchain_service.chat(request.message, agent)
        
        return ChatResponse(
            response=response,
            session_id=request.session_id or "new-session",
            chart_data=None  # Implement chart generation logic
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 11. Run the Backend

```bash
# From the backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing with Frontend

Once the backend is running:

1. Start the backend: `uvicorn app.main:app --reload`
2. In another terminal, start the frontend: `cd frontend && npm start`
3. Open http://localhost:3000
4. Test the chat functionality!

## Custom Tools for LangChain

Create tools for customer queries:

```python
from langchain.tools import Tool

def get_customer_info(customer_id: str) -> str:
    """Get customer information"""
    # Query your database
    return f"Customer {customer_id} info"

def get_account_balance(customer_id: str) -> str:
    """Get account balance"""
    # Query your database
    return f"Account balance for {customer_id}"

tools = [
    Tool(
        name="CustomerInfo",
        func=get_customer_info,
        description="Get customer information by ID"
    ),
    Tool(
        name="AccountBalance",
        func=get_account_balance,
        description="Get account balance for a customer"
    ),
]
```

## Chart Data Generation

Return chart data in the format expected by frontend:

```python
def generate_chart_data():
    return {
        "chartType": "bar",
        "data": {
            "labels": ["Customer 1", "Customer 2", "Customer 3"],
            "datasets": [{
                "label": "Account Balance",
                "data": [50000, 75000, 100000],
                "backgroundColor": "rgba(54, 162, 235, 0.5)"
            }]
        },
        "options": {
            "plugins": {
                "title": {
                    "text": "Customer Account Balances"
                }
            }
        }
    }
```

## Next Steps

1. ✅ Set up basic FastAPI app
2. ⏳ Create database models
3. ⏳ Implement customer endpoints
4. ⏳ Add LangChain tools
5. ⏳ Implement chart generation
6. ⏳ Add authentication
7. ⏳ Connect to frontend
8. ⏳ Test end-to-end

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [LangChain Documentation](https://python.langchain.com)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)

---

**Ready to build!** Start with step 1 and work your way through. The frontend is waiting for your backend! 🚀

