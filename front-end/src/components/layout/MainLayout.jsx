import Header from './Header';
import Sidebar from './Sidebar';
import ChatArea from '../chat/ChatArea';
import InputBar from '../chat/InputBar';
import { useWebSocket } from '../../hooks/useWebSocket';

const MainLayout = () => {
  const { sendMessage } = useWebSocket();
  
  const handleSendMessage = (message) => {
    sendMessage(message);
  };
  
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-50 to-slate-100">
      <Header />
      
      <div className="flex-1 container mx-auto p-4 flex gap-4 overflow-hidden">
        {/* Main chat area - 65% width */}
        <div className="flex-1 flex flex-col bg-white rounded-2xl shadow-xl overflow-hidden" style={{ maxWidth: '65%' }}>
          <ChatArea />
          <InputBar onSendMessage={handleSendMessage} />
        </div>
        
        {/* Sidebar - 35% width */}
        <div className="w-full" style={{ maxWidth: '35%' }}>
          <Sidebar />
        </div>
      </div>
    </div>
  );
};

export default MainLayout;

