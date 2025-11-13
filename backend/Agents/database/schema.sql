-- =====================================================
-- AgentX Database Schema for Supabase
-- Complete schema with all 7 tables
-- =====================================================

-- =====================================================
-- 1. USER PROFILE TABLE (enhanced with user type)
-- =====================================================
CREATE TABLE IF NOT EXISTS user_profile (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    phone TEXT,
    user_type TEXT CHECK (user_type IN ('employee', 'business_owner', 'service_provider')) DEFAULT 'employee',
    national_id TEXT,
    nationality TEXT,
    establishment_id TEXT,  -- For business owners
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_profile_user_id ON user_profile(user_id);
CREATE INDEX IF NOT EXISTS idx_user_profile_user_type ON user_profile(user_type);

-- =====================================================
-- 2. USER BEHAVIOR TABLE (provided by friend)
-- =====================================================
CREATE TABLE IF NOT EXISTS user_behavior (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE,
    last_message TEXT,
    predicted_need TEXT,
    intent TEXT CHECK (intent IN ('service', 'complaint', 'inquiry', 'support')),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_behavior_user_id ON user_behavior(user_id);
CREATE INDEX IF NOT EXISTS idx_user_behavior_intent ON user_behavior(intent);

-- =====================================================
-- 3. CONVERSATIONS TABLE (provided by friend)
-- =====================================================
CREATE TABLE IF NOT EXISTS conversations (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversations_user_created ON conversations(user_id, created_at DESC);

-- =====================================================
-- 4. RESUMES TABLE (new - for resume management)
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
-- 5. TICKETS TABLE (new - for ticket management)
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
-- 6. TOOL CALLS TABLE (new - for analytics)
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
-- 7. PROCESS STEPS TABLE (new - for checklist tracking)
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
-- VIEWS FOR ANALYTICS
-- =====================================================

-- View: User activity summary
CREATE OR REPLACE VIEW user_activity_summary AS
SELECT 
    u.user_id,
    u.full_name,
    COUNT(DISTINCT c.id) as total_messages,
    COUNT(DISTINCT t.id) as total_tickets,
    COUNT(DISTINCT r.id) as total_resumes,
    COUNT(DISTINCT tc.id) as total_tool_calls,
    MAX(c.created_at) as last_activity
FROM user_profile u
LEFT JOIN conversations c ON u.user_id = c.user_id
LEFT JOIN tickets t ON u.user_id = t.user_id
LEFT JOIN resumes r ON u.user_id = r.user_id
LEFT JOIN tool_calls tc ON u.user_id = tc.user_id
GROUP BY u.user_id, u.full_name;

-- View: Daily activity metrics
CREATE OR REPLACE VIEW daily_metrics AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_conversations,
    COUNT(DISTINCT user_id) as unique_users
FROM conversations
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- =====================================================
-- FUNCTIONS FOR AUTOMATIC TIMESTAMPS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for auto-updating updated_at
CREATE TRIGGER update_resumes_updated_at BEFORE UPDATE ON resumes
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tickets_updated_at BEFORE UPDATE ON tickets
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_behavior_updated_at BEFORE UPDATE ON user_behavior
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_process_steps_updated_at BEFORE UPDATE ON process_steps
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- SAMPLE DATA FOR TESTING (optional - comment out for production)
-- =====================================================
/*
-- Sample user
INSERT INTO user_profile (user_id, full_name, phone) 
VALUES ('550e8400-e29b-41d4-a716-446655440000', 'أحمد محمد العتيبي', '0501234567')
ON CONFLICT (user_id) DO NOTHING;

-- Sample conversation
INSERT INTO conversations (user_id, role, content)
VALUES 
    ('550e8400-e29b-41d4-a716-446655440000', 'user', 'مرحباً، أريد إضافة سيرتي الذاتية'),
    ('550e8400-e29b-41d4-a716-446655440000', 'assistant', 'مرحباً أحمد! سأساعدك في إضافة سيرتك الذاتية...')
ON CONFLICT DO NOTHING;
*/

-- =====================================================
-- 8. CONTRACTS TABLE (new - for employment contracts)
-- =====================================================
CREATE TABLE IF NOT EXISTS contracts (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    contract_id TEXT NOT NULL UNIQUE,
    employer_id TEXT,
    employer_name TEXT,
    job_title TEXT NOT NULL,
    salary DECIMAL(10, 2),
    start_date DATE NOT NULL,
    end_date DATE,
    status TEXT NOT NULL CHECK (status IN ('active', 'pending', 'terminated', 'expired')) DEFAULT 'active',
    renewal_history JSONB,  -- array of renewal records
    termination_reason TEXT,
    termination_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_contracts_user_id ON contracts(user_id);
CREATE INDEX IF NOT EXISTS idx_contracts_contract_id ON contracts(contract_id);
CREATE INDEX IF NOT EXISTS idx_contracts_status ON contracts(status);
CREATE INDEX IF NOT EXISTS idx_contracts_end_date ON contracts(end_date);

-- =====================================================
-- 9. CERTIFICATES TABLE (new - for salary/experience certificates)
-- =====================================================
CREATE TABLE IF NOT EXISTS certificates (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    certificate_id TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL CHECK (type IN ('salary', 'experience')),
    purpose TEXT,  -- visa, loan, new_job, etc.
    status TEXT NOT NULL CHECK (status IN ('requested', 'processing', 'ready', 'delivered')) DEFAULT 'requested',
    request_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ready_date TIMESTAMP WITH TIME ZONE,
    document_url TEXT,
    employee_data JSONB,  -- name, position, salary, employment duration
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_certificates_user_id ON certificates(user_id);
CREATE INDEX IF NOT EXISTS idx_certificates_certificate_id ON certificates(certificate_id);
CREATE INDEX IF NOT EXISTS idx_certificates_status ON certificates(status);
CREATE INDEX IF NOT EXISTS idx_certificates_type ON certificates(type);

-- =====================================================
-- 10. WORK PERMITS TABLE (new - for business owners)
-- =====================================================
CREATE TABLE IF NOT EXISTS work_permits (
    id BIGSERIAL PRIMARY KEY,
    establishment_id TEXT NOT NULL,
    permit_id TEXT NOT NULL UNIQUE,
    employee_id TEXT,
    employee_name TEXT NOT NULL,
    nationality TEXT NOT NULL,
    job_title TEXT NOT NULL,
    issue_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    renewal_cost DECIMAL(10, 2),
    status TEXT NOT NULL CHECK (status IN ('active', 'expiring_soon', 'expired', 'renewal_pending')) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_work_permits_establishment ON work_permits(establishment_id);
CREATE INDEX IF NOT EXISTS idx_work_permits_permit_id ON work_permits(permit_id);
CREATE INDEX IF NOT EXISTS idx_work_permits_status ON work_permits(status);
CREATE INDEX IF NOT EXISTS idx_work_permits_expiry ON work_permits(expiry_date);

-- =====================================================
-- 11. REMINDERS TABLE (new - for proactive notifications)
-- =====================================================
CREATE TABLE IF NOT EXISTS reminders (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    reminder_id TEXT NOT NULL UNIQUE,
    reminder_type TEXT NOT NULL CHECK (reminder_type IN ('contract_expiry', 'permit_expiry', 'certificate_ready', 'custom')),
    related_entity_id TEXT,  -- contract_id, permit_id, certificate_id
    message TEXT NOT NULL,
    trigger_date TIMESTAMP WITH TIME ZONE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'sent', 'dismissed', 'actioned')) DEFAULT 'pending',
    action_taken JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reminders_user_id ON reminders(user_id);
CREATE INDEX IF NOT EXISTS idx_reminders_status ON reminders(status);
CREATE INDEX IF NOT EXISTS idx_reminders_trigger_date ON reminders(trigger_date);
CREATE INDEX IF NOT EXISTS idx_reminders_type ON reminders(reminder_type);

-- =====================================================
-- TRIGGERS FOR NEW TABLES
-- =====================================================
CREATE TRIGGER update_contracts_updated_at BEFORE UPDATE ON contracts
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_certificates_updated_at BEFORE UPDATE ON certificates
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_work_permits_updated_at BEFORE UPDATE ON work_permits
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reminders_updated_at BEFORE UPDATE ON reminders
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
VALUES (2, 'Complete rebuild: Added user_type, contracts, certificates, work_permits, reminders tables')
ON CONFLICT (version) DO UPDATE SET description = EXCLUDED.description;

-- =====================================================
-- END OF SCHEMA
-- =====================================================

