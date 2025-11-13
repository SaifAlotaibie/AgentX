import React from 'react';
import { motion } from 'framer-motion';
import { Bell, Clock, AlertCircle, CheckCircle, XCircle } from 'lucide-react';

export default function RemindersTab({ reminders, loading, error, onRefresh, formatDate }) {
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-indigo-600 border-t-transparent"></div>
        <p className="text-gray-600 mt-4">جاري التحميل...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
        <p className="text-red-600">{error}</p>
        <button
          onClick={onRefresh}
          className="mt-4 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
        >
          إعادة المحاولة
        </button>
      </div>
    );
  }

  if (reminders.length === 0) {
    return (
      <div className="bg-white rounded-xl p-12 text-center shadow-md">
        <Bell className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h2 className="text-2xl font-semibold text-gray-700 mb-2">لا توجد تذكيرات</h2>
        <p className="text-gray-500">سيتم إشعارك هنا عند وجود أي تذكيرات مهمة</p>
      </div>
    );
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'contract_expiry': return <AlertCircle className="w-5 h-5 text-orange-600" />;
      case 'permit_expiry': return <Clock className="w-5 h-5 text-red-600" />;
      case 'certificate_ready': return <CheckCircle className="w-5 h-5 text-green-600" />;
      default: return <Bell className="w-5 h-5 text-indigo-600" />;
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'contract_expiry': return 'border-orange-300 bg-orange-50';
      case 'permit_expiry': return 'border-red-300 bg-red-50';
      case 'certificate_ready': return 'border-green-300 bg-green-50';
      default: return 'border-indigo-300 bg-indigo-50';
    }
  };

  const getTypeText = (type) => {
    switch (type) {
      case 'contract_expiry': return 'انتهاء عقد';
      case 'permit_expiry': return 'انتهاء تصريح';
      case 'certificate_ready': return 'شهادة جاهزة';
      case 'custom': return 'تذكير';
      default: return type;
    }
  };

  return (
    <div className="space-y-4">
      {reminders.map((reminder, index) => (
        <motion.div
          key={reminder.reminderId}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          whileHover={{ scale: 1.01 }}
          className={`bg-white rounded-xl p-6 shadow-md border-2 ${getTypeColor(reminder.data?.reminder_type)} transition`}
        >
          <div className="flex items-start gap-4">
            {/* Icon */}
            <div className="flex-shrink-0 mt-1">
              {getTypeIcon(reminder.data?.reminder_type)}
            </div>

            {/* Content */}
            <div className="flex-1 text-right">
              {/* Type Badge */}
              <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-white text-gray-700 mb-2">
                {getTypeText(reminder.data?.reminder_type)}
              </span>

              {/* Message */}
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                {reminder.data?.message || 'تذكير'}
              </h3>

              {/* Details */}
              <div className="space-y-1 text-sm text-gray-600">
                {reminder.data?.trigger_date && (
                  <div className="flex items-center justify-end gap-2">
                    <span>{formatDate(reminder.data.trigger_date)}</span>
                    <Clock className="w-4 h-4" />
                  </div>
                )}
                {reminder.data?.related_entity_id && (
                  <div className="text-xs text-gray-500">
                    المرجع: {reminder.data.related_entity_id}
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="flex gap-2 mt-4">
                <button className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition text-sm">
                  اتخاذ إجراء
                </button>
                <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition text-sm">
                  تجاهل
                </button>
              </div>
            </div>
          </div>

          {/* Reminder ID (bottom) */}
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="flex justify-between text-xs text-gray-500">
              <span className="font-mono">{reminder.reminderId}</span>
              <span>رقم التذكير</span>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}

