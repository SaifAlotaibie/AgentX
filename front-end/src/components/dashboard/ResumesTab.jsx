import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { FileText, Mail, Phone, Briefcase, GraduationCap, BriefcaseIcon } from 'lucide-react';

export default function ResumesTab({ resumes, loading, error, onRefresh, formatDate }) {
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-600 border-t-transparent"></div>
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

  if (resumes.length === 0) {
    return (
      <div className="bg-white rounded-xl p-12 text-center shadow-md">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h2 className="text-2xl font-semibold text-gray-700 mb-2">لا توجد سير ذاتية</h2>
        <p className="text-gray-500 mb-6">ابدأ بإنشاء سيرتك الذاتية من خلال المحادثة</p>
        <Link
          to="/chat"
          className="inline-block px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition"
        >
          ابدأ الآن
        </Link>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {resumes.map((resume, index) => (
        <motion.div
          key={resume.resumeId}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          whileHover={{ scale: 1.02 }}
          className="bg-white rounded-xl p-6 shadow-md border border-gray-200 hover:border-purple-300 transition"
        >
          {/* Resume Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="text-right flex-1">
              <h3 className="text-xl font-bold text-gray-900">{resume.data?.full_name || 'بدون اسم'}</h3>
              <div className="flex items-center justify-end text-sm text-gray-500 mt-1">
                <span>{resume.data?.job_title || 'المسمى الوظيفي'}</span>
                <Briefcase className="w-4 h-4 mr-2" />
              </div>
            </div>
            <div className="bg-purple-100 text-purple-600 px-3 py-1 rounded-full text-xs font-semibold">
              {resume.resumeId}
            </div>
          </div>

          {/* Contact Info */}
          {resume.data?.contact && (
            <div className="space-y-2 mb-4 text-sm">
              {resume.data.contact.email && (
                <div className="flex items-center justify-end text-gray-600">
                  <span className="font-arabic">{resume.data.contact.email}</span>
                  <Mail className="w-4 h-4 mr-2 text-purple-600" />
                </div>
              )}
              {resume.data.contact.phone && (
                <div className="flex items-center justify-end text-gray-600">
                  <span className="font-arabic">{resume.data.contact.phone}</span>
                  <Phone className="w-4 h-4 mr-2 text-purple-600" />
                </div>
              )}
            </div>
          )}

          {/* Education & Experience Summary */}
          <div className="space-y-2 mb-4">
            {resume.data?.education && Array.isArray(resume.data.education) && resume.data.education.length > 0 && (
              <div className="flex items-center justify-end text-sm text-gray-600">
                <span>{resume.data.education.length} شهادة تعليمية</span>
                <GraduationCap className="w-4 h-4 mr-2 text-blue-600" />
              </div>
            )}
            {resume.data?.experience && Array.isArray(resume.data.experience) && resume.data.experience.length > 0 && (
              <div className="flex items-center justify-end text-sm text-gray-600">
                <span>{resume.data.experience.length} خبرة عملية</span>
                <BriefcaseIcon className="w-4 h-4 mr-2 text-green-600" />
              </div>
            )}
          </div>

          {/* Metadata */}
          <div className="pt-4 border-t border-gray-100">
            <div className="flex justify-between text-xs text-gray-500">
              <span>{formatDate(resume.updatedAt)}</span>
              <span>آخر تحديث</span>
            </div>
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>{formatDate(resume.createdAt)}</span>
              <span>تاريخ الإنشاء</span>
            </div>
          </div>

          {/* Actions */}
          <div className="mt-4 pt-4 border-t border-gray-100 flex gap-2">
            <button className="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition text-sm">
              عرض التفاصيل
            </button>
            <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition text-sm">
              تحميل
            </button>
          </div>
        </motion.div>
      ))}
    </div>
  );
}

