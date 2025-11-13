import React from 'react';
import { motion } from 'framer-motion';
import { FileText, User, Briefcase, Calendar, AlertTriangle, CheckCircle } from 'lucide-react';

export default function WorkPermitsTab({ permits, loading, error, onRefresh, formatDate }) {
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-orange-600 border-t-transparent"></div>
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

  if (permits.length === 0) {
    return (
      <div className="bg-white rounded-xl p-12 text-center shadow-md">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h2 className="text-2xl font-semibold text-gray-700 mb-2">لا توجد تصاريح عمل</h2>
        <p className="text-gray-500 mb-6">يمكنك عرض وإدارة تصاريح العمل من خلال المحادثة</p>
      </div>
    );
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-700';
      case 'expiring_soon': return 'bg-orange-100 text-orange-700';
      case 'expired': return 'bg-red-100 text-red-700';
      case 'renewal_pending': return 'bg-yellow-100 text-yellow-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active': return 'نشط';
      case 'expiring_soon': return 'ينتهي قريباً';
      case 'expired': return 'منتهي';
      case 'renewal_pending': return 'التجديد قيد الانتظار';
      default: return status;
    }
  };

  const getStatusIcon = (status) => {
    if (status === 'active') return <CheckCircle className="w-5 h-5 text-green-600" />;
    if (status === 'expiring_soon' || status === 'expired') return <AlertTriangle className="w-5 h-5 text-orange-600" />;
    return <FileText className="w-5 h-5 text-gray-600" />;
  };

  return (
    <div className="space-y-4">
      {/* Expiring Soon Alert */}
      {permits.some(p => p.data?.status === 'expiring_soon' || p.data?.status === 'expired') && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-orange-50 border-r-4 border-orange-500 p-4 rounded-lg"
        >
          <div className="flex items-center justify-end">
            <div className="text-right">
              <h4 className="font-semibold text-orange-800">تنبيه: تصاريح تحتاج تجديد</h4>
              <p className="text-sm text-orange-700">
                لديك {permits.filter(p => p.data?.status === 'expiring_soon' || p.data?.status === 'expired').length} تصريح يحتاج تجديد
              </p>
            </div>
            <AlertTriangle className="w-6 h-6 text-orange-600 mr-3" />
          </div>
        </motion.div>
      )}

      {/* Permits Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {permits.map((permit, index) => (
          <motion.div
            key={permit.permitId}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.02 }}
            className={`bg-white rounded-xl p-6 shadow-md border-2 transition ${
              permit.data?.status === 'expiring_soon' || permit.data?.status === 'expired'
                ? 'border-orange-300'
                : 'border-gray-200 hover:border-orange-300'
            }`}
          >
            {/* Permit Header */}
            <div className="flex items-start justify-between mb-4">
              <div className="text-right flex-1">
                <h3 className="text-lg font-bold text-gray-900">
                  {permit.data?.employee_name || 'اسم الموظف'}
                </h3>
                <div className="flex items-center justify-end text-sm text-gray-500 mt-1">
                  <span>{permit.data?.job_title || 'المسمى الوظيفي'}</span>
                  <Briefcase className="w-4 h-4 mr-2" />
                </div>
              </div>
              {getStatusIcon(permit.data?.status)}
            </div>

            {/* Status Badge */}
            <div className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(permit.data?.status)} mb-4`}>
              {getStatusText(permit.data?.status)}
            </div>

            {/* Permit Details */}
            <div className="space-y-3 mb-4">
              {permit.data?.nationality && (
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-700">{permit.data.nationality}</span>
                  <div className="flex items-center text-gray-600">
                    <span>الجنسية</span>
                    <User className="w-4 h-4 mr-2" />
                  </div>
                </div>
              )}
              
              {permit.data?.expiry_date && (
                <div className="flex items-center justify-between text-sm">
                  <span className={`font-semibold ${
                    permit.data.status === 'expiring_soon' || permit.data.status === 'expired'
                      ? 'text-orange-600'
                      : 'text-gray-700'
                  }`}>
                    {formatDate(permit.data.expiry_date)}
                  </span>
                  <div className="flex items-center text-gray-600">
                    <span>تاريخ الانتهاء</span>
                    <Calendar className="w-4 h-4 mr-2" />
                  </div>
                </div>
              )}
            </div>

            {/* Permit ID */}
            <div className="pt-4 border-t border-gray-100 mb-4">
              <div className="flex justify-between text-xs text-gray-500">
                <span className="font-mono">{permit.permitId}</span>
                <span>رقم التصريح</span>
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-2">
              {(permit.data?.status === 'expiring_soon' || permit.data?.status === 'expired') && (
                <button className="flex-1 px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition text-sm">
                  تجديد الآن
                </button>
              )}
              <button className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition text-sm">
                التفاصيل
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

