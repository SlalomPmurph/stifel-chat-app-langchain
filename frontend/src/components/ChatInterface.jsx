import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  CircularProgress,
  Container,
  Alert,
} from '@mui/material';
import { Send } from '@mui/icons-material';
import Message from './Message';
import { useChatContext } from '../context/ChatContext';
import { useCreateSession, useSendMessage } from '../hooks/useChatQueries';

const ChatInterface = () => {
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);
  const {
    messages,
    addMessage,
    sessionId,
    setSessionId,
    advisorId,
  } = useChatContext();

  // React Query hooks
  const createSessionMutation = useCreateSession();
  const sendMessageMutation = useSendMessage();

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Create session on mount if none exists
  useEffect(() => {
    const initializeSession = async () => {
      if (!sessionId && !createSessionMutation.isPending) {
        try {
          const response = await createSessionMutation.mutateAsync(advisorId);
          setSessionId(response.session_id);
        } catch (error) {
          console.error('Failed to create session:', error);
        }
      }
    };
    initializeSession();
  }, [sessionId, advisorId, setSessionId, createSessionMutation]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || sendMessageMutation.isPending) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    };

    // Add user message to chat
    addMessage(userMessage);
    const messageToSend = inputMessage;
    setInputMessage('');

    try {
      // Send message to backend using React Query mutation
      const response = await sendMessageMutation.mutateAsync({
        message: messageToSend,
        advisorId,
        sessionId,
      });

      // Add assistant response to chat
      const assistantMessage = {
        role: 'assistant',
        content: response.response,
        chart_data: response.chart_data,
        timestamp: new Date().toISOString(),
      };

      addMessage(assistantMessage);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };
      addMessage(errorMessage);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const isLoading = sendMessageMutation.isPending || createSessionMutation.isPending;

  return (
    <Container maxWidth="lg" sx={{ height: '100vh', display: 'flex', flexDirection: 'column', py: 2 }}>
      {/* Header */}
      <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
        <Typography variant="h5" component="h1" gutterBottom>
          Stifel Financial Advisor Chat
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Ask questions about your customers and get insights
        </Typography>
      </Paper>

      {/* Error Alert */}
      {sendMessageMutation.isError && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => sendMessageMutation.reset()}>
          Failed to send message: {sendMessageMutation.error?.message || 'Unknown error'}
        </Alert>
      )}

      {/* Messages Area */}
      <Paper
        elevation={2}
        sx={{
          flex: 1,
          p: 2,
          mb: 2,
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {messages.length === 0 ? (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: 'text.secondary',
            }}
          >
            <Typography variant="h6">
              Start a conversation by typing a message below
            </Typography>
          </Box>
        ) : (
          <Box>
            {messages.map((message, index) => (
              <Message key={index} message={message} />
            ))}
            {isLoading && (
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
                <CircularProgress size={24} />
              </Box>
            )}
            <div ref={messagesEndRef} />
          </Box>
        )}
      </Paper>

      {/* Input Area */}
      <Paper elevation={2} sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            placeholder="Ask a question about your customers..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            variant="outlined"
          />
          <IconButton
            color="primary"
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            sx={{ alignSelf: 'flex-end' }}
          >
            <Send />
          </IconButton>
        </Box>
      </Paper>
    </Container>
  );
};

export default ChatInterface;

  return (
    <Container maxWidth="lg" sx={{ height: '100vh', display: 'flex', flexDirection: 'column', py: 2 }}>
      {/* Header */}
      <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
        <Typography variant="h5" component="h1" gutterBottom>
          Stifel Financial Advisor Chat
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Ask questions about your customers and get insights
        </Typography>
      </Paper>

      {/* Messages Area */}
      <Paper
        elevation={2}
        sx={{
          flex: 1,
          p: 2,
          mb: 2,
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {messages.length === 0 ? (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: 'text.secondary',
            }}
          >
            <Typography variant="h6">
              Start a conversation by typing a message below
            </Typography>
          </Box>
        ) : (
          <Box>
            {messages.map((message, index) => (
              <Message key={index} message={message} />
            ))}
            {isLoading && (
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
                <CircularProgress size={24} />
              </Box>
            )}
            <div ref={messagesEndRef} />
          </Box>
        )}
      </Paper>

      {/* Input Area */}
      <Paper elevation={2} sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            placeholder="Ask a question about your customers..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            variant="outlined"
          />
          <IconButton
            color="primary"
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            sx={{ alignSelf: 'flex-end' }}
          >
            <Send />
          </IconButton>
        </Box>
      </Paper>
    </Container>
  );
};

export default ChatInterface;

