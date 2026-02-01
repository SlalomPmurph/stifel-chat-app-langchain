# Stifel Financial Chat Application - Backend

FastAPI backend with LangChain and Ollama integration for the Stifel Financial Advisor Chat Application.

## Features

- 🚀 FastAPI REST API
- 🤖 LangChain agent with Ollama/Mistral LLM
- 💾 SQLAlchemy ORM with SQLite (dev) / PostgreSQL (prod)
- 🔐 JWT authentication ready
- 📊 Chart data generation
- 🔄 CORS enabled for frontend
- 📝 Comprehensive logging
- ✅ Type hints with Pydantic

## Tech Stack

- **FastAPI** - Modern Python web framework
- **LangChain** - LLM orchestration framework
- **Ollama** - Local LLM hosting (Mistral model)
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **Python-Jose** - JWT tokens
- **Uvicorn** - ASGI server

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── chat.py          # Chat endpoints
│   │       ├── customers.py     # Customer endpoints
│   │       └── charts.py        # Chart generation
│   ├── core/
│   │   ├── config.py            # Settings
│   │   └── security.py          # Auth utilities
│   ├── database/
│   │   └── session.py           # Database setup
│   ├── models/
│   │   ├── customer.py          # Customer & Account models
│   │   └── chat.py              # Chat session models
│   ├── services/
│   │   ├── langchain_service.py # LangChain integration
│   │   ├── chat_service.py      # Chat operations
│   │   └── customer_service.py  # Customer operations
│   └── main.py                  # FastAPI app
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
└── seed_db.py                   # Database seeding script
```

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Ollama installed locally
- (Optional) PostgreSQL for production

## Installation

### 1. Install Ollama

```bash
# macOS
brew install ollama

# Or download from https://ollama.ai

# Pull the Mistral model
ollama pull mistral

# Verify installation
ollama run mistral
```

### 2. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env if needed
```

### 5. Seed Database (Optional)

```bash
python seed_db.py
```

This creates sample customers and accounts for testing.

## Running the Application

### Development Mode

```bash
# Make sure Ollama is running
ollama serve  # In another terminal if not running as service

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health & Info

- `GET /` - Root endpoint with app info
- `GET /health` - Health check

### Chat Endpoints

- `POST /api/v1/chat/message` - Send a chat message
  ```json
  {
    "message": "Show me customer balances",
    "advisor_id": "advisor-1",
    "session_id": "optional-session-id"
  }
  ```

- `POST /api/v1/chat/session` - Create new chat session
  ```json
  {
    "advisor_id": "advisor-1"
  }
  ```

- `GET /api/v1/chat/history/{session_id}?advisor_id=advisor-1` - Get chat history

### Customer Endpoints

- `GET /api/v1/customers?advisor_id=advisor-1` - List all customers
- `GET /api/v1/customers/{customer_id}?advisor_id=advisor-1` - Get customer details

### Chart Endpoints

- `POST /api/v1/charts/generate` - Generate chart data
  ```json
  {
    "data_type": "accounts",
    "filters": {"advisor_id": "advisor-1"},
    "chart_type": "bar"
  }
  ```

## Environment Variables

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
DATABASE_URL=sqlite:///./stifel.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/stifel_db

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Logging
LOG_LEVEL=INFO
```

## LangChain Integration

The application uses LangChain with Ollama/Mistral for AI responses.

### Available Tools

1. **CustomerInfo** - Get customer information
2. **AccountBalance** - Get account balances
3. **PortfolioSummary** - Get portfolio allocation

### Custom Tools

You can add custom tools in `app/services/langchain_service.py`:

```python
def custom_tool(input: str) -> str:
    """Your custom tool logic"""
    return "result"

Tool(
    name="CustomTool",
    func=custom_tool,
    description="What the tool does"
)
```

## Database Models

### Customer
- id, advisor_id, name, email, phone, account_status
- Relationship: One-to-Many with Accounts

### Account
- id, customer_id, account_number, account_type, balance
- Types: checking, savings, investment, retirement

### ChatSession
- id, session_id, advisor_id, started_at, ended_at
- Relationship: One-to-Many with ChatMessages

### ChatMessage
- id, session_id, role, content, chart_data, timestamp
- Roles: 'user' or 'assistant'

## Testing

```bash
# Run tests (when implemented)
pytest

# With coverage
pytest --cov=app tests/
```

## Development

### Adding a New Endpoint

1. Create route in `app/api/routes/`
2. Add service logic in `app/services/`
3. Include router in `app/main.py`

### Adding a New Model

1. Create model in `app/models/`
2. Import in `app/models/__init__.py`
3. Run `init_db()` or use Alembic for migrations

## Troubleshooting

### Ollama Not Running

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### Database Issues

```bash
# Delete and recreate database
rm stifel.db
python seed_db.py
```

### Import Errors

```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Production Deployment

### Using Docker (Recommended)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup

1. Set production environment variables
2. Use PostgreSQL for database
3. Deploy Ollama on GPU instance
4. Use proper SECRET_KEY
5. Set DEBUG=False
6. Configure proper CORS origins

## Monitoring

- **Logging**: Configured in `app/main.py`
- **Health Check**: `/health` endpoint
- **Metrics**: Add Prometheus/StatsD as needed

## Security

- JWT authentication ready (not enforced in dev)
- CORS configured
- SQL injection protection via SQLAlchemy ORM
- Input validation via Pydantic

## License

Proprietary - Stifel Financial Group

---

**Status**: ✅ Backend Complete & Ready

**Next**: Connect with frontend at http://localhost:3000

