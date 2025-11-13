import { motion } from 'framer-motion';
import TicketCard from './TicketCard';
import { useChatStore } from '../../store/chatStore';
import { Inbox } from 'lucide-react';

const TicketsTab = () => {
  const { tickets } = useChatStore();
  
  if (tickets.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center px-4 py-12">
        <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
          <Inbox className="w-8 h-8 text-gray-400" />
        </div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">No Tickets Yet</h3>
        <p className="text-sm text-gray-500">
          Tickets will appear here when you start using resume management features.
        </p>
      </div>
    );
  }
  
  return (
    <div className="space-y-3 p-4 overflow-y-auto h-full">
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-1">
          Active Tickets
        </h3>
        <p className="text-xs text-gray-500">
          {tickets.filter(t => t.status === 'open').length} open, {tickets.filter(t => t.status === 'closed').length} closed
        </p>
      </div>
      
      {tickets.map((ticket, index) => (
        <motion.div
          key={ticket.ticketId}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
        >
          <TicketCard ticket={ticket} />
        </motion.div>
      ))}
    </div>
  );
};

export default TicketsTab;

