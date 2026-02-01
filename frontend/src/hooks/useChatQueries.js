import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import chatService from '../services/chatService';

// Query keys
export const chatKeys = {
  all: ['chat'],
  sessions: () => [...chatKeys.all, 'sessions'],
  session: (sessionId) => [...chatKeys.all, 'session', sessionId],
  history: (sessionId) => [...chatKeys.all, 'history', sessionId],
};

// Hook to create a new chat session
export const useCreateSession = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (advisorId) => chatService.createSession(advisorId),
    onSuccess: (data) => {
      // Invalidate and refetch sessions
      queryClient.invalidateQueries({ queryKey: chatKeys.sessions() });
    },
  });
};

// Hook to send a chat message
export const useSendMessage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: chatService.sendMessage,
    onSuccess: (data, variables) => {
      // Invalidate chat history for this session
      queryClient.invalidateQueries({
        queryKey: chatKeys.history(variables.sessionId)
      });
    },
  });
};

// Hook to get chat history
export const useChatHistory = (sessionId, options = {}) => {
  return useQuery({
    queryKey: chatKeys.history(sessionId),
    queryFn: () => chatService.getChatHistory(sessionId),
    enabled: !!sessionId, // Only run if sessionId exists
    staleTime: 1000 * 60 * 5, // Consider data fresh for 5 minutes
    ...options,
  });
};

