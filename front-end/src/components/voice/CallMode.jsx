import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Phone, PhoneOff, Mic, MicOff, Volume2 } from 'lucide-react';

const CallMode = ({ 
  isInCall, 
  isListening, 
  isSpeaking, 
  isProcessing,
  currentMessage,
  onEndCall,
  onStopListening  // NEW: Function to manually stop listening
}) => {
  console.log('🎨 [CallMode] Rendering - isInCall:', isInCall);
  
  if (!isInCall) {
    console.log('🎨 [CallMode] Not in call, returning null');
    return null;
  }
  
  console.log('🎨 [CallMode] IN CALL! Showing full screen UI');

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="fixed inset-0 bg-gradient-to-br from-qiwa-primary via-purple-600 to-qiwa-secondary z-50 flex flex-col items-center justify-center"
      >
        {/* Call Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-2">
            مكالمة مع مساعد قوى
          </h1>
          <p className="text-white/80 text-lg">
            {isProcessing 
              ? 'جاري المعالجة...' 
              : isSpeaking 
              ? 'المساعد يتحدث...'
              : isListening 
              ? '🎤 استمع إليك...'
              : 'جاهز للاستماع'}
          </p>
        </div>

        {/* Animated Call Avatar */}
        <div className="relative mb-12">
          {/* Pulsing rings */}
          {(isListening || isSpeaking) && (
            <>
              <motion.div
                animate={{ scale: [1, 1.5, 1], opacity: [0.5, 0, 0.5] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute inset-0 rounded-full bg-white"
                style={{ width: '200px', height: '200px', left: '-25px', top: '-25px' }}
              />
              <motion.div
                animate={{ scale: [1, 1.3, 1], opacity: [0.7, 0, 0.7] }}
                transition={{ duration: 2, repeat: Infinity, delay: 0.3 }}
                className="absolute inset-0 rounded-full bg-white"
                style={{ width: '200px', height: '200px', left: '-25px', top: '-25px' }}
              />
            </>
          )}
          
          {/* Avatar Circle */}
          <div className="w-40 h-40 rounded-full bg-white flex items-center justify-center shadow-2xl relative z-10">
            {isSpeaking ? (
              <Volume2 className="w-20 h-20 text-qiwa-primary animate-pulse" />
            ) : isListening ? (
              <Mic className="w-20 h-20 text-red-500 animate-pulse" />
            ) : (
              <Phone className="w-20 h-20 text-qiwa-primary" />
            )}
          </div>
        </div>

        {/* Live Transcript (what agent is saying) */}
        {currentMessage && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-2xl mx-auto px-6 mb-12"
          >
            <div className="bg-white/20 backdrop-blur-lg rounded-2xl p-6 text-center">
              <p className="text-white text-xl leading-relaxed" dir="rtl">
                {currentMessage}
              </p>
            </div>
          </motion.div>
        )}

        {/* Call Controls */}
        <div className="flex gap-6">
          {/* Stop Listening / End Turn (Let Agent Speak) */}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={onStopListening}
            className={`w-16 h-16 rounded-full flex items-center justify-center ${
              isListening 
                ? 'bg-yellow-500 shadow-lg' 
                : 'bg-white/30 backdrop-blur-sm'
            }`}
            disabled={isProcessing || isSpeaking || !isListening}
            title={isListening ? "أوقف الاستماع ودع المساعد يتحدث" : "غير نشط"}
          >
            {isListening ? (
              <Mic className="w-8 h-8 text-white" />
            ) : (
              <MicOff className="w-8 h-8 text-white/50" />
            )}
          </motion.button>

          {/* End Call */}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={onEndCall}
            className="w-20 h-20 rounded-full bg-red-500 flex items-center justify-center shadow-2xl"
            title="إنهاء المكالمة"
          >
            <PhoneOff className="w-10 h-10 text-white" />
          </motion.button>
        </div>

        {/* Hint */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="text-white/60 text-sm mt-8 text-center max-w-md"
        >
          🟡 زر أصفر: أوقف الاستماع ودع المساعد يتحدث<br/>
          🔴 زر أحمر: إنهاء المكالمة تماماً
        </motion.p>
      </motion.div>
    </AnimatePresence>
  );
};

export default CallMode;

