import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Ticket, Clock, CheckCircle, XCircle, ArrowRight, AlertCircle } from 'lucide-react';
import { MOCK_USER } from '../config/mockUser';

const API_URL = 'http://localhost:8000';

export default function TicketsPage() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Get userId from session
  const userId = sessionStorage.getItem('userId') || MOCK_USER.id;

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/tickets/${userId}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setTickets(data.tickets || []);
      } else {
        setError('فشل في تحميل التذاكر');
      }
    } catch (err) {
      setError('خطأ في الاتصال بالخادم');
      console.error('Error fetching tickets:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'غير محدد';
    const date = new Date(dateString);
    return date.toLocaleDateString('ar-SA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'open':
        return <Clock className="w-5 h-5 text-blue-600" />;
      case 'closed':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'cancelled':
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'open':
        return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'closed':
        return 'bg-green-100 text-green-700 border-green-200';
      case 'cancelled':
        return 'bg-red-100 text-red-700 border-red-200';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'open':
        return 'مفتوحة';
      case 'closed':
        return 'مغلقة';
      case 'cancelled':
        return 'ملغاة';
      default:
        return status;
    }
  };

  const getTypeText = (type) => {
    switch (type) {
      case 'resume_add':
        return 'إضافة سيرة ذاتية';
      case 'resume_edit':
        return 'تعديل سيرة ذاتية';
      case 'resume_delete':
        return 'حذف سيرة ذاتية';
      case 'qa':
        return 'استفسار';
      default:
        return type;
    }
  };

  const openTickets = tickets.filter(t => t.status === 'open');
  const closedTickets = tickets.filter(t => t.status === 'closed');

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 p-6"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Link to="/" className="inline-flex items-center text-purple-600 hover:text-purple-700 mb-4">
            <ArrowRight className="w-5 h-5 ml-2" />
            العودة للمحادثة
          </Link>
          <h1 className="text-4xl font-bold text-gray-900 text-right">التذاكر</h1>
          <p className="text-gray-600 text-right mt-2">جميع التذاكر والطلبات</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-white rounded-xl p-6 shadow-md border border-gray-200"
          >
            <div className="flex items-center justify-between">
              <div className="text-right">
                <p className="text-gray-600 text-sm">إجمالي التذاكر</p>
                <p className="text-3xl font-bold text-gray-900">{tickets.length}</p>
              </div>
              <Ticket className="w-12 h-12 text-gray-900 opacity-20" />
            </div>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-white rounded-xl p-6 shadow-md border border-blue-200"
          >
            <div className="flex items-center justify-between">
              <div className="text-right">
                <p className="text-gray-600 text-sm">التذاكر المفتوحة</p>
                <p className="text-3xl font-bold text-blue-600">{openTickets.length}</p>
              </div>
              <Clock className="w-12 h-12 text-blue-600 opacity-20" />
            </div>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-white rounded-xl p-6 shadow-md border border-green-200"
          >
            <div className="flex items-center justify-between">
              <div className="text-right">
                <p className="text-gray-600 text-sm">التذاكر المغلقة</p>
                <p className="text-3xl font-bold text-green-600">{closedTickets.length}</p>
              </div>
              <CheckCircle className="w-12 h-12 text-green-600 opacity-20" />
            </div>
          </motion.div>
        </div>

        {/* Tickets List */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-600 border-t-transparent"></div>
            <p className="text-gray-600 mt-4">جاري التحميل...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
            <p className="text-red-600">{error}</p>
            <button
              onClick={fetchTickets}
              className="mt-4 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
            >
              إعادة المحاولة
            </button>
          </div>
        ) : tickets.length === 0 ? (
          <div className="bg-white rounded-xl p-12 text-center shadow-md">
            <Ticket className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h2 className="text-2xl font-semibold text-gray-700 mb-2">لا توجد تذاكر</h2>
            <p className="text-gray-500 mb-6">لم تقم بإنشاء أي تذاكر بعد</p>
            <Link
              to="/"
              className="inline-block px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition"
            >
              ابدأ محادثة جديدة
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {tickets.map((ticket, index) => (
              <motion.div
                key={ticket.ticketId}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl p-6 shadow-md border border-gray-200 hover:border-purple-300 transition"
              >
                <div className="flex items-start justify-between">
                  {/* Ticket Info */}
                  <div className="flex-1 text-right">
                    <div className="flex items-center justify-end gap-3 mb-2">
                      <h3 className="text-lg font-bold text-gray-900">{getTypeText(ticket.type)}</h3>
                      {getStatusIcon(ticket.status)}
                    </div>
                    
                    <p className="text-gray-600 text-sm mb-3">{ticket.description}</p>
                    
                    <div className="flex items-center justify-end gap-4 text-xs text-gray-500">
                      <span>{formatDate(ticket.createdAt)}</span>
                      <span>•</span>
                      <span className="font-mono">{ticket.ticketId}</span>
                    </div>
                    
                    {ticket.closedAt && (
                      <div className="flex items-center justify-end gap-2 text-xs text-green-600 mt-2">
                        <span>{formatDate(ticket.closedAt)}</span>
                        <CheckCircle className="w-4 h-4" />
                      </div>
                    )}
                  </div>

                  {/* Status Badge */}
                  <div className={`px-4 py-2 rounded-full text-sm font-semibold border ${getStatusColor(ticket.status)}`}>
                    {getStatusText(ticket.status)}
                  </div>
                </div>

                {/* Actions for open tickets */}
                {ticket.status === 'open' && (
                  <div className="mt-4 pt-4 border-t border-gray-100 flex gap-2 justify-end">
                    <Link
                      to="/"
                      className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition text-sm"
                    >
                      متابعة في المحادثة
                    </Link>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}

