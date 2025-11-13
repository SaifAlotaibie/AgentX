import { useNavigate } from 'react-router-dom';
import { Building2, Users, FileText, Briefcase, ShieldCheck, TrendingUp } from 'lucide-react';

export default function HRSDHomePage() {
  const navigate = useNavigate();

  const platforms = [
    {
      id: 'qiwa',
      name: 'قوى',
      nameEn: 'Qiwa',
      description: 'منصة التوظيف الإلكترونية',
      icon: '💼',
      color: 'from-green-500 to-emerald-600',
      path: '/qiwa'
    },
    {
      id: 'takamol',
      name: 'تكامل',
      nameEn: 'Takamol',
      description: 'منصة التكامل والخدمات',
      icon: '🔗',
      color: 'from-blue-500 to-blue-600',
      path: null
    },
    {
      id: 'mudad',
      name: 'مداد',
      nameEn: 'Mudad',
      description: 'خدمات الموارد البشرية',
      icon: '📋',
      color: 'from-purple-500 to-purple-600',
      path: null
    }
  ];

  const handlePlatformClick = (platform) => {
    if (platform.path) {
      navigate(platform.path);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Top Bar */}
      <div className="bg-gradient-to-r from-green-700 to-green-600 text-white py-3 px-6 text-sm">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <span>اليوم الموافق 19/11</span>
          <span>English</span>
        </div>
      </div>

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-green-600 rounded-lg flex items-center justify-center">
                <Building2 className="w-10 h-10 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">وزارة الموارد البشرية</h1>
                <p className="text-sm text-gray-600">Ministry of Human Resources</p>
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

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-green-600 via-green-700 to-green-800 text-white py-20 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-4">أهلاً بك في قوى</h1>
          <p className="text-xl mb-8 text-green-100">
            أكبر قاعدة بيانات للمنشآت والعمال ومقدمي الخدمات في المملكة، نسعى لتمكينها
          </p>
          <div className="flex justify-center gap-4">
            <div className="bg-white/20 backdrop-blur-sm rounded-lg px-6 py-4">
              <div className="text-3xl font-bold">15M+</div>
              <div className="text-sm">عقود تشغيل</div>
            </div>
            <div className="bg-white/20 backdrop-blur-sm rounded-lg px-6 py-4">
              <div className="text-3xl font-bold">500K+</div>
              <div className="text-sm">منشأة مسجلة</div>
            </div>
            <div className="bg-white/20 backdrop-blur-sm rounded-lg px-6 py-4">
              <div className="text-3xl font-bold">2.5M+</div>
              <div className="text-sm">معاملة يومية</div>
            </div>
          </div>
        </div>
      </section>

      {/* Platforms Section */}
      <section className="py-16 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">منصات الوزارة</h2>
            <p className="text-xl text-gray-600">
              خدمات رقمية متكاملة لسوق العمل السعودي
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {platforms.map((platform) => (
              <div
                key={platform.id}
                onClick={() => handlePlatformClick(platform)}
                className={`group relative bg-white rounded-2xl shadow-lg overflow-hidden transition-all duration-300 ${
                  platform.path ? 'cursor-pointer hover:shadow-2xl hover:scale-105' : 'opacity-75'
                }`}
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${platform.color} opacity-5 group-hover:opacity-10 transition-opacity`}></div>
                
                <div className="relative p-8">
                  {/* Icon */}
                  <div className="text-6xl mb-4">{platform.icon}</div>
                  
                  {/* Title */}
                  <h3 className="text-3xl font-bold text-gray-900 mb-2">
                    {platform.name}
                  </h3>
                  <p className="text-lg text-gray-500 mb-4">{platform.nameEn}</p>
                  
                  {/* Description */}
                  <p className="text-gray-600 mb-6">{platform.description}</p>
                  
                  {/* Button */}
                  {platform.path && (
                    <button
                      className={`w-full bg-gradient-to-r ${platform.color} text-white py-3 px-6 rounded-xl font-bold shadow-lg hover:shadow-xl transition-all group-hover:scale-105`}
                    >
                      الدخول للمنصة ←
                    </button>
                  )}
                  
                  {!platform.path && (
                    <div className="w-full bg-gray-200 text-gray-500 py-3 px-6 rounded-xl font-bold text-center">
                      قريباً
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-16 px-6 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">خدمات المنصة</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { icon: '✅', title: 'نقل الخدمات', desc: 'نقل خدمات العمال بين المنشآت' },
              { icon: '👔', title: 'عقود العمل', desc: 'إصدار وإدارة عقود العمل' },
              { icon: '🔍', title: 'التفتيش الإلكتروني', desc: 'خدمات التفتيش والمتابعة' },
              { icon: '📊', title: 'إدارة الأجور', desc: 'خدمات إدارة وحماية الأجور' },
              { icon: '🎯', title: 'استقدام العمالة', desc: 'خدمات الاستقدام المنظمة' },
              { icon: '💰', title: 'استخدام النطاقات', desc: 'برنامج نطاقات للمنشآت' },
              { icon: '🏢', title: 'إصدار الشهادات', desc: 'إصدار الشهادات الرسمية' },
              { icon: '📈', title: 'الشفافية التجارية', desc: 'خدمات الشفافية والمراقبة' }
            ].map((service, idx) => (
              <div key={idx} className="bg-gray-50 rounded-xl p-6 text-center hover:bg-green-50 hover:shadow-lg transition-all">
                <div className="text-4xl mb-3">{service.icon}</div>
                <h3 className="font-bold text-gray-900 mb-2">{service.title}</h3>
                <p className="text-sm text-gray-600">{service.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold text-xl mb-4">تواصل معنا</h3>
              <p className="text-gray-400">الرقم الموحد: 19911</p>
              <p className="text-gray-400">care@hrsd.gov.sa</p>
            </div>
            <div>
              <h3 className="font-bold text-xl mb-4">روابط سريعة</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">الخدمات</a></li>
                <li><a href="#" className="hover:text-white">الاستفسارات</a></li>
                <li><a href="#" className="hover:text-white">الشكاوى</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-xl mb-4">الخدمات</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">منصة قوى</a></li>
                <li><a href="#" className="hover:text-white">خدمة العملاء</a></li>
                <li><a href="#" className="hover:text-white">المدونة القانونية</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-xl mb-4">عن الوزارة</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">رؤية ورسالة</a></li>
                <li><a href="#" className="hover:text-white">الهيكل التنظيمي</a></li>
                <li><a href="#" className="hover:text-white">الخدمات والمساعدة</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
            <p>© 2024 جميع الحقوق محفوظة لوزارة الموارد البشرية والتنمية الاجتماعية - المملكة العربية السعودية</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

