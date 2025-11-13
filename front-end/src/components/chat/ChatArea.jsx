import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import MessageBubble from './MessageBubble';
import Checklist from './Checklist';
import TypingIndicator from './TypingIndicator';
import { useChatStore } from '../../store/chatStore';
import { MessageSquare } from 'lucide-react';

const ChatArea = () => {
  const { messages, processSteps, isTyping } = useChatStore();
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping, processSteps]);
  
  const hasMessages = messages.length > 0;
  
  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {!hasMessages ? (
        /* Empty state */
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col items-center justify-center h-full text-center px-4"
        >
          <div className="w-20 h-20 bg-gradient-to-br from-qiwa-primary to-qiwa-secondary rounded-full flex items-center justify-center mb-6 shadow-lg">
            <MessageSquare className="w-10 h-10 text-white" />
          </div>
          
          <h2 className="text-2xl font-bold text-gray-800 mb-3">
            Welcome to Qiwa Assistant
          </h2>
          
          <p className="text-gray-600 mb-2 max-w-md">
            مرحباً بك في مساعد منصة قوى
          </p>
          
          <p className="text-gray-500 text-sm max-w-lg">
            I can help you manage your resume, answer questions about Qiwa services, and more.
            Just type your message below or use voice input!
          </p>
          
          <div className="mt-8 flex flex-wrap gap-3 justify-center">
            <div className="px-4 py-2 bg-purple-50 rounded-lg text-sm text-gray-600">
              💼 Manage your resume
            </div>
            <div className="px-4 py-2 bg-blue-50 rounded-lg text-sm text-gray-600">
              ❓ Ask questions
            </div>
            <div className="px-4 py-2 bg-green-50 rounded-lg text-sm text-gray-600">
              🎤 Use voice input
            </div>
          </div>
        </motion.div>
      ) : (
        /* Messages */
        <div className="max-w-4xl mx-auto">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          
          {/* Show checklist if there are process steps */}
          {processSteps.length > 0 && (
            <div className="flex justify-start">
              <Checklist steps={processSteps} />
            </div>
          )}
          
          {/* Typing indicator */}
          {isTyping && (
            <div className="flex justify-start">
              <TypingIndicator />
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
};

export default ChatArea;

