import { useState } from 'react';
import { motion } from 'framer-motion';
import { Ticket, BarChart3 } from 'lucide-react';
import TicketsTab from '../sidebar/TicketsTab';
import DashboardTab from '../sidebar/DashboardTab';
import { useChatStore } from '../../store/chatStore';

const Sidebar = () => {
  const [activeTab, setActiveTab] = useState('tickets');
  const { tickets } = useChatStore();
  
  const tabs = [
    { 
      id: 'tickets', 
      label: 'Tickets', 
      icon: Ticket,
      badge: tickets.filter(t => t.status === 'open').length
    },
    { 
      id: 'dashboard', 
      label: 'Dashboard', 
      icon: BarChart3
    },
  ];
  
  return (
    <div className="bg-white rounded-2xl shadow-xl h-full flex flex-col overflow-hidden">
      {/* Tabs header */}
      <div className="flex border-b border-gray-200">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 text-sm font-medium transition-colors relative ${
              activeTab === tab.id
                ? 'text-qiwa-primary'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            <span>{tab.label}</span>
            
            {tab.badge > 0 && (
              <span className="ml-1 px-1.5 py-0.5 text-xs bg-red-500 text-white rounded-full">
                {tab.badge}
              </span>
            )}
            
            {/* Active indicator */}
            {activeTab === tab.id && (
              <motion.div
                layoutId="activeTab"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-qiwa-primary"
              />
            )}
          </button>
        ))}
      </div>
      
      {/* Tab content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'tickets' && <TicketsTab />}
        {activeTab === 'dashboard' && <DashboardTab />}
      </div>
    </div>
  );
};

export default Sidebar;

