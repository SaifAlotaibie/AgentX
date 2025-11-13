-- =====================================================
-- FIX SUPABASE SCHEMA - Run this in Supabase SQL Editor
-- This will fix all missing tables and columns
-- =====================================================

-- Drop old tables with wrong schema
DROP TABLE IF EXISTS resumes CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;

-- Create complete schema
-- =====================================================
-- 4. RESUMES TABLE (FIXED - with all columns)
-- =====================================================
CREATE TABLE IF NOT EXISTS resumes (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    resume_id TEXT NOT NULL UNIQUE,
    full_name TEXT,
    job_title TEXT,
    contact JSONB,  -- {email, phone}
    education JSONB,  -- array of education entries
    experience JSONB,  -- array of experience entries
    skills JSONB,  -- array of skills
    summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);
CREATE INDEX IF NOT EXISTS idx_resumes_resume_id ON resumes(resume_id);
CREATE INDEX IF NOT EXISTS idx_resumes_created_at ON resumes(created_at DESC);

-- =====================================================
-- 5. TICKETS TABLE (FIXED - with all columns)
-- =====================================================
CREATE TABLE IF NOT EXISTS tickets (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    ticket_id TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,  -- resume_add, resume_edit, resume_delete, qa
    description TEXT,
    status TEXT NOT NULL CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    closed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_tickets_user_id ON tickets(user_id);
CREATE INDEX IF NOT EXISTS idx_tickets_ticket_id ON tickets(ticket_id);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_created_at ON tickets(created_at DESC);

-- =====================================================
-- 6. TOOL CALLS TABLE (NEW)
-- =====================================================
CREATE TABLE IF NOT EXISTS tool_calls (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    session_id TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    tool_input JSONB,  -- structured input parameters
    tool_output TEXT,
    execution_time_ms INT,
    success BOOLEAN DEFAULT true,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tool_calls_user_id ON tool_calls(user_id);
CREATE INDEX IF NOT EXISTS idx_tool_calls_session_id ON tool_calls(session_id);
CREATE INDEX IF NOT EXISTS idx_tool_calls_tool_name ON tool_calls(tool_name);
CREATE INDEX IF NOT EXISTS idx_tool_calls_created_at ON tool_calls(created_at DESC);

-- =====================================================
-- 7. PROCESS STEPS TABLE (NEW)
-- =====================================================
CREATE TABLE IF NOT EXISTS process_steps (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    session_id TEXT NOT NULL,
    step_id TEXT NOT NULL,
    step_title TEXT NOT NULL,
    step_status TEXT NOT NULL CHECK (step_status IN ('pending', 'in_progress', 'done', 'failed')),
    step_meta JSONB,  -- additional metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_process_steps_user_id ON process_steps(user_id);
CREATE INDEX IF NOT EXISTS idx_process_steps_session_id ON process_steps(session_id);
CREATE INDEX IF NOT EXISTS idx_process_steps_created_at ON process_steps(created_at DESC);

-- =====================================================
-- TRIGGERS FOR AUTO-UPDATING updated_at
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers
CREATE TRIGGER update_resumes_updated_at BEFORE UPDATE ON resumes
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tickets_updated_at BEFORE UPDATE ON tickets
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_behavior_updated_at BEFORE UPDATE ON user_behavior
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_process_steps_updated_at BEFORE UPDATE ON process_steps
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- SCHEMA VERSION
-- =====================================================
CREATE TABLE IF NOT EXISTS schema_version (
    version INT PRIMARY KEY,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    description TEXT
);

INSERT INTO schema_version (version, description) 
VALUES (1, 'Fixed schema with all columns - resumes, tickets, tool_calls, process_steps')
ON CONFLICT (version) DO NOTHING;

-- =====================================================
-- VERIFICATION QUERY (Run this after)
-- =====================================================
-- SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;

