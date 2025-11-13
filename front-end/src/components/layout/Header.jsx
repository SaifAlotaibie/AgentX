import { Bot } from 'lucide-react';
import { useChatStore } from '../../store/chatStore';

const Header = () => {
  const { connectionStatus } = useChatStore();
  
  return (
    <header className="bg-gradient-to-r from-qiwa-primary to-qiwa-secondary text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and title */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold">Qiwa Assistant</h1>
              <p className="text-xs opacity-90">مساعد منصة قوى</p>
            </div>
          </div>
          
          {/* Connection indicator */}
          <div className="flex items-center gap-2 bg-white/10 px-3 py-1.5 rounded-full">
            <div className={`w-2 h-2 rounded-full ${
              connectionStatus === 'connected' 
                ? 'bg-green-400' 
                : connectionStatus === 'connecting'
                ? 'bg-amber-400 animate-pulse'
                : 'bg-red-400'
            }`}></div>
            <span className="text-xs font-medium capitalize">
              {connectionStatus}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

