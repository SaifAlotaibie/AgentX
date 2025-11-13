-- =====================================================
-- SUPABASE MIGRATION V2 - Complete System Rebuild
-- Run this in Supabase SQL Editor after V1
-- =====================================================

-- =====================================================
-- 1. UPDATE USER_PROFILE TABLE (add user_type)
-- =====================================================
ALTER TABLE user_profile 
ADD COLUMN IF NOT EXISTS user_type TEXT CHECK (user_type IN ('employee', 'business_owner', 'service_provider')) DEFAULT 'employee',
ADD COLUMN IF NOT EXISTS national_id TEXT,
ADD COLUMN IF NOT EXISTS nationality TEXT,
ADD COLUMN IF NOT EXISTS establishment_id TEXT;

CREATE INDEX IF NOT EXISTS idx_user_profile_user_type ON user_profile(user_type);

-- =====================================================
-- 2. CONTRACTS TABLE
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
    renewal_history JSONB,
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
-- 3. CERTIFICATES TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS certificates (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    certificate_id TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL CHECK (type IN ('salary', 'experience')),
    purpose TEXT,
    status TEXT NOT NULL CHECK (status IN ('requested', 'processing', 'ready', 'delivered')) DEFAULT 'requested',
    request_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ready_date TIMESTAMP WITH TIME ZONE,
    document_url TEXT,
    employee_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_certificates_user_id ON certificates(user_id);
CREATE INDEX IF NOT EXISTS idx_certificates_certificate_id ON certificates(certificate_id);
CREATE INDEX IF NOT EXISTS idx_certificates_status ON certificates(status);
CREATE INDEX IF NOT EXISTS idx_certificates_type ON certificates(type);

-- =====================================================
-- 4. WORK PERMITS TABLE
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
-- 5. REMINDERS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS reminders (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    reminder_id TEXT NOT NULL UNIQUE,
    reminder_type TEXT NOT NULL CHECK (reminder_type IN ('contract_expiry', 'permit_expiry', 'certificate_ready', 'custom')),
    related_entity_id TEXT,
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
-- 6. TRIGGERS
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
-- 7. UPDATE SCHEMA VERSION
-- =====================================================
INSERT INTO schema_version (version, description) 
VALUES (2, 'Complete rebuild: Added user_type, contracts, certificates, work_permits, reminders')
ON CONFLICT (version) DO UPDATE SET description = EXCLUDED.description;

-- =====================================================
-- VERIFICATION QUERY
-- =====================================================
-- Run this to verify all tables exist:
-- SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;

-- Should show: certificates, contracts, conversations, process_steps, reminders, 
--              resumes, schema_version, tickets, tool_calls, user_behavior, 
--              user_profile, work_permits

