import { motion } from 'framer-motion';
import { formatTimestamp, detectArabic } from '../../lib/utils';
import { Bot, User, Volume2, VolumeX, Loader2 } from 'lucide-react';
import { useAudioPlayer } from '../../hooks/useAudioPlayer';

const API_BASE_URL = 'http://localhost:8000';

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user';
  const isArabic = detectArabic(message.content);
  const { isPlaying, currentAudio, toggleAudio } = useAudioPlayer();
  
  // Check if this message has audio and is currently playing
  const fullAudioUrl = message.audioUrl ? `${API_BASE_URL}${message.audioUrl}` : null;
  const isThisPlaying = currentAudio === fullAudioUrl && isPlaying;
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'} mb-4`}
    >
      {/* Avatar */}
      <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
        isUser 
          ? 'bg-gradient-to-br from-qiwa-primary to-qiwa-secondary' 
          : 'bg-gradient-to-br from-emerald-400 to-cyan-500'
      }`}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>
      
      {/* Message content */}
      <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} max-w-[70%]`}>
        <div className={`px-4 py-3 rounded-2xl ${
          isUser
            ? 'bg-gradient-to-br from-qiwa-primary to-qiwa-secondary text-white'
            : 'bg-white shadow-md text-gray-800'
        } ${isArabic ? 'rtl text-right' : ''}`}>
          <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
            {message.content}
          </p>
          
          {/* Audio player button for assistant messages with TTS */}
          {!isUser && message.audioUrl && (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => toggleAudio(fullAudioUrl)}
              className="mt-2 flex items-center gap-2 text-sm text-qiwa-primary hover:text-qiwa-secondary transition-colors"
            >
              {isThisPlaying ? (
                <>
                  <VolumeX className="w-4 h-4" />
                  <span>إيقاف الصوت</span>
                </>
              ) : (
                <>
                  <Volume2 className="w-4 h-4" />
                  <span>استماع للرد</span>
                </>
              )}
            </motion.button>
          )}
        </div>
        
        {message.timestamp && (
          <span className="text-xs text-gray-400 mt-1 px-2">
            {formatTimestamp(message.timestamp)}
          </span>
        )}
      </div>
    </motion.div>
  );
};

export default MessageBubble;

