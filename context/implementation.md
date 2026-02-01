# Implementation Guide

## Stifel Financial Group Chat Application

This document outlines the implementation details for building the Stifel Financial Group Chat Application.

---

## Architecture Overview

### System Architecture
```
┌─────────────────────────────────────────┐
│           React Frontend                │
│  - Chat Interface                       │
│  - Chart.js Visualizations              │
│  - Customer Data Display                │
└──────────────┬──────────────────────────┘
               │ REST API / WebSocket
┌──────────────▼──────────────────────────┐
│       Python/LangChain Backend          │
│  - LangChain Agent                      │
│  - Customer Data Processing             │
│  - Chart Data Generation                │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Data Sources                    │
│  - Customer Database                    │
│  - Financial Data APIs                  │
│  - Ollama (Local LLM - Mistral)         │
└─────────────────────────────────────────┘
```

---

## Frontend Implementation

### Tech Stack
- **React** (v18+)
- **Chart.js** (v4+) with react-chartjs-2
- **Axios** for API communication
- **WebSocket** for real-time chat updates
- **TailwindCSS** or **Material-UI** for styling

### Key Components

#### 1. ChatInterface Component
```
/src/components/ChatInterface.jsx
- Main chat container
- Message display area
- Input field for advisor queries
- Auto-scroll functionality
```

#### 2. Message Component
```
/src/components/Message.jsx
- Renders individual chat messages
- Supports text and chart responses
- Differentiates user vs assistant messages
- Timestamp display
```

#### 3. ChartDisplay Component
```
/src/components/ChartDisplay.jsx
- Renders Chart.js visualizations
- Supports multiple chart types:
  * Bar charts (customer accounts)
  * Line charts (portfolio performance)
  * Pie charts (asset allocation)
  * Doughnut charts (sector distribution)
- Interactive tooltips and legends
```

#### 4. CustomerDataPanel Component
```
/src/components/CustomerDataPanel.jsx
- Display customer information
- Quick access to customer details
- Filter and search capabilities
```

### State Management
- **React Context** or **Redux** for global state
- Manage:
  - Chat history
  - Current advisor session
  - Customer data cache
  - Loading states

### API Integration
```javascript
// Example API structure
/api/chat/message          // POST - Send chat message
/api/chat/history          // GET - Retrieve chat history
/api/customers             // GET - Get customer list
/api/customers/:id         // GET - Get specific customer data
/api/charts/generate       // POST - Generate chart data
```

---

## Backend Implementation

### Tech Stack
- **Python** (3.10+)
- **LangChain** for LLM orchestration
- **FastAPI** for REST API
- **WebSocket** support for real-time communication
- **SQLAlchemy** for database ORM
- **Pandas** for data processing
- **Ollama** for local LLM hosting
- **Mistral** (or Llama2) as the LLM model

### Project Structure
```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry
│   ├── config.py               # Configuration settings
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py         # Chat endpoints
│   │   │   ├── customers.py    # Customer endpoints
│   │   │   └── charts.py       # Chart data endpoints
│   ├── services/
│   │   ├── langchain_service.py   # LangChain integration
│   │   ├── customer_service.py    # Customer data logic
│   │   └── chart_service.py       # Chart data generation
│   ├── models/
│   │   ├── customer.py         # Customer data models
│   │   ├── chat.py             # Chat message models
│   │   └── advisor.py          # Advisor models
│   ├── database/
│   │   ├── db.py               # Database connection
│   │   └── repositories/       # Data access layer
│   └── utils/
│       ├── security.py         # Authentication & authorization
│       └── helpers.py          # Utility functions
├── requirements.txt
└── .env.example
```

### LangChain Integration

