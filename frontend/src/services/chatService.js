import api from './api';

// API functions that return promises for React Query
export const chatService = {
  // Send a chat message
  sendMessage: async ({ message, advisorId, sessionId }) => {
    const response = await api.post('/api/v1/chat/message', {
      message,
      advisor_id: advisorId,
      session_id: sessionId,
    });
    return response.data;
  },

  // Get chat history
  getChatHistory: async (sessionId) => {
    const response = await api.get(`/api/v1/chat/history/${sessionId}`);
    return response.data;
  },

  // Create a new chat session
  createSession: async (advisorId) => {
    const response = await api.post('/api/v1/chat/session', {
      advisor_id: advisorId,
    });
    return response.data;
  },
};

export default chatService;

