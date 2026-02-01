const config = {
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  wsUrl: process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws',
  environment: process.env.REACT_APP_ENV || 'development',
};

export default config;

