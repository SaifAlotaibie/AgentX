import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Navigation from './components/layout/Navigation';
import HRSDHomePage from './pages/HRSDHomePage';
import QiwaMainPage from './pages/QiwaMainPage';
import ChatPage from './pages/ChatPage';
import DashboardPage from './pages/DashboardPage';
import TicketsPage from './pages/TicketsPage';
import { useWebSocket } from './hooks/useWebSocket';
import { MOCK_USER } from './config/mockUser';

// Component to conditionally show navigation
function AppLayout() {
  const location = useLocation();
  const { connectionStatus } = useWebSocket();
  
  // Show navigation only on chat, dashboard, and tickets pages
  const showNavigation = ['/chat', '/dashboard', '/tickets'].includes(location.pathname);
  
  return (
    <div className="min-h-screen bg-gray-50" dir="rtl">
      {/* Dev Mode Banner */}
      <div className="fixed top-0 left-0 right-0 bg-yellow-400 text-black text-center py-1 text-xs font-semibold z-[9999] shadow-md">
        🔧 وضع التطوير: مسجل دخول كـ {MOCK_USER.name} ({MOCK_USER.id.slice(0, 8)}...)
      </div>

      {/* Navigation - only on specific pages */}
      {showNavigation && <Navigation />}

      {/* Main Content with padding for dev banner */}
      <main className={showNavigation ? "pt-[4.5rem] h-screen" : "pt-7 h-screen"}>
        <AnimatePresence mode="wait">
          <Routes>
            <Route path="/" element={<HRSDHomePage />} />
            <Route path="/qiwa" element={<QiwaMainPage />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/tickets" element={<TicketsPage />} />
          </Routes>
        </AnimatePresence>
      </main>

      {/* Connection Status Indicator - only on pages with navigation */}
      {showNavigation && connectionStatus !== 'connected' && (
        <div className="fixed bottom-4 left-4 z-50">
          <div className={`px-4 py-2 rounded-lg shadow-lg text-sm font-medium ${
            connectionStatus === 'connecting'
              ? 'bg-yellow-500 text-white'
              : 'bg-red-500 text-white'
          }`}>
            {connectionStatus === 'connecting' ? 'جاري الاتصال...' : 'غير متصل'}
          </div>
        </div>
      )}
    </div>
  );
}

function App() {
  // Set mock user in sessionStorage for testing
  useEffect(() => {
    if (!sessionStorage.getItem('userId')) {
      sessionStorage.setItem('userId', MOCK_USER.id);
    }
    if (!sessionStorage.getItem('sessionId')) {
      sessionStorage.setItem('sessionId', `S${Date.now()}`);
    }
  }, []);

  return (
    <Router>
      <AppLayout />
    </Router>
  );
}

export default App;