#### Agent Setup
```python
1. LLM (Ollama with Mistral model - runs locally)
1. LLM (OpenAI GPT-4 or Anthropic Claude)
2. Custom tools for:
   - Customer data retrieval
   - Account information queries
   - Chart data generation
   - Portfolio analysis
3. Memory management for conversation context

# Example LangChain setup with Ollama:
from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

llm = Ollama(model="mistral", base_url="http://localhost:11434")
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=[customer_tool, account_tool, chart_tool, portfolio_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)
4. Prompt templates for financial advisor context
```

#### Custom LangChain Tools
1. **CustomerDataTool**
   - Query customer information
   - Filter by advisor access permissions
   
2. **AccountQueryTool**
   - Retrieve account balances
   - Get transaction history
   
3. **ChartGeneratorTool**
   - Process data for visualization
   - Return Chart.js compatible format
   
4. **PortfolioAnalysisTool**
   - Calculate portfolio metrics
   - Performance analysis

### API Endpoints

#### Chat Endpoints
```python
POST /api/v1/chat/message
- Request: { "message": str, "advisor_id": str, "session_id": str }
- Response: { "response": str, "chart_data": dict, "metadata": dict }

GET /api/v1/chat/history/{session_id}
- Response: { "messages": [...] }
```

#### Customer Endpoints
```python
GET /api/v1/customers
- Query params: advisor_id
- Response: { "customers": [...] }

GET /api/v1/customers/{customer_id}
- Response: { "customer": {...}, "accounts": [...] }
```

#### Chart Endpoints
```python
POST /api/v1/charts/generate
- Request: { "data_type": str, "filters": dict, "chart_type": str }
- Response: { "chartData": {...}, "chartOptions": {...} }
```

### Security Implementation
1. **Authentication**
   - JWT tokens for advisor sessions
   - OAuth 2.0 integration with corporate SSO
   
2. **Authorization**
   - Role-based access control (RBAC)
   - Advisor can only access their assigned customers
   - Data isolation per advisor

3. **Data Protection**
   - Encryption at rest and in transit
   - PII data masking in logs
   - Compliance with financial regulations (SOC 2, FINRA)

---

## Database Schema

### Core Tables

#### advisors
```sql
- id (PK)
- email
- name
- employee_id
- created_at
- updated_at
```

#### customers
```sql
- id (PK)
- advisor_id (FK)
- name
- email
- phone
- account_status
- created_at
- updated_at
```

#### accounts
```sql
- id (PK)
- customer_id (FK)
- account_number
- account_type
- balance
- created_at
- updated_at
```

#### chat_sessions
```sql
- id (PK)
- advisor_id (FK)
- started_at
- ended_at
```

#### chat_messages
```sql
- id (PK)
- session_id (FK)
- role (user/assistant)
- content
- chart_data (JSON)
- timestamp
```

---

## Chart.js Integration

### Supported Chart Types

#### 1. Customer Accounts Bar Chart
```javascript
{
  type: 'bar',
  data: {
    labels: ['Checking', 'Savings', 'Investment', 'Retirement'],
    datasets: [{
      label: 'Account Balances',
      data: [12500, 45000, 125000, 350000]
    }]
  }
}
```

#### 2. Portfolio Performance Line Chart
```javascript
{
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
      label: 'Portfolio Value',
      data: [450000, 465000, 455000, 480000, 490000, 510000]
    }]
  }
}
```

#### 3. Asset Allocation Pie Chart
```javascript
{
  type: 'pie',
  data: {
    labels: ['Stocks', 'Bonds', 'Cash', 'Real Estate'],
    datasets: [{
      data: [45, 30, 15, 10]
    }]
  }
}
```

### Chart Response Format
Backend returns standardized chart data:
```json
{
  "type": "chart",
  "chartType": "bar|line|pie|doughnut",
  "data": {
    "labels": [...],
- [ ] Install and configure Ollama locally
- [ ] Pull Mistral model (`ollama pull mistral`)
    "datasets": [...]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": { "text": "Chart Title" },
      "legend": { "display": true }
- [ ] Integrate LangChain with Ollama/Mistral
- [ ] Test LLM responses and adjust prompts
  }
}
```

