import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, Clock, XCircle, Circle } from 'lucide-react';

const getStatusIcon = (status) => {
  switch (status) {
    case 'done':
      return <CheckCircle className="w-5 h-5 text-green-500" />;
    case 'in_progress':
      return <Clock className="w-5 h-5 text-blue-500 animate-pulse" />;
    case 'failed':
      return <XCircle className="w-5 h-5 text-red-500" />;
    default:
      return <Circle className="w-5 h-5 text-gray-300" />;
  }
};

const getStatusColor = (status) => {
  switch (status) {
    case 'done':
      return 'bg-green-50 border-green-200';
    case 'in_progress':
      return 'bg-blue-50 border-blue-200';
    case 'failed':
      return 'bg-red-50 border-red-200';
    default:
      return 'bg-gray-50 border-gray-200';
  }
};

export default function Checklist({ steps }) {
  if (!steps || steps.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="bg-white rounded-2xl p-6 shadow-md border border-purple-100 max-w-md mx-auto"
    >
      <h3 className="text-lg font-bold text-gray-900 mb-4 text-right">
        خطوات المعالجة
      </h3>
      <div className="space-y-3">
        {steps.map((step, index) => (
          <motion.div
            key={step.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`flex items-center gap-3 p-3 rounded-lg border ${getStatusColor(step.status)}`}
          >
            {getStatusIcon(step.status)}
            <div className="flex-1 text-right">
              <p className="font-medium text-gray-900">{step.title}</p>
              {step.meta && Object.keys(step.meta).length > 0 && (
                <p className="text-xs text-gray-600 mt-1">
                  {JSON.stringify(step.meta, null, 2)}
                </p>
              )}
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
