# 🧪 **COMPREHENSIVE TESTING GUIDE - ALL FEATURES**

## 🎯 **WHAT CHANGED**

### ✅ **Development Mode Enabled**
- **File**: `backend/Agents/config/settings.py`
- **Flag**: `DEV_MODE_ALL_FEATURES = True`
- **Effect**: **ALL TOOLS are now available regardless of user_type!**

### ✅ **Agent Updated**
- **File**: `backend/Agents/agents/real_agent.py`
- **Change**: Modified tool loading to enable ALL features in dev mode
- **Result**: You can now test ALL features (employee, business owner, service provider) with ANY user!

---

## 🚀 **QUICK START**

### **1. Restart Backend** (REQUIRED!)
```bash
cd backend/Agents
python3 app.py
```

### **2. Open Chat**
```
http://localhost:5173/chat
```

### **3. Start Testing!**
All features are now available via voice or text chat! ✨

---

## 📋 **ALL FEATURES TO TEST**

### **Feature 1: Contract Management** 📄
**What**: View your employment contracts

**Voice Commands:**
- "أريد رؤية عقدي"
- "اعرض لي عقد العمل"
- "ما تفاصيل عقدي؟"

**Expected Response:**
```
عقدك: الشركة: شركة أرامكو السعودية
الوظيفة: مهندس برمجيات أول
الراتب: 15,000 ريال
```

**Dashboard Check:**
- Go to `http://localhost:5173/dashboard`
- Click "العقود" tab
- Should see 2 contracts with details

---

### **Feature 2: Certificate Requests** 📜
**What**: Request salary certificates or experience letters

**Voice Commands:**
```
You: "أريد طلب شهادة راتب"
Agent: "ما هو الغرض من الشهادة؟"
You: "للتأشيرة" (or "للبنك" or "وظيفة جديدة")
Agent: "تم استلام طلب شهادة الراتب..."
```

**Or single command:**
```
"أريد طلب شهادة راتب للتأشيرة"
```

**For experience letter:**
```
"اطلب خطاب خبرة للوظيفة الجديدة"
```

**Dashboard Check:**
- Click "الشهادات" tab
- Should see 3 certificates:
  - ✅ Salary (ready) - green
  - ⏳ Experience (processing) - yellow  
  - 📋 Salary (requested) - blue

---

### **Feature 3: Work Permits** 🛡️
**What**: Manage employee work permits (for business owners)

**Voice Commands:**
```
"عرض تصاريح العمل"
→ Agent: "لديك 5 تصريح عمل"

"تحقق من التصاريح المنتهية"
→ Agent: "⚠️ 2 تصريح ينتهي قريباً: أحمد محمد, فاطمة حسن"

"جدد تصريح رقم PER2607EBEF"
→ Agent: "تم تجديد التصريح بنجاح"
```

**Dashboard Check:**
- Click "لوحة التحكم" → Need to add Work Permits tab (business owner feature)
- **NOTE**: Currently you need to be business_owner to see this tab in dashboard

---

### **Feature 4: End-of-Service Calculator** 💰
**What**: Calculate end-of-service rewards according to Saudi labor law

**Voice Commands:**
```
You: "احسب مكافأة نهاية الخدمة"
Agent: "متى بدأت العمل؟"
You: "2020-01-01"

Agent: "متى انتهى العمل؟"
You: "2024-01-01"

Agent: "ما هو راتبك الشهري؟"
You: "10000"

Agent: "ما نوع الإنهاء؟ (resignation, contract_end, termination)"
You: "resignation"

Agent: "مكافأة نهاية الخدمة: XX,XXX ريال
       
التفصيل:
- السنة 1-5: راتب نصف شهر لكل سنة
- بعد 5 سنوات: راتب شهر كامل لكل سنة
..."
```

**This follows actual Saudi labor law calculations!**

---

### **Feature 5: Proactive Reminders** 🔔
**What**: System automatically reminds you of important events

**Voice Commands:**
```
"عرض التذكيرات"
→ Agent: "لديك 4 تذكيرات:
- ⚠️ عقدك مع شركة أرامكو ينتهي خلال 30 يوم
- ⚠️ تصريح عمل الموظف أحمد محمد ينتهي خلال 15 يوم
- ✅ شهادة الراتب المطلوبة جاهزة للتحميل
- 📋 تذكير: تحديث بياناتك الشخصية"
```

**Dashboard Check:**
- Click "التذكيرات" tab
- Should see 4 reminders with:
  - Color coding (orange/red/green)
  - Action buttons
  - Trigger dates

---

### **Feature 6: Enhanced Resume Validation** ✨
**What**: Now requires education AND experience (not just name + job)

**Voice Commands:**
```
You: "أضف سيرتي الذاتية"
Agent: "ما اسمك الكامل؟"
You: "زياد الحربي"

Agent: "ما مسماك الوظيفي؟"
You: "مهندس ذكاء اصطناعي"

Agent: "ما بريدك الإلكتروني؟"
You: "ziyad@test.com"

Agent: "ما رقم هاتفك؟"
You: "0544123456"

[NEW! Agent will now ask:]
Agent: "ما تعليمك؟ (مثلاً: بكالوريوس علوم حاسب - جامعة الملك سعود - 2020)"
You: "ماجستير ذكاء اصطناعي - جامعة ستانفورد - 2022"

Agent: "ما خبرتك العملية؟ (مثلاً: مهندس برمجيات - شركة أرامكو - 2020 إلى 2023)"
You: "مهندس ذكاء اصطناعي - شركة علي بابا - 2022 إلى الآن"

Agent: "تم إضافة السيرة الذاتية بنجاح!"
```

