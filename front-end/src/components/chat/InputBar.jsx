import React, { useState } from 'react';
import { Send, Mic, MicOff, Phone } from 'lucide-react';
import { useWebSocket } from '../../hooks/useWebSocket';
import { useVoiceInput } from '../../hooks/useVoiceInput';
import { motion } from 'framer-motion';

export default function InputBar({ onStartCall, isInCall }) {
  const [input, setInput] = useState('');
  const { sendMessage, connectionStatus } = useWebSocket();
  const { isListening, isProcessing, startListening, stopListening, transcript, error } = useVoiceInput();

  // Update input when transcript changes
  React.useEffect(() => {
    if (transcript) {
      setInput(transcript);
    }
  }, [transcript]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && connectionStatus === 'connected') {
      sendMessage(input.trim());
      setInput('');
    }
  };

  const toggleVoice = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  const isDisabled = connectionStatus !== 'connected';

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-3">
      {/* Voice Call Button (NEW - Phone Call Mode) */}
      <motion.button
        type="button"
        onClick={() => {
          console.log('📞 Phone button clicked!');
          console.log('onStartCall exists?', !!onStartCall);
          if (onStartCall) {
            onStartCall();
          } else {
            console.error('❌ onStartCall is undefined!');
          }
        }}
        disabled={isDisabled || isInCall}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className={`p-3 rounded-full transition ${
          isInCall
            ? 'bg-green-500 text-white'
            : isDisabled
            ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
            : 'bg-green-500 text-white hover:bg-green-600 shadow-md'
        }`}
        title="ابدأ مكالمة صوتية"
      >
        <Phone className="w-5 h-5" />
      </motion.button>

      {/* Voice Input Button (for single voice messages) */}
      <motion.button
        type="button"
        onClick={toggleVoice}
        disabled={isDisabled || isProcessing || isInCall}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className={`p-3 rounded-full transition ${
          isListening
            ? 'bg-red-500 text-white animate-pulse'
            : isProcessing
            ? 'bg-yellow-500 text-white'
            : isDisabled || isInCall
            ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
            : 'bg-purple-100 text-purple-600 hover:bg-purple-200'
        }`}
        title={
          isListening 
            ? 'إيقاف التسجيل' 
            : isProcessing 
            ? 'جاري المعالجة...'
            : 'رسالة صوتية واحدة'
        }
      >
        {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
      </motion.button>

      {/* Text Input */}
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={
          isInCall
            ? 'المكالمة نشطة...'
            : isDisabled
            ? 'جاري الاتصال...'
            : isProcessing
            ? 'جاري تحويل الصوت إلى نص...'
            : isListening
            ? '🎤 جاري الاستماع...'
            : 'اكتب أو 📞 اتصل صوتياً...'
        }
        disabled={isDisabled || isProcessing || isInCall}
        className="flex-1 px-6 py-3 rounded-full border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition text-right disabled:bg-gray-50 disabled:text-gray-400"
        dir="auto"
      />

      {/* Send Button */}
      <motion.button
        type="submit"
          disabled={!input.trim() || isDisabled || isInCall}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className={`p-3 rounded-full transition ${
            input.trim() && !isDisabled && !isInCall
              ? 'bg-purple-600 text-white hover:bg-purple-700 shadow-md'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          }`}
        title="إرسال"
      >
        <Send className="w-5 h-5" />
      </motion.button>
    </form>
  );
}
