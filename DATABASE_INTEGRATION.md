# 🗄️ Supabase Database Integration - Complete Guide

**Status**: ✅ Fully Implemented  
**Date**: November 12, 2025  
**System**: AgentX - Qiwa AI Customer Service Agent

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Database Schema](#database-schema)
4. [Setup Instructions](#setup-instructions)
5. [How It Works](#how-it-works)
6. [Testing](#testing)
7. [Querying Data](#querying-data)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The system now uses **dual storage architecture**:

- **PRIMARY**: JSON files (in `backend/Agents/logs/`) - Dev/debug, never fails
- **SECONDARY**: Supabase PostgreSQL - Production analytics, rich querying

### Why Dual Storage?

✅ **Safety**: System won't crash if Supabase fails  
✅ **Development**: JSON files for quick debugging  
✅ **Production**: Supabase for real analytics and insights  
✅ **Flexibility**: Can disable Supabase without breaking anything

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     USER MESSAGE                         │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              real_employee_router.py                     │
│  • Logs user message → JSON + Supabase                  │
│  • Creates user profile (first interaction)             │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  real_agent.py                           │
│  • Invokes LLM with tools                               │
│  • Logs each tool call → Supabase (with timing)         │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│            Tools (Resume, Ticket, Knowledge)             │
│  • Execute operations                                    │
│  • Write to JSON (primary)                              │
│  • Write to Supabase (secondary)                        │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              real_employee_router.py                     │
│  • Logs assistant response → JSON + Supabase            │
│  • Logs process steps → Supabase                        │
│  • Updates user behavior → Supabase                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🗂️ Database Schema

### 7 Tables

#### 1. **user_profile** (Identity)
| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| user_id | UUID | Unique user identifier |
| full_name | TEXT | User's full name |
| phone | TEXT | Phone number |
| created_at | TIMESTAMP | Profile creation time |

#### 2. **user_behavior** (Analytics)
| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| user_id | UUID | User reference |
| last_message | TEXT | Last user message |
| predicted_need | TEXT | Predicted user need |
| intent | TEXT | service/complaint/inquiry/support |
| updated_at | TIMESTAMP | Last update time |

#### 3. **conversations** (Message History)
| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| user_id | UUID | User reference |
| role | TEXT | user/assistant |
| content | TEXT | Message content |
| created_at | TIMESTAMP | Message timestamp |

#### 4. **resumes** (Resume Management)
| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| user_id | UUID | User reference |
| resume_id | TEXT | Unique resume ID |
| full_name | TEXT | Resume full name |
| job_title | TEXT | Job title |
| contact | JSONB | Contact info |
| education | JSONB | Education array |
| experience | JSONB | Experience array |
| skills | JSONB | Skills array |
| summary | TEXT | Resume summary |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update time |

#### 5. **tickets** (Support Tickets)
| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| user_id | UUID | User reference |
| ticket_id | TEXT | Unique ticket ID |
| type | TEXT | Ticket type |
| description | TEXT | Ticket description |
| status | TEXT | open/in_progress/resolved/closed |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update time |
| closed_at | TIMESTAMP | Close time (nullable) |

#### 6. **tool_calls** (Analytics - Tool Usage)
| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| user_id | UUID | User reference |
| session_id | TEXT | Session ID |
| tool_name | TEXT | Tool name |
| tool_input | JSONB | Tool input parameters |
| tool_output | TEXT | Tool output |
| execution_time_ms | INT | Execution time in ms |
| success | BOOLEAN | Success status |
| error_message | TEXT | Error message (if failed) |
| created_at | TIMESTAMP | Execution timestamp |

#### 7. **process_steps** (Live Checklist Tracking)
| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| user_id | UUID | User reference |
| session_id | TEXT | Session ID |
| step_id | TEXT | Step identifier |
| step_title | TEXT | Step title |
| step_status | TEXT | pending/in_progress/done/failed |
| step_meta | JSONB | Additional metadata |
| created_at | TIMESTAMP | Step creation time |
| updated_at | TIMESTAMP | Step update time |

---

## 🚀 Setup Instructions

### Step 1: Apply Database Schema

1. **Login to Supabase Dashboard**: https://supabase.com/dashboard
2. **Select your project**: `womyztswwrnyazqglryg`
3. **Navigate to SQL Editor**
4. **Run the schema file**:
   ```bash
   cat backend/Agents/database/schema.sql
   ```
   Copy and paste the entire SQL script into the SQL editor and execute.

5. **Verify tables created**:
   ```sql
   SELECT tablename FROM pg_tables WHERE schemaname = 'public';
   ```

### Step 2: Configure Environment Variables

#### Backend (.env)
The credentials are already hardcoded in `config/settings.py`, but if you want to use `.env`:

```bash
# Add to backend/Agents/.env
SUPABASE_URL=https://womyztswwrnyazqglryg.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndvbXl6dHN3d3JueWF6cWdscnlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5NTAzMDgsImV4cCI6MjA3ODUyNjMwOH0.C-DRpZva7Xc5agXOmXb1sIQzlv89tXyH_gebcmLll1Q
```

#### Frontend (.env.local)
```bash
# Create front-end/.env.local
cp front-end/.env.local.example front-end/.env.local
```

The file should contain:
```
VITE_SUPABASE_URL=https://womyztswwrnyazqglryg.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndvbXl6dHN3d3JueWF6cWdscnlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5NTAzMDgsImV4cCI6MjA3ODUyNjMwOH0.C-DRpZva7Xc5agXOmXb1sIQzlv89tXyH_gebcmLll1Q
```

### Step 3: Test Connection

```bash
cd backend/Agents
python3 database/test_connection.py
```

You should see:
```
🎉 ALL TESTS PASSED! Supabase integration is working perfectly!
```

---

## ⚙️ How It Works

### Data Flow Examples

#### Example 1: User Sends Message

```python
# 1. Router receives message
user_message = "أريد إضافة سيرتي الذاتية"

# 2. JSON log (primary - always succeeds)
log_chat(sessionId, userId, "user", message)

# 3. Supabase log (secondary - won't break if fails)
supabase_conversation_storage.log_message(userId, "user", message)
```

#### Example 2: Agent Calls Tool

```python
# Agent invokes "add_resume" tool
start_time = time.time()
result = resume_tool.add_resume(userId, resume_data)
execution_time_ms = int((time.time() - start_time) * 1000)

# Log to Supabase with timing
supabase_tool_call_storage.log_tool_call(
    userId=userId,
    sessionId=sessionId,
    tool_name="add_resume",
    tool_input=resume_data,
    tool_output=result,
    execution_time_ms=245,  # actual measured time
    success=True
)
```

#### Example 3: Resume Created

```python
# 1. JSON storage (primary)
resume_storage.save_resume(userId, resumeId, resume_data)

# 2. Supabase storage (secondary)
supabase_resume_storage.save_resume(userId, resumeId, resume_data)

# Both happen, JSON always succeeds, Supabase errors are caught
```

---

## 🧪 Testing

### Run Full Test Suite

```bash
cd backend/Agents
python3 database/test_connection.py
```

### Manual Testing via WebSocket

1. Start backend:
   ```bash
   cd backend/Agents
   python3 -m uvicorn app:app --reload
   ```

2. Connect via WebSocket and send a message

3. Check Supabase dashboard to see data flowing in real-time

### Test Individual Components

```python
# In Python shell
from database.supabase_storage import supabase_conversation_storage

supabase_conversation_storage.log_message(
    userId="550e8400-e29b-41d4-a716-446655440000",
    role="user",
    content="مرحباً"
)
```

---

## 📊 Querying Data

### Example Queries in Supabase SQL Editor

#### Get User Activity Summary
```sql
SELECT * FROM user_activity_summary;
```

#### Get Conversation History for User
```sql
SELECT * FROM conversations 
WHERE user_id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY created_at DESC
LIMIT 50;
```

#### Get Tool Usage Statistics
```sql
SELECT 
    tool_name,
    COUNT(*) as call_count,
    AVG(execution_time_ms) as avg_time_ms,
    SUM(CASE WHEN success THEN 1 ELSE 0 END) as success_count
FROM tool_calls
GROUP BY tool_name
ORDER BY call_count DESC;
```

#### Get Daily Active Users
```sql
SELECT * FROM daily_metrics
ORDER BY date DESC
LIMIT 30;
```

#### Get Recent Tickets
```sql
SELECT 
    t.ticket_id,
    t.type,
    t.status,
    u.full_name,
    t.created_at
FROM tickets t
JOIN user_profile u ON t.user_id = u.user_id
ORDER BY t.created_at DESC
LIMIT 20;
```

### Using Frontend Supabase Client

```javascript
import { getUserConversations, getUserAnalytics } from './lib/supabase';

// Get user's conversation history
const conversations = await getUserConversations(userId);

// Get user analytics
const analytics = await getUserAnalytics(userId);
console.log(analytics);
// { totalMessages: 45, totalTickets: 3, totalResumes: 2, totalToolCalls: 67 }
```

---

## 🔧 Troubleshooting

### Issue 1: "Supabase not available" warnings

**Cause**: Supabase client failed to initialize  
**Solution**: Check credentials in `config/settings.py` or `.env`

```bash
cd backend/Agents
python3 -c "from database.supabase_client import test_connection; test_connection()"
```

### Issue 2: Schema version table not found

**Cause**: Schema SQL not applied  
**Solution**: Run `schema.sql` in Supabase SQL Editor

### Issue 3: UUID format errors

**Cause**: userId is not valid UUID  
**Solution**: The storage classes auto-convert, but ensure userId is UUID-compatible string

```python
import uuid
userId = str(uuid.uuid4())  # Always use this format
```

### Issue 4: Data not appearing in Supabase

**Possible causes**:
1. Backend not restarted after integration
2. Supabase write failed silently (check console for warnings)
3. User ID mismatch

**Debug**:
```bash
# Check backend logs
cd backend/Agents
python3 -m uvicorn app:app --reload

# Watch for warnings like:
# ⚠️ Supabase conversation logging failed: ...
```

---

## 📈 Analytics Insights

With Supabase integration, you can now answer questions like:

- **How many users interact with the agent daily?**
- **What are the most used tools?**
- **Average tool execution time?**
- **Which intents are most common?**
- **Conversation flow patterns?**
- **Resume creation success rate?**
- **Ticket resolution time?**

All of this without modifying any existing functionality! 🎉

---

## 📚 File Reference

### Backend Files

| File | Purpose |
|------|---------|
| `database/schema.sql` | Complete database schema |
| `database/supabase_client.py` | Supabase connection singleton |
| `database/supabase_storage.py` | All storage classes (7 tables) |
| `database/test_connection.py` | Comprehensive test suite |
| `storage/resume_storage.py` | Dual-write resume storage |
| `storage/ticket_storage.py` | Dual-write ticket storage |
| `agents/real_agent.py` | Tool call logging |
| `routers/real_employee_router.py` | Conversation & behavior logging |

### Frontend Files

| File | Purpose |
|------|---------|
| `src/lib/supabase.js` | Supabase client + helper functions |
| `.env.local.example` | Environment template |

---

## 🎯 Summary

✅ **Dual storage**: JSON (primary) + Supabase (secondary)  
✅ **7 tables**: Full coverage of all data  
✅ **Non-breaking**: System works even if Supabase fails  
✅ **Analytics-ready**: Rich querying capabilities  
✅ **Real-time tracking**: Tool calls, process steps, conversations  
✅ **Production-ready**: Safe, tested, documented  

**The system is now fully integrated with Supabase while maintaining backward compatibility! 🚀**

