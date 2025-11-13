import React from 'react';
import { motion } from 'framer-motion';
import ChatArea from '../components/chat/ChatArea';
import InputBar from '../components/chat/InputBar';
import CallMode from '../components/voice/CallMode';
import { useChatStore } from '../store/chatStore';
import { useVoiceCall } from '../hooks/useVoiceCall';

export default function ChatPage() {
  const {
    isInCall,
    isListening,
    isSpeaking,
    isProcessing,
    currentMessage,
    error,
    startCall,
    endCall,
    stopListening,  // NEW: Get stopListening
  } = useVoiceCall();

  console.log('🏠 [ChatPage] Rendered with isInCall:', isInCall);
  console.log('🏠 [ChatPage] startCall function exists?', !!startCall);

  return (
    <>
      {/* Voice Call Mode (Overlays everything when active) */}
      <CallMode
        isInCall={isInCall}
        isListening={isListening}
        isSpeaking={isSpeaking}
        isProcessing={isProcessing}
        currentMessage={currentMessage}
        onEndCall={endCall}
        onStopListening={stopListening}  // NEW: Pass stopListening
      />

      {/* Normal Chat UI (Hidden during calls) */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="flex flex-col h-full bg-gradient-to-br from-purple-50 via-white to-blue-50"
      >
        {/* Header */}
        <div className="bg-white border-b border-gray-200 p-4 shadow-sm">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-2xl font-bold text-gray-900 text-right">محادثة قوى</h1>
            <p className="text-sm text-gray-600 text-right mt-1">
              مساعدك الذكي لإدارة السيرة الذاتية والإجابة على استفساراتك
            </p>
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-hidden">
          <ChatArea />
        </div>

        {/* Input Bar */}
        <div className="bg-white border-t border-gray-200 p-4 shadow-lg">
          <div className="max-w-4xl mx-auto">
            <InputBar 
              onStartCall={startCall}
              isInCall={isInCall}
            />
          </div>
        </div>
      </motion.div>
    </>
  );
}

