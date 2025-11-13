// Mock user for testing without authentication
// This allows the system to work with Supabase without real login
export const MOCK_USER = {
  id: 'a1b2c3d4-5678-90ab-cdef-123456789000',  // Valid UUID format
  name: 'زياد الحربي',
  email: 'ziyad.dev@qiwa.test',
  phone: '+966501234567',
  user_type: 'employee',  // Can be: employee, business_owner, service_provider
  establishment_id: 'EST12345'  // For business owner testing
};

