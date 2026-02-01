# Stifel Financial Group Chat Application - Frontend

React-based frontend for the Stifel Financial Advisor Chat Application.

## Features

- 💬 Real-time chat interface for financial advisors
- 📊 Interactive charts (Bar, Line, Pie, Doughnut) using Chart.js
- 🎨 Material-UI design system
- 🔐 Authentication and authorization ready
- 📱 Responsive design
- 💾 Local storage for chat persistence
- ⚡ Smart caching and data synchronization with React Query

## Tech Stack

- **React** 18+
- **TanStack Query (React Query)** - Server state management & caching
- **Material-UI (MUI)** - UI component library
- **Chart.js & react-chartjs-2** - Data visualization
- **Axios** - HTTP client
- **React Context API** - Client state management

## Project Structure

```
frontend/
├── public/                 # Static files
├── src/
│   ├── components/         # React components
│   │   ├── ChatInterface.jsx
│   │   ├── Message.jsx
│   │   └── ChartDisplay.jsx
│   ├── hooks/              # React Query custom hooks
│   │   ├── useChatQueries.js
│   │   ├── useCustomerQueries.js
│   │   └── useChartQueries.js
│   ├── context/            # React context providers
│   │   └── ChatContext.js
│   ├── services/           # API services
│   │   ├── api.js
│   │   ├── chatService.js
│   │   ├── customerService.js
│   │   └── chartService.js
│   ├── config/             # Configuration files
│   │   └── config.js
│   ├── utils/              # Utility functions
│   ├── App.js              # Main app component
│   ├── index.js            # Entry point
│   └── index.css           # Global styles
├── .env                    # Environment variables
├── .env.example            # Example environment variables
└── package.json            # Dependencies
```

## Getting Started

### Prerequisites

- Node.js 16+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and update the API URLs if needed.

### Development

Start the development server:
```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

### Building for Production

Create an optimized production build:
```bash
npm run build
```

### Testing

Run tests:
```bash
npm test
```

## Components

### ChatInterface
Main chat component that handles message display and input.

### Message
Renders individual chat messages with support for text and charts.

### ChartDisplay
Renders Chart.js visualizations based on data from the backend.

## Services

### chatService
Handles all chat-related API calls:
- Send messages
- Retrieve chat history
- Create chat sessions

### customerService
Manages customer data operations:
- Get customer list
- Get customer details

### chartService
Handles chart data generation requests.

## State Management

Uses React Context API for global state management:
- Chat messages
- Session information
- Loading states
- Advisor information

## Environment Variables

- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:8000)
- `REACT_APP_WS_URL` - WebSocket URL (default: ws://localhost:8000/ws)
- `REACT_APP_ENV` - Environment (development/production)

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App (one-way operation)

## Chart Types Supported

- **Bar Chart** - Customer account balances, comparisons
- **Line Chart** - Portfolio performance over time
- **Pie Chart** - Asset allocation, sector distribution
- **Doughnut Chart** - Similar to pie chart with center hole

## Future Enhancements

- [ ] WebSocket integration for real-time updates
- [ ] Advanced search and filtering
- [ ] Export chat history
- [ ] Dark mode support
- [ ] Voice input capability
- [ ] Mobile responsive improvements

## Contributing

Please follow the existing code structure and ensure all components are properly documented.

## License

Proprietary - Stifel Financial Group

