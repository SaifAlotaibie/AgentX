import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { FileText, Calendar, User, ArrowRight, FileCheck, BriefcaseIcon, Shield, Bell } from 'lucide-react';
import { MOCK_USER } from '../config/mockUser';

// Import tab components
import ResumesTab from '../components/dashboard/ResumesTab';
import ContractsTab from '../components/dashboard/ContractsTab';
import CertificatesTab from '../components/dashboard/CertificatesTab';
import WorkPermitsTab from '../components/dashboard/WorkPermitsTab';
import RemindersTab from '../components/dashboard/RemindersTab';

const API_URL = 'http://localhost:8000';

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState('resumes');
  const [resumes, setResumes] = useState([]);
  const [contracts, setContracts] = useState([]);
  const [certificates, setCertificates] = useState([]);
  const [permits, setPermits] = useState([]);
  const [reminders, setReminders] = useState([]);
  
  const [loading, setLoading] = useState({
    resumes: true,
    contracts: true,
    certificates: true,
    permits: true,
    reminders: true
  });
  
  const [error, setError] = useState({
    resumes: null,
    contracts: null,
    certificates: null,
    permits: null,
    reminders: null
  });
  
  // Get user info from session
  const userId = sessionStorage.getItem('userId') || MOCK_USER.id;
  const userType = MOCK_USER.user_type || 'employee';
  const establishmentId = MOCK_USER.establishment_id;

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = () => {
    fetchResumes();
    fetchContracts();
    fetchCertificates();
    if (userType === 'business_owner') {
      fetchPermits();
    }
    fetchReminders();
  };

  const fetchResumes = async () => {
    try {
      setLoading(prev => ({ ...prev, resumes: true }));
      const response = await fetch(`${API_URL}/resumes/${userId}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setResumes(data.resumes || []);
        setError(prev => ({ ...prev, resumes: null }));
      } else {
        setError(prev => ({ ...prev, resumes: 'فشل في تحميل السير الذاتية' }));
      }
    } catch (err) {
      setError(prev => ({ ...prev, resumes: 'خطأ في الاتصال بالخادم' }));
      console.error('Error fetching resumes:', err);
    } finally {
      setLoading(prev => ({ ...prev, resumes: false }));
    }
  };

  const fetchContracts = async () => {
    try {
      setLoading(prev => ({ ...prev, contracts: true }));
      const response = await fetch(`${API_URL}/contracts/${userId}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setContracts(data.contracts || []);
        setError(prev => ({ ...prev, contracts: null }));
      } else {
        setError(prev => ({ ...prev, contracts: 'فشل في تحميل العقود' }));
      }
    } catch (err) {
      setError(prev => ({ ...prev, contracts: 'خطأ في الاتصال بالخادم' }));
      console.error('Error fetching contracts:', err);
    } finally {
      setLoading(prev => ({ ...prev, contracts: false }));
    }
  };

  const fetchCertificates = async () => {
    try {
      setLoading(prev => ({ ...prev, certificates: true }));
      const response = await fetch(`${API_URL}/certificates/${userId}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setCertificates(data.certificates || []);
        setError(prev => ({ ...prev, certificates: null }));
      } else {
        setError(prev => ({ ...prev, certificates: 'فشل في تحميل الشهادات' }));
      }
    } catch (err) {
      setError(prev => ({ ...prev, certificates: 'خطأ في الاتصال بالخادم' }));
      console.error('Error fetching certificates:', err);
    } finally {
      setLoading(prev => ({ ...prev, certificates: false }));
    }
  };

  const fetchPermits = async () => {
    try {
      setLoading(prev => ({ ...prev, permits: true }));
      const response = await fetch(`${API_URL}/permits/${establishmentId}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setPermits(data.permits || []);
        setError(prev => ({ ...prev, permits: null }));
      } else {
        setError(prev => ({ ...prev, permits: 'فشل في تحميل تصاريح العمل' }));
      }
    } catch (err) {
      setError(prev => ({ ...prev, permits: 'خطأ في الاتصال بالخادم' }));
      console.error('Error fetching permits:', err);
    } finally {
      setLoading(prev => ({ ...prev, permits: false }));
    }
  };

  const fetchReminders = async () => {
    try {
      setLoading(prev => ({ ...prev, reminders: true }));
      const response = await fetch(`${API_URL}/reminders/${userId}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setReminders(data.reminders || []);
        setError(prev => ({ ...prev, reminders: null }));
      } else {
        setError(prev => ({ ...prev, reminders: 'فشل في تحميل التذكيرات' }));
      }
    } catch (err) {
      setError(prev => ({ ...prev, reminders: 'خطأ في الاتصال بالخادم' }));
      console.error('Error fetching reminders:', err);
    } finally {
      setLoading(prev => ({ ...prev, reminders: false }));
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'غير محدد';
    const date = new Date(dateString);
    return date.toLocaleDateString('ar-SA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  // Define tabs based on user type
  const tabs = [
    { id: 'resumes', label: 'السير الذاتية', icon: FileText, count: resumes.length },
    { id: 'contracts', label: 'العقود', icon: FileCheck, count: contracts.length },
    { id: 'certificates', label: 'الشهادات', icon: BriefcaseIcon, count: certificates.length },
    ...(userType === 'business_owner' ? [
      { id: 'permits', label: 'تصاريح العمل', icon: Shield, count: permits.length }
    ] : []),
    { id: 'reminders', label: 'التذكيرات', icon: Bell, count: reminders.length }
  ];

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
          <Link to="/chat" className="inline-flex items-center text-purple-600 hover:text-purple-700 mb-4">
            <ArrowRight className="w-5 h-5 ml-2" />
            العودة للمحادثة
          </Link>
          <h1 className="text-4xl font-bold text-gray-900 text-right">لوحة التحكم</h1>
          <p className="text-gray-600 text-right mt-2">جميع بياناتك في مكان واحد</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-white rounded-xl p-4 shadow-md border border-purple-100"
          >
            <div className="text-right">
              <p className="text-gray-600 text-xs">السير الذاتية</p>
              <p className="text-2xl font-bold text-purple-600">{resumes.length}</p>
            </div>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-white rounded-xl p-4 shadow-md border border-blue-100"
          >
            <div className="text-right">
              <p className="text-gray-600 text-xs">العقود</p>
              <p className="text-2xl font-bold text-blue-600">{contracts.length}</p>
            </div>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-white rounded-xl p-4 shadow-md border border-green-100"
          >
            <div className="text-right">
              <p className="text-gray-600 text-xs">الشهادات</p>
              <p className="text-2xl font-bold text-green-600">{certificates.length}</p>
            </div>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-white rounded-xl p-4 shadow-md border border-indigo-100"
          >
            <div className="text-right">
              <p className="text-gray-600 text-xs">التذكيرات</p>
              <p className="text-2xl font-bold text-indigo-600">{reminders.length}</p>
            </div>
          </motion.div>
        </div>

        {/* Tabs Navigation */}
        <div className="bg-white rounded-xl shadow-md p-2 mb-6">
          <div className="flex gap-2 overflow-x-auto">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-6 py-3 rounded-lg transition whitespace-nowrap ${
                    isActive
                      ? 'bg-purple-600 text-white shadow-lg'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-semibold">{tab.label}</span>
                  {tab.count > 0 && (
                    <span className={`px-2 py-0.5 rounded-full text-xs ${
                      isActive ? 'bg-white/20' : 'bg-gray-200'
                    }`}>
                      {tab.count}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* Tab Content */}
        <div>
          {activeTab === 'resumes' && (
            <ResumesTab
              resumes={resumes}
              loading={loading.resumes}
              error={error.resumes}
              onRefresh={fetchResumes}
              formatDate={formatDate}
            />
          )}
          
          {activeTab === 'contracts' && (
            <ContractsTab
              contracts={contracts}
              loading={loading.contracts}
              error={error.contracts}
              onRefresh={fetchContracts}
              formatDate={formatDate}
            />
          )}
          
          {activeTab === 'certificates' && (
            <CertificatesTab
              certificates={certificates}
              loading={loading.certificates}
              error={error.certificates}
              onRefresh={fetchCertificates}
              formatDate={formatDate}
            />
          )}
          
          {activeTab === 'permits' && userType === 'business_owner' && (
            <WorkPermitsTab
              permits={permits}
              loading={loading.permits}
              error={error.permits}
              onRefresh={fetchPermits}
              formatDate={formatDate}
            />
          )}
          
          {activeTab === 'reminders' && (
            <RemindersTab
              reminders={reminders}
              loading={loading.reminders}
              error={error.reminders}
              onRefresh={fetchReminders}
              formatDate={formatDate}
            />
          )}
        </div>
      </div>
    </motion.div>
  );
}
