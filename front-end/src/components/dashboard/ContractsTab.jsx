import React from 'react';
import { motion } from 'framer-motion';
import { FileText, Building2, Briefcase, DollarSign, Calendar, CheckCircle, XCircle } from 'lucide-react';

export default function ContractsTab({ contracts, loading, error, onRefresh, formatDate }) {
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
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

  if (contracts.length === 0) {
    return (
      <div className="bg-white rounded-xl p-12 text-center shadow-md">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h2 className="text-2xl font-semibold text-gray-700 mb-2">لا توجد عقود</h2>
        <p className="text-gray-500 mb-6">يمكنك طلب عرض عقدك من خلال المحادثة مع المساعد</p>
      </div>
    );
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-700';
      case 'pending': return 'bg-yellow-100 text-yellow-700';
      case 'terminated': return 'bg-red-100 text-red-700';
      case 'expired': return 'bg-gray-100 text-gray-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active': return 'نشط';
      case 'pending': return 'قيد الانتظار';
      case 'terminated': return 'منتهي';
      case 'expired': return 'منتهي الصلاحية';
      default: return status;
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {contracts.map((contract, index) => (
        <motion.div
          key={contract.contractId}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          whileHover={{ scale: 1.02 }}
          className="bg-white rounded-xl p-6 shadow-md border border-gray-200 hover:border-blue-300 transition"
        >
          {/* Contract Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="text-right flex-1">
              <h3 className="text-xl font-bold text-gray-900">
                {contract.data?.employer_name || 'اسم الشركة'}
              </h3>
              <div className="flex items-center justify-end text-sm text-gray-500 mt-1">
                <span>{contract.data?.job_title || 'المسمى الوظيفي'}</span>
                <Briefcase className="w-4 h-4 mr-2" />
              </div>
            </div>
            <div className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(contract.data?.status)}`}>
              {getStatusText(contract.data?.status)}
            </div>
          </div>

          {/* Contract Details */}
          <div className="space-y-3 mb-4">
            {contract.data?.salary && (
              <div className="flex items-center justify-between text-sm">
                <span className="font-semibold text-blue-600">{contract.data.salary.toLocaleString()} ريال</span>
                <div className="flex items-center text-gray-600">
                  <span>الراتب الشهري</span>
                  <DollarSign className="w-4 h-4 mr-2" />
                </div>
              </div>
            )}
            
            {contract.data?.start_date && (
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-700">{formatDate(contract.data.start_date)}</span>
                <div className="flex items-center text-gray-600">
                  <span>تاريخ البداية</span>
                  <Calendar className="w-4 h-4 mr-2" />
                </div>
              </div>
            )}
            
            {contract.data?.end_date && (
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-700">{formatDate(contract.data.end_date)}</span>
                <div className="flex items-center text-gray-600">
                  <span>تاريخ الانتهاء</span>
                  <Calendar className="w-4 h-4 mr-2" />
                </div>
              </div>
            )}
          </div>

          {/* Contract ID */}
          <div className="pt-4 border-t border-gray-100">
            <div className="flex justify-between text-xs text-gray-500">
              <span className="font-mono">{contract.contractId}</span>
              <span>رقم العقد</span>
            </div>
          </div>

          {/* Actions */}
          <div className="mt-4 pt-4 border-t border-gray-100 flex gap-2">
            <button className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm">
              عرض التفاصيل
            </button>
            <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition text-sm">
              طلب تجديد
            </button>
          </div>
        </motion.div>
      ))}
    </div>
  );
}