**If you skip education/experience:**
```
Agent: "عذراً، السيرة الذاتية تحتاج إلى تعليم وخبرة عملية. يرجى تقديم هذه المعلومات."
```

---

## 🎮 **TESTING MATRIX**

### **Test Each Feature Via:**
| Feature | Voice Chat | Text Chat | Dashboard View |
|---------|-----------|-----------|----------------|
| Contracts | ✅ | ✅ | ✅ |
| Certificates | ✅ | ✅ | ✅ |
| Work Permits | ✅ | ✅ | ⚠️ (need tab) |
| Reward Calc | ✅ | ✅ | ❌ (calc only) |
| Reminders | ✅ | ✅ | ✅ |
| Resume (enhanced) | ✅ | ✅ | ✅ |

---

## 🔍 **HOW TO VERIFY IT'S WORKING**

### **Check 1: Agent System Prompt**
When you restart backend, you should see:
```
✅ Mock user initialized: زياد الحربي (employee) (a1b2c3d4...)
```

### **Check 2: Tool Count**
In the backend logs, when a chat starts, you should see:
```
Tools loaded: 13+  (all tools from all user types)
```

### **Check 3: Agent Response**
When you first connect, agent should say:
```
"مرحباً! أنا مساعد قوى الذكي. 🔧 وضع التطوير نشط - جميع الميزات متاحة للاختبار!"
```

---

## 📊 **EXPECTED DATA (Seeded)**

### **Contracts: 2**
1. أرامكو - 15,000 ريال - نشط
2. STC - 12,000 ريال - نشط

### **Certificates: 3**
1. Salary (visa) - Ready ✅
2. Experience (new_job) - Processing ⏳
3. Salary (loan) - Requested 📋

### **Work Permits: 5**
1. أحمد محمد - Expiring soon (15 days) ⚠️
2. محمد علي - Active ✅
3. فاطمة حسن - Expiring soon (5 days) ⚠️
4. خالد إبراهيم - Expired ❌
5. سارة أحمد - Active ✅

### **Reminders: 4**
1. Contract expiry (أرامكو) - 30 days
2. Permit expiry (أحمد) - 15 days
3. Certificate ready - Now
4. Custom reminder - 7 days

---

## 🐛 **TROUBLESHOOTING**

### **Problem 1: Agent says "I don't have that tool"**
**Solution**: Restart backend! `cd backend/Agents && python3 app.py`

### **Problem 2: Dashboard shows "No data"**
**Solution**: Re-run seed script:
```bash
cd backend/Agents
python3 seed_demo_data.py
```

### **Problem 3: Tools not responding**
**Check**:
1. Backend running? → `http://localhost:8000/health`
2. WebSocket connected? → Check browser console
3. Data files exist? → Check `backend/Agents/data/`

### **Problem 4: Agent asks for resume ID even in dev mode**
**This is FIXED!** Agent now auto-uses the last accessed resume.

---

## 🎯 **COMPLETE TEST SEQUENCE**

### **30-Minute Full Test**

**Minutes 0-5: Setup**
```bash
1. cd backend/Agents && python3 app.py
2. Open http://localhost:5173/chat
3. Click phone icon to start voice call
```

**Minutes 5-10: Contract Features**
```
1. "أريد رؤية عقدي"
2. Go to dashboard → Check contracts tab
3. Click "عرض التفاصيل"
```

**Minutes 10-15: Certificate Features**
```
1. "اطلب شهادة راتب للبنك"
2. Go to dashboard → Check certificates tab
3. Verify new certificate appears
```

**Minutes 15-20: Work Permit Features**
```
1. "عرض تصاريح العمل"
2. "تحقق من التصاريح المنتهية"
3. "جدد تصريح رقم [ID]"
```

**Minutes 20-25: Reward Calculator**
```
1. "احسب مكافأة نهاية الخدمة"
2. Answer all prompts
3. Verify calculation explanation
```

**Minutes 25-30: Reminders & Resume**
```
1. "عرض التذكيرات"
2. Go to dashboard → Check reminders tab
3. "أضف سيرة ذاتية" (test enhanced validation)
```

---

## ✅ **SUCCESS CRITERIA**

You know it's working if:
- ✅ Agent responds to ALL feature requests
- ✅ Dashboard tabs show seeded data
- ✅ Resume creation requires education + experience
- ✅ Voice call mode works smoothly
- ✅ No "I don't have access to that tool" errors

---

## 🎉 **YOU'RE ALL SET!**

**Current Status:**
- ✅ 6 resumes
- ✅ 2 contracts
- ✅ 3 certificates  
- ✅ 5 work permits
- ✅ 4 reminders
- ✅ ALL tools enabled
- ✅ Enhanced validation active

**Just restart backend and start testing!** 🚀

---

## 📝 **NOTES FOR PRODUCTION**

When you're ready to deploy:

1. **Turn off dev mode**:
   ```python
   # In backend/Agents/config/settings.py
   DEV_MODE_ALL_FEATURES = False  # IMPORTANT!
   ```

2. **User types will be enforced**:
   - Employees → Resume, Contract, Certificate tools only
   - Business Owners → Work Permit tools only
   - Service Providers → Reward Calculator only

3. **Dashboard tabs will be user-type-specific**:
   - The frontend already handles this via `MOCK_USER.user_type`

**For now, enjoy testing ALL features! 🎉**

