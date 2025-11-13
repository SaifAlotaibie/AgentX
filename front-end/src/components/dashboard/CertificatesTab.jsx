import React from 'react';
import { motion } from 'framer-motion';
import { FileText, Clock, CheckCircle, Loader, XCircle } from 'lucide-react';

export default function CertificatesTab({ certificates, loading, error, onRefresh, formatDate }) {
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-green-600 border-t-transparent"></div>
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

  if (certificates.length === 0) {
    return (
      <div className="bg-white rounded-xl p-12 text-center shadow-md">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h2 className="text-2xl font-semibold text-gray-700 mb-2">لا توجد شهادات</h2>
        <p className="text-gray-500 mb-6">يمكنك طلب شهادة راتب أو خطاب خبرة من خلال المحادثة</p>
      </div>
    );
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'ready': return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'processing': return <Loader className="w-5 h-5 text-yellow-600 animate-spin" />;
      case 'requested': return <Clock className="w-5 h-5 text-blue-600" />;
      default: return <FileText className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'ready': return 'bg-green-100 text-green-700';
      case 'processing': return 'bg-yellow-100 text-yellow-700';
      case 'requested': return 'bg-blue-100 text-blue-700';
      case 'delivered': return 'bg-gray-100 text-gray-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'ready': return 'جاهز';
      case 'processing': return 'قيد المعالجة';
      case 'requested': return 'تم الطلب';
      case 'delivered': return 'تم التسليم';
      default: return status;
    }
  };

  const getTypeText = (type) => {
    return type === 'salary' ? 'شهادة راتب' : 'خطاب خبرة';
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {certificates.map((cert, index) => (
        <motion.div
          key={cert.certificateId}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          whileHover={{ scale: 1.02 }}
          className="bg-white rounded-xl p-6 shadow-md border border-gray-200 hover:border-green-300 transition"
        >
          {/* Certificate Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="text-right flex-1">
              <h3 className="text-lg font-bold text-gray-900">{getTypeText(cert.data?.type)}</h3>
              <p className="text-sm text-gray-500 mt-1">
                الغرض: {cert.data?.purpose || 'غير محدد'}
              </p>
            </div>
            {getStatusIcon(cert.data?.status)}
          </div>

          {/* Status Badge */}
          <div className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(cert.data?.status)} mb-4`}>
            {getStatusText(cert.data?.status)}
          </div>

          {/* Certificate Details */}
          <div className="space-y-2 mb-4 text-sm">
            <div className="flex justify-between text-gray-600">
              <span>{formatDate(cert.data?.request_date || cert.createdAt)}</span>
              <span>تاريخ الطلب</span>
            </div>
            {cert.data?.ready_date && (
              <div className="flex justify-between text-green-600 font-semibold">
                <span>{formatDate(cert.data.ready_date)}</span>
                <span>تاريخ الجاهزية</span>
              </div>
            )}
          </div>

          {/* Certificate ID */}
          <div className="pt-4 border-t border-gray-100 mb-4">
            <div className="flex justify-between text-xs text-gray-500">
              <span className="font-mono">{cert.certificateId}</span>
              <span>رقم الشهادة</span>
            </div>
          </div>

          {/* Actions */}
          {cert.data?.status === 'ready' && (
            <button className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition text-sm">
              تحميل الشهادة
            </button>
          )}
          {cert.data?.status === 'processing' && (
            <button disabled className="w-full px-4 py-2 bg-gray-300 text-gray-500 rounded-lg cursor-not-allowed text-sm">
              جاري المعالجة...
            </button>
          )}
          {cert.data?.status === 'requested' && (
            <button disabled className="w-full px-4 py-2 bg-gray-300 text-gray-500 rounded-lg cursor-not-allowed text-sm">
              في قائمة الانتظار
            </button>
          )}
        </motion.div>
      ))}
    </div>
  );
}

