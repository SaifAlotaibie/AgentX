import { create } from 'zustand';

const useChatStore = create((set) => ({
  // State
  messages: [],
  processSteps: [],
  tickets: [],
  connectionStatus: 'disconnected', // 'connecting' | 'connected' | 'disconnected' | 'error'
  isTyping: false,
  sessionId: `S${Date.now()}`,
  userId: `U${Date.now()}`,
  currentTicketId: null,
  
  // Actions
  addMessage: (message) => set((state) => {
    // Prevent duplicate messages (check last 3 messages for same content)
    const lastMessages = state.messages.slice(-3);
    const isDuplicate = lastMessages.some(
      m => m.content === message.content && m.role === message.role
    );
    
    if (isDuplicate) {
      console.log('Duplicate message prevented:', message.content);
      return state; // Don't add duplicate
    }
    
    // Add message with audioUrl if present
    return {
      messages: [...state.messages, { 
        ...message, 
        id: Date.now() + Math.random(),
        audioUrl: message.audioUrl || null // Include audio URL for TTS responses
      }]
    };
  }),
  
  updateProcessSteps: (steps) => set({ processSteps: steps }),
  
  addTicket: (ticket) => set((state) => ({
    tickets: [ticket, ...state.tickets],
    currentTicketId: ticket.ticketId
  })),
  
  updateTicket: (updatedTicket) => set((state) => ({
    tickets: state.tickets.map(t => 
      t.ticketId === updatedTicket.ticketId ? updatedTicket : t
    )
  })),
  
  setConnectionStatus: (status) => set({ connectionStatus: status }),
  
  setIsTyping: (isTyping) => set({ isTyping }),
  
  clearChat: () => set({ 
    messages: [], 
    processSteps: [], 
    isTyping: false,
    currentTicketId: null 
  }),
  
  // Stats for dashboard
  getStats: () => {
    const state = useChatStore.getState();
    return {
      totalMessages: state.messages.length,
      userMessages: state.messages.filter(m => m.role === 'user').length,
      assistantMessages: state.messages.filter(m => m.role === 'assistant').length,
      totalTickets: state.tickets.length,
      openTickets: state.tickets.filter(t => t.status === 'open').length,
      closedTickets: state.tickets.filter(t => t.status === 'closed').length,
    };
  },
}));

export { useChatStore };

