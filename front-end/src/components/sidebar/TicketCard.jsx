import { formatTimestamp } from '../../lib/utils';
import { FileText, Clock, Check } from 'lucide-react';

const TicketCard = ({ ticket }) => {
  const getTypeColor = (type) => {
    if (type?.includes('add')) return 'bg-green-100 text-green-700';
    if (type?.includes('edit')) return 'bg-blue-100 text-blue-700';
    if (type?.includes('delete')) return 'bg-red-100 text-red-700';
    return 'bg-gray-100 text-gray-700';
  };
  
  const getTypeLabel = (type) => {
    if (type?.includes('add')) return 'Add';
    if (type?.includes('edit')) return 'Edit';
    if (type?.includes('delete')) return 'Delete';
    return type || 'Unknown';
  };
  
  const isOpen = ticket.status === 'open';
  
  return (
    <div className="p-4 bg-white rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-gray-500" />
          <span className="text-sm font-mono text-gray-700">{ticket.ticketId}</span>
        </div>
        
        <span className={`px-2 py-0.5 text-xs rounded-full ${
          isOpen 
            ? 'bg-amber-100 text-amber-700' 
            : 'bg-green-100 text-green-700'
        }`}>
          {isOpen ? <Clock className="w-3 h-3 inline mr-1" /> : <Check className="w-3 h-3 inline mr-1" />}
          {ticket.status}
        </span>
      </div>
      
      <div className="space-y-1">
        <div className={`inline-block px-2 py-1 rounded text-xs font-medium ${getTypeColor(ticket.type)}`}>
          {getTypeLabel(ticket.type)}
        </div>
        
        {ticket.createdAt && (
          <p className="text-xs text-gray-500 mt-2">
            Created: {formatTimestamp(ticket.createdAt)}
          </p>
        )}
        
        {ticket.closedAt && (
          <p className="text-xs text-gray-500">
            Closed: {formatTimestamp(ticket.closedAt)}
          </p>
        )}
      </div>
    </div>
  );
};

export default TicketCard;

