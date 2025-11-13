import { useEffect, useRef } from 'react';
import { useChatStore } from '../store/chatStore';
import { MOCK_USER } from '../config/mockUser';

const WS_URL = 'ws://localhost:8000/ws';

export function useWebSocket() {
  const ws = useRef(null);
  const reconnectTimeout = useRef(null);
  const reconnectAttempts = useRef(0);
  const MAX_RECONNECT_ATTEMPTS = 5;

  const {
    addMessage,
    updateProcessSteps,
    updateTicket,
    setConnectionStatus,
    connectionStatus
  } = useChatStore();

  // Get session info from storage
  const sessionId = sessionStorage.getItem('sessionId') || `S${Date.now()}`;
  const userId = sessionStorage.getItem('userId') || MOCK_USER.id;
  const userRole = 'employee';

  const connect = () => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      return;
    }

    setConnectionStatus('connecting');

    try {
      const wsUrl = `${WS_URL}/${sessionId}/${userId}/${userRole}`;
      console.log('Connecting to WebSocket:', wsUrl);
      
      ws.current = new WebSocket(wsUrl);

      ws.current.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus('connected');
        reconnectAttempts.current = 0;
      };

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('Received:', data);

          switch (data.type) {
            case 'chat_message':
              addMessage({
                role: data.role,
                content: data.message,
                timestamp: data.timestamp
              });
              break;

            case 'process_update':
              if (data.steps) {
                updateProcessSteps(data.steps);
              }
              break;

            case 'ticket_update':
              if (data.ticket) {
                updateTicket(data.ticket);
              }
              break;

            case 'final_response':
              addMessage({
                role: 'assistant',
                content: data.message,
                timestamp: data.timestamp || new Date().toISOString()
              });
              break;

            case 'audio_response':
              // Handle audio + text response from TTS
              addMessage({
                role: 'assistant',
                content: data.text,
                audioUrl: data.audioUrl,
                timestamp: data.timestamp
              });
              console.log('[WS] Audio response received:', data.audioUrl);
              break;

            default:
              console.log('Unknown message type:', data.type);
          }
        } catch (error) {
          console.error('Error parsing message:', error);
        }
      };

      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('disconnected');
      };

      ws.current.onclose = (event) => {
        console.log('WebSocket closed:', event.code, event.reason);
        setConnectionStatus('disconnected');

        // Attempt to reconnect
        if (reconnectAttempts.current < MAX_RECONNECT_ATTEMPTS) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 10000);
          console.log(`Reconnecting in ${delay}ms...`);
          
          reconnectTimeout.current = setTimeout(() => {
            reconnectAttempts.current++;
            connect();
          }, delay);
        } else {
          console.log('Max reconnection attempts reached');
          addMessage({
            role: 'system',
            content: 'فشل الاتصال بالخادم. يرجى تحديث الصفحة.',
            timestamp: new Date().toISOString()
          });
        }
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      setConnectionStatus('disconnected');
    }
  };

  const disconnect = () => {
    if (reconnectTimeout.current) {
      clearTimeout(reconnectTimeout.current);
    }
    if (ws.current) {
      ws.current.close();
      ws.current = null;
    }
    setConnectionStatus('disconnected');
  };

  const sendMessage = (message) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      const payload = {
        type: 'user_message',
        sessionId,
        userId,
        userRole,
        message
      };
      
      console.log('Sending:', payload);
      ws.current.send(JSON.stringify(payload));

      // Add user message to chat immediately
      addMessage({
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
      });
    } else {
      console.error('WebSocket is not connected');
      addMessage({
        role: 'system',
        content: 'غير متصل. جاري محاولة إعادة الاتصال...',
        timestamp: new Date().toISOString()
      });
      connect();
    }
  };

  // Connect on mount
  useEffect(() => {
    connect();

    // Cleanup on unmount
    return () => {
      disconnect();
    };
  }, []);

  return {
    sendMessage,
    connectionStatus,
    reconnect: connect
  };
}
