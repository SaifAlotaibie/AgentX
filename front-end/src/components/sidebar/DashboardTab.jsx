import { useChatStore } from '../../store/chatStore';
import { MessageCircle, Ticket, CheckCircle, Clock } from 'lucide-react';
import { motion } from 'framer-motion';

const StatCard = ({ icon: Icon, label, value, color }) => (
  <motion.div
    initial={{ opacity: 0, scale: 0.95 }}
    animate={{ opacity: 1, scale: 1 }}
    className={`p-4 rounded-lg ${color} border border-gray-200`}
  >
    <div className="flex items-center gap-3">
      <div className="flex-shrink-0">
        <Icon className="w-5 h-5 text-gray-600" />
      </div>
      <div>
        <p className="text-2xl font-bold text-gray-800">{value}</p>
        <p className="text-xs text-gray-600">{label}</p>
      </div>
    </div>
  </motion.div>
);

const DashboardTab = () => {
  const stats = useChatStore(state => state.getStats());
  const { sessionId, connectionStatus } = useChatStore();
  
  return (
    <div className="p-4 space-y-4 overflow-y-auto h-full">
      {/* Connection status */}
      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">Status</span>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${
              connectionStatus === 'connected' 
                ? 'bg-green-500' 
                : connectionStatus === 'connecting'
                ? 'bg-amber-500 animate-pulse'
                : 'bg-red-500'
            }`}></div>
            <span className="text-sm font-medium text-gray-700 capitalize">
              {connectionStatus}
            </span>
          </div>
        </div>
      </div>
      
      {/* Stats grid */}
      <div className="grid grid-cols-2 gap-3">
        <StatCard
          icon={MessageCircle}
          label="Total Messages"
          value={stats.totalMessages}
          color="bg-blue-50"
        />
        <StatCard
          icon={Ticket}
          label="Total Tickets"
          value={stats.totalTickets}
          color="bg-purple-50"
        />
        <StatCard
          icon={Clock}
          label="Open Tickets"
          value={stats.openTickets}
          color="bg-amber-50"
        />
        <StatCard
          icon={CheckCircle}
          label="Closed Tickets"
          value={stats.closedTickets}
          color="bg-green-50"
        />
      </div>
      
      {/* Session info */}
      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h3 className="text-sm font-semibold text-gray-700 mb-2">Session Info</h3>
        <div className="space-y-1">
          <div className="flex justify-between text-xs">
            <span className="text-gray-500">Session ID:</span>
            <span className="text-gray-700 font-mono">{sessionId.slice(0, 12)}...</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-gray-500">User Messages:</span>
            <span className="text-gray-700">{stats.userMessages}</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-gray-500">Agent Messages:</span>
            <span className="text-gray-700">{stats.assistantMessages}</span>
          </div>
        </div>
      </div>
      
      {/* Activity indicator */}
      <div className="bg-gradient-to-br from-qiwa-primary to-qiwa-secondary rounded-lg p-4 text-white">
        <h3 className="text-sm font-semibold mb-2">🎯 Quick Stats</h3>
        <p className="text-xs opacity-90">
          You've exchanged {stats.totalMessages} messages and created {stats.totalTickets} tickets in this session.
        </p>
      </div>
    </div>
  );
};

export default DashboardTab;

