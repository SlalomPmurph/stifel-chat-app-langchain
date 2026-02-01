# Stifel Financial Group Chat Application

An intelligent chat application built for Stifel Financial Advisors to interact with customer data and receive AI-powered insights with visual chart representations.

## Overview

This application enables Stifel financial advisors to:
- Ask questions about their customers through a conversational interface
- Receive AI-powered responses related to customer accounts and portfolios
- View interactive charts and visualizations (Chart.js)
- Access customer information securely

## Architecture

```
┌─────────────────────────────────────────┐
│      React Frontend (Port 3000)         │
│  - Chat Interface                       │
│  - Chart.js Visualizations              │
│  - Material-UI Components               │
└──────────────┬──────────────────────────┘
               │ REST API
┌──────────────▼──────────────────────────┐
│  Python/LangChain Backend (Port 8000)   │
│  - FastAPI REST API                     │
│  - LangChain Agent                      │
│  - Ollama + Mistral (Local LLM)         │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Data Layer                      │
│  - PostgreSQL Database                  │
│  - Customer & Account Data              │
└─────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **React** 18+
- **TanStack Query (React Query)** - Server state management
- **Material-UI (MUI)** - UI components
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **React Context API** - Client state management

### Backend
- **Python** 3.10+
- **FastAPI** - REST API framework
- **LangChain** - LLM orchestration
- **Ollama** - Local LLM hosting
- **Mistral** - Language model (runs locally)
- **SQLAlchemy** - Database ORM
- **Pandas** - Data processing

### Database
- **PostgreSQL** - Primary database

## Project Structure

```
stifel-chat-app-langchain/
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   ├── context/        # State management
│   │   └── config/         # Configuration
│   └── package.json
├── backend/                # Python/FastAPI backend (to be created)
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── services/      # Business logic
│   │   ├── models/        # Database models
│   │   └── main.py        # Entry point
│   └── requirements.txt
├── context/                # Documentation
│   ├── project_overview.md
│   └── implementation.md
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- **Node.js** 16+ and npm
- **Python** 3.10+
- **Ollama** installed locally
- **PostgreSQL** (optional for now)

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

The frontend will be available at [http://localhost:3000](http://localhost:3000)

### Backend Setup (Coming Soon)

The backend will be set up with:
- FastAPI framework
- LangChain integration
- Ollama/Mistral for local LLM processing

### Ollama Setup

1. Install Ollama from [https://ollama.ai](https://ollama.ai)

2. Pull the Mistral model:
```bash
ollama pull mistral
```

3. Verify installation:
```bash
ollama run mistral
```

## Features

### Current Features (Frontend)
✅ Chat interface with message history
✅ Material-UI design system
✅ Chart display component (Bar, Line, Pie, Doughnut)
✅ API service layer ready
✅ Context-based state management
✅ Local storage persistence

### Upcoming Features (Backend)
🔄 FastAPI REST endpoints
🔄 LangChain agent with custom tools
🔄 Ollama/Mistral integration
🔄 Customer data management
🔄 Chart data generation
🔄 Authentication & authorization

## Development Workflow

### Phase 1: ✅ Foundation
- [x] React project setup
- [x] Material-UI integration
- [x] Chart.js components
- [x] API service layer
- [x] Context providers
- [ ] Python/FastAPI backend setup

### Phase 2: Backend Implementation
- [ ] FastAPI project structure
- [ ] Database models and migrations
- [ ] LangChain integration with Ollama
- [ ] Custom LangChain tools
- [ ] API endpoints

### Phase 3: Integration
- [ ] Connect frontend to backend
- [ ] WebSocket for real-time chat
- [ ] Chart data generation
- [ ] Customer data integration

### Phase 4: Security & Testing
- [ ] Authentication implementation
- [ ] Authorization and access control
- [ ] Unit and integration tests
- [ ] E2E testing

## Environment Variables

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_ENV=development
```

### Backend (.env) - Coming Soon
```
DATABASE_URL=postgresql://user:pass@localhost/stifel_db
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
SECRET_KEY=your-secret-key
```

## Documentation

Detailed documentation is available in the `/context` directory:
- [Project Overview](./context/project_overview.md) - High-level project description
- [Implementation Guide](./context/implementation.md) - Detailed technical implementation

## Chart Types

The application supports multiple chart types for data visualization:

- **Bar Charts** - Account balances, comparisons
- **Line Charts** - Portfolio performance over time
- **Pie Charts** - Asset allocation
- **Doughnut Charts** - Sector distribution

## Security

- JWT-based authentication (planned)
- Role-based access control
- Advisor can only access their assigned customers
- Data encryption in transit and at rest
- Compliance with FINRA regulations

## Why Ollama + Mistral?

We're using Ollama with the Mistral model instead of OpenAI because:
- **No API costs** - Runs entirely locally
- **Data privacy** - Customer data never leaves your infrastructure
- **No API key required** - No external dependencies
- **Full control** - Customize and fine-tune as needed
- **LangChain compatible** - Works seamlessly with LangChain

## Contributing

1. Follow the project structure
2. Write tests for new features
3. Document all components and functions
4. Follow code style guidelines

## License

Proprietary - Stifel Financial Group

## Support

For questions or issues, please contact the development team.

---

**Status**: 🚧 In Development - Frontend Complete, Backend In Progress

