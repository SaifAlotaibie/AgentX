import { useNavigate } from 'react-router-dom';
import { MessageSquare, FileText, Users, Briefcase, TrendingUp, Shield } from 'lucide-react';

export default function QiwaMainPage() {
  const navigate = useNavigate();

  const services = [
    {
      icon: '💼',
      title: 'إصدار الشهادات للعمال',
      description: 'خدمة إصدار شهادات العمل بالضمانة الاجتماعية الموثقة'
    },
    {
      icon: '👔',
      title: 'عقود العمل',
      description: 'إصدار وإدارة وتجديد عقود العمل إلكترونياً'
    },
    {
      icon: '🔍',
      title: 'التفتيش الإلكتروني',
      description: 'خدمات التفتيش الإلكتروني لضمان سلامة بيئة العمل'
    },
    {
      icon: '📊',
      title: 'إدارة الأجور',
      description: 'خدمات حماية الأجور وإدارة الرواتب إلكترونياً'
    },
    {
      icon: '🎯',
      title: 'استقدام العمالة',
      description: 'خدمات استقدام العمالة المنزلية والعمالة المهنية'
    },
    {
      icon: '💰',
      title: 'استخدام النطاقات',
      description: 'الاستعلام والتعامل مع نظام نطاقات للمنشآت'
    }
  ];

  const stats = [
    { number: '99.9%', label: 'نسبة الموثوقية' },
    { number: '500K+', label: 'منشأة مسجلة' },
    { number: '15M+', label: 'عقود تشغيل' },
    { number: '2.5M+', label: 'معاملة يومية' }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Bar */}
      <div className="bg-green-700 text-white py-2 px-6 text-sm">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <span>اليوم الموافق 19/11</span>
          <span>English</span>
        </div>
      </div>

      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center">
                <Briefcase className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">وزارة الموارد البشرية</h1>
                <p className="text-xs text-gray-600">Ministry of Human Resources</p>
              </div>
            </div>
            <nav className="flex gap-6 text-gray-700">
              <a href="#" className="hover:text-green-600">الرئيسية</a>
              <a href="#" className="hover:text-green-600">الخدمات</a>
              <a href="#" className="hover:text-green-600">عن الوزارة</a>
              <a href="#" className="hover:text-green-600">اتصل بنا</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Banner */}
      <section className="bg-gradient-to-r from-green-600 to-emerald-700 text-white py-16 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="inline-block bg-white/20 backdrop-blur-sm rounded-full px-4 py-2 mb-4">
                <span className="text-sm font-medium">💼 منصة قوى</span>
              </div>
              <h1 className="text-5xl font-bold mb-4">منصة قوى في أرقام</h1>
              <p className="text-xl text-green-100 mb-6">
                منصة إلكترونية متكاملة تدير كافة خدمات سوق العمل إلكترونياً
              </p>
            </div>
            <div className="flex-1 flex justify-center">
              <div className="w-64 h-64 bg-white/10 backdrop-blur-sm rounded-3xl flex items-center justify-center">
                <div className="text-center">
                  <div className="text-7xl mb-4">📊</div>
                  <div className="text-2xl font-bold">أرقام موثوقة</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 px-6 bg-white border-b">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-4 gap-6">
            {stats.map((stat, idx) => (
              <div key={idx} className="text-center p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl">
                <div className="text-4xl font-bold text-green-700 mb-2">{stat.number}</div>
                <div className="text-gray-600 font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-16 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">خدمات المنصة</h2>
            <p className="text-xl text-gray-600">
              خدمات رقمية متكاملة لإدارة سوق العمل السعودي
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            {services.map((service, idx) => (
              <div key={idx} className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border border-gray-100">
                <div className="w-16 h-16 bg-green-100 rounded-xl flex items-center justify-center text-3xl mb-4">
                  {service.icon}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{service.title}</h3>
                <p className="text-gray-600 mb-4">{service.description}</p>
                <button className="text-green-600 hover:text-green-700 font-semibold flex items-center gap-2">
                  الدخول للخدمة ←
                </button>
              </div>
            ))}
          </div>

          {/* Customer Service CTA */}
          <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 rounded-3xl p-12 text-white text-center shadow-2xl">
            <div className="max-w-3xl mx-auto">
              <div className="inline-block bg-white/20 backdrop-blur-sm rounded-full px-6 py-3 mb-6">
                <MessageSquare className="inline-block w-6 h-6 mr-2" />
                <span className="font-semibold">خدمة العملاء الذكية</span>
              </div>
              
              <h2 className="text-4xl font-bold mb-4">تحتاج مساعدة؟</h2>
              <p className="text-xl text-blue-100 mb-8">
                مساعدك الشخصي الذكي متاح على مدار الساعة للإجابة على استفساراتك وإدارة سيرتك الذاتية
              </p>
              
              <div className="flex justify-center gap-4 mb-8">
                <div className="bg-white/20 backdrop-blur-sm rounded-xl px-6 py-4">
                  <div className="text-3xl font-bold">24/7</div>
                  <div className="text-sm">متاح دائماً</div>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-xl px-6 py-4">
                  <div className="text-3xl font-bold">AI</div>
                  <div className="text-sm">ذكاء اصطناعي</div>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-xl px-6 py-4">
                  <div className="text-3xl font-bold">عربي</div>
                  <div className="text-sm">يتحدث العربية</div>
                </div>
              </div>

              <button
                onClick={() => navigate('/chat')}
                className="bg-white text-blue-700 px-12 py-5 rounded-full text-xl font-bold shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all inline-flex items-center gap-3"
              >
                <MessageSquare className="w-6 h-6" />
                ابدأ المحادثة مع الوكيل الذكي
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Knowledge Center */}
      <section className="py-16 px-6 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-12">مركز المعرفة</h2>
          <div className="grid grid-cols-3 gap-8">
            <div className="bg-white rounded-2xl p-8 shadow-lg">
              <FileText className="w-12 h-12 text-blue-600 mx-auto mb-4" />
              <h3 className="font-bold text-xl mb-2">دليل المستخدم</h3>
              <p className="text-gray-600">تعرف على كيفية استخدام المنصة</p>
            </div>
            <div className="bg-white rounded-2xl p-8 shadow-lg">
              <Users className="w-12 h-12 text-green-600 mx-auto mb-4" />
              <h3 className="font-bold text-xl mb-2">خدمات الدعم</h3>
              <p className="text-gray-600">احصل على المساعدة الفورية</p>
            </div>
            <div className="bg-white rounded-2xl p-8 shadow-lg">
              <Shield className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              <h3 className="font-bold text-xl mb-2">حقوق العمال</h3>
              <p className="text-gray-600">تعرف على حقوقك وواجباتك</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold text-lg mb-4">تواصل معنا</h3>
              <p className="text-gray-400 text-sm">الرقم الموحد: 19911</p>
              <p className="text-gray-400 text-sm">care@hrsd.gov.sa</p>
            </div>
            <div>
              <h3 className="font-bold text-lg mb-4">روابط سريعة</h3>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white">الخدمات</a></li>
                <li><a href="#" className="hover:text-white">الاستفسارات</a></li>
                <li><a href="#" className="hover:text-white">الشكاوى والمقترحات</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-lg mb-4">الخدمات</h3>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white">منصة قوى</a></li>
                <li><a href="#" className="hover:text-white">الضمانة الاجتماعية</a></li>
                <li><a href="#" className="hover:text-white">خدمات الأفراد</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-lg mb-4">عن الوزارة</h3>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white">رؤية ورسالة</a></li>
                <li><a href="#" className="hover:text-white">الهيكل التنظيمي</a></li>
                <li><a href="#" className="hover:text-white">المسؤولية المجتمعية</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-6 text-center text-gray-400 text-sm">
            <p>© 2024 جميع الحقوق محفوظة - وزارة الموارد البشرية والتنمية الاجتماعية</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

