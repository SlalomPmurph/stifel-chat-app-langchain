import React from 'react';
import { Box, Paper, Typography, Avatar } from '@mui/material';
import { Person, SmartToy } from '@mui/icons-material';
import ChartDisplay from './ChartDisplay';

const Message = ({ message }) => {
  const isUser = message.role === 'user';
  const isAssistant = message.role === 'assistant';

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        mb: 2,
      }}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: isUser ? 'row-reverse' : 'row',
          alignItems: 'flex-start',
          maxWidth: '80%',
        }}
      >
        <Avatar
          sx={{
            bgcolor: isUser ? 'primary.main' : 'secondary.main',
            mx: 1,
          }}
        >
          {isUser ? <Person /> : <SmartToy />}
        </Avatar>

        <Box>
          <Paper
            elevation={1}
            sx={{
              p: 2,
              bgcolor: isUser ? 'primary.light' : 'grey.100',
              color: isUser ? 'primary.contrastText' : 'text.primary',
              borderRadius: 2,
            }}
          >
            <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
              {message.content}
            </Typography>

            {message.timestamp && (
              <Typography
                variant="caption"
                sx={{
                  display: 'block',
                  mt: 1,
                  opacity: 0.7,
                }}
              >
                {new Date(message.timestamp).toLocaleTimeString()}
              </Typography>
            )}
          </Paper>

          {/* Display chart if present */}
          {isAssistant && message.chart_data && (
            <ChartDisplay chartData={message.chart_data} />
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default Message;

