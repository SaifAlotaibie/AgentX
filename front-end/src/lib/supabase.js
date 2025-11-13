/**
 * Supabase client for frontend (Future use).
 * 
 * Currently not actively used in the app, but ready for:
 * - Direct data queries from frontend
 * - Real-time subscriptions
 * - User authentication
 * - Analytics dashboard
 */

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

// Create Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey);

/**
 * Helper function to fetch user's conversation history
 * @param {string} userId - User ID
 * @param {number} limit - Number of messages to fetch
 * @returns {Promise<Array>} - Array of conversation messages
 */
export async function getUserConversations(userId, limit = 50) {
  const { data, error } = await supabase
    .from('conversations')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false })
    .limit(limit);
  
  if (error) {
    console.error('Error fetching conversations:', error);
    return [];
  }
  
  return data;
}

/**
 * Helper function to fetch user's resumes
 * @param {string} userId - User ID
 * @returns {Promise<Array>} - Array of resumes
 */
export async function getUserResumes(userId) {
  const { data, error } = await supabase
    .from('resumes')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });
  
  if (error) {
    console.error('Error fetching resumes:', error);
    return [];
  }
  
  return data;
}

/**
 * Helper function to fetch user's tickets
 * @param {string} userId - User ID
 * @returns {Promise<Array>} - Array of tickets
 */
export async function getUserTickets(userId) {
  const { data, error } = await supabase
    .from('tickets')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });
  
  if (error) {
    console.error('Error fetching tickets:', error);
    return [];
  }
  
  return data;
}

/**
 * Subscribe to real-time conversation updates
 * @param {string} userId - User ID
 * @param {Function} callback - Callback function to handle new messages
 * @returns {Object} - Subscription object
 */
export function subscribeToConversations(userId, callback) {
  return supabase
    .channel(`conversations:${userId}`)
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'public',
        table: 'conversations',
        filter: `user_id=eq.${userId}`
      },
      callback
    )
    .subscribe();
}

/**
 * Get user analytics data
 * @param {string} userId - User ID
 * @returns {Promise<Object>} - Analytics object
 */
export async function getUserAnalytics(userId) {
  try {
    const [conversations, tickets, resumes, toolCalls] = await Promise.all([
      supabase.from('conversations').select('*', { count: 'exact', head: true }).eq('user_id', userId),
      supabase.from('tickets').select('*', { count: 'exact', head: true }).eq('user_id', userId),
      supabase.from('resumes').select('*', { count: 'exact', head: true }).eq('user_id', userId),
      supabase.from('tool_calls').select('*', { count: 'exact', head: true }).eq('user_id', userId),
    ]);

    return {
      totalMessages: conversations.count || 0,
      totalTickets: tickets.count || 0,
      totalResumes: resumes.count || 0,
      totalToolCalls: toolCalls.count || 0,
    };
  } catch (error) {
    console.error('Error fetching analytics:', error);
    return {
      totalMessages: 0,
      totalTickets: 0,
      totalResumes: 0,
      totalToolCalls: 0,
    };
  }
}

export default supabase;