---

## Development Workflow

### Phase 1: Foundation (Weeks 1-2)
- [ ] Set up React project structure
- [ ] Set up Python/FastAPI backend
- [ ] Database schema design and migration
- [ ] Basic authentication system
- [ ] Development environment configuration

### Phase 2: Core Chat Functionality (Weeks 3-4)
- [ ] Implement chat UI components
- [ ] Create FastAPI chat endpoints
- [ ] Integrate LangChain with basic LLM
- [ ] Implement WebSocket for real-time chat
- [ ] Build conversation memory system

### Phase 3: Customer Data Integration (Weeks 5-6)
- [ ] Customer data API endpoints
- [ ] LangChain custom tools for data retrieval
- [ ] Implement advisor-customer access control
- [ ] Customer data display components

### Phase 4: Chart Integration (Weeks 7-8)
- [ ] Chart.js component library
- [ ] Chart data generation service
- [ ] LangChain tool for chart requests
- [ ] Chart rendering in chat interface
- [ ] Interactive chart features

### Phase 5: Security & Testing (Weeks 9-10)
- [ ] Security audit and hardening
- [ ] Unit and integration tests
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Documentation

### Phase 6: Deployment (Week 11-12)
- [ ] Production environment setup
- [ ] CI/CD pipeline configuration
- [ ] Monitoring and logging setup
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
- [ ] Production deployment

---

## Environment Variables

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_ENV=development
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@localhost/stifel_db
OPENAI_API_KEY=sk-...
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

---

## Testing Strategy

### Frontend Tests
- **Unit Tests**: Jest + React Testing Library
- **Ollama**: Deploy on dedicated GPU instances for production
- **Component Tests**: Test chat interface, charts, forms
- **E2E Tests**: Cypress for user workflows

#### Ollama Production Considerations
- Use GPU-enabled instances (AWS g4dn, g5 series)
- Run Ollama as a systemd service
- Consider multiple Ollama instances behind load balancer
- Monitor GPU memory and model response times

### Backend Tests
- **Unit Tests**: pytest for services and utilities
- **Integration Tests**: API endpoint testing
- **LangChain Tests**: Mock LLM responses
- **Load Tests**: Locust for performance testing
- **Ollama Monitoring**: Track model performance and response times

---

## Deployment Considerations

### Frontend Deployment
- **Hosting**: Vercel, Netlify, or AWS S3 + CloudFront
- **Build**: Production-optimized React build
- **CDN**: Static asset distribution

### Backend Deployment
- **Hosting**: AWS EC2, ECS, or Google Cloud Run
- **Database**: AWS RDS (PostgreSQL) or managed database
- **Scaling**: Horizontal scaling with load balancer
- **Caching**: Redis for session and data caching

### Monitoring
- **Application Monitoring**: DataDog, New Relic, or Sentry
- **Logging**: ELK Stack or CloudWatch
- **Uptime Monitoring**: Pingdom or UptimeRobot
- **LLM Monitoring**: LangSmith for LangChain tracing

---

## Security Best Practices

1. **API Security**
   - Rate limiting on endpoints
   - Input validation and sanitization
   - SQL injection prevention (use ORM)
   - XSS protection

2. **Data Security**
   - Encrypt sensitive data at rest
   - Use HTTPS/TLS for all communications
   - Implement audit logging
   - Regular security audits

3. **Compliance**
   - FINRA regulations compliance
   - SOC 2 certification requirements
   - Data retention policies
   - Privacy policy implementation

---

## Future Enhancements

- **Voice Input**: Speech-to-text for advisor queries
- **Multi-language Support**: Internationalization
- **Advanced Analytics**: Predictive insights using ML
- **Mobile App**: React Native mobile version
- **Document Analysis**: Upload and analyze financial documents
- **Email Integration**: Send charts and reports via email
- **Collaboration**: Share insights with team members
- **Custom Dashboards**: Personalized advisor dashboards

