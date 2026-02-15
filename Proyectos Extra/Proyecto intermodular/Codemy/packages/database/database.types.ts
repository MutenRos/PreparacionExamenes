export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string
          role: 'student' | 'parent' | 'teacher' | 'admin'
          age_group: 'kids' | 'teens' | 'adults' | null
          parent_id: string | null
          display_name: string | null
          avatar_url: string | null
          country_code: string | null
          language_code: string | null
          timezone: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id: string
          role?: 'student' | 'parent' | 'teacher' | 'admin'
          age_group?: 'kids' | 'teens' | 'adults' | null
          parent_id?: string | null
          display_name?: string | null
          avatar_url?: string | null
          country_code?: string | null
          language_code?: string | null
          timezone?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          role?: 'student' | 'parent' | 'teacher' | 'admin'
          age_group?: 'kids' | 'teens' | 'adults' | null
          parent_id?: string | null
          display_name?: string | null
          avatar_url?: string | null
          country_code?: string | null
          language_code?: string | null
          timezone?: string | null
          created_at?: string
          updated_at?: string
        }
      }
      concept_progress: {
        Row: {
          user_id: string
          concept_id: string
          language: string
          status: 'not_started' | 'in_progress' | 'completed' | 'mastered'
          score: number
          time_spent_minutes: number
          attempts: number
          first_completed_at: string | null
          last_activity_at: string
        }
        Insert: {
          user_id: string
          concept_id: string
          language: string
          status?: 'not_started' | 'in_progress' | 'completed' | 'mastered'
          score?: number
          time_spent_minutes?: number
          attempts?: number
          first_completed_at?: string | null
          last_activity_at?: string
        }
        Update: {
          user_id?: string
          concept_id?: string
          language?: string
          status?: 'not_started' | 'in_progress' | 'completed' | 'mastered'
          score?: number
          time_spent_minutes?: number
          attempts?: number
          first_completed_at?: string | null
          last_activity_at?: string
        }
      }
      submissions: {
        Row: {
          id: string
          user_id: string
          exercise_id: string
          language: string
          code: string
          status: 'pending' | 'running' | 'passed' | 'failed' | 'timeout' | 'error'
          score: number
          execution_time_ms: number | null
          memory_used_mb: number | null
          test_results: any | null
          feedback: any | null
          created_at: string
        }
        Insert: {
          id?: string
          user_id: string
          exercise_id: string
          language: string
          code: string
          status?: 'pending' | 'running' | 'passed' | 'failed' | 'timeout' | 'error'
          score?: number
          execution_time_ms?: number | null
          memory_used_mb?: number | null
          test_results?: any | null
          feedback?: any | null
          created_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          exercise_id?: string
          language?: string
          code?: string
          status?: 'pending' | 'running' | 'passed' | 'failed' | 'timeout' | 'error'
          score?: number
          execution_time_ms?: number | null
          memory_used_mb?: number | null
          test_results?: any | null
          feedback?: any | null
          created_at?: string
        }
      }
      user_xp: {
        Row: {
          user_id: string
          total_xp: number
          level: number
          xp_in_level: number
          streak_days: number
          longest_streak: number
          last_activity_date: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          user_id: string
          total_xp?: number
          level?: number
          xp_in_level?: number
          streak_days?: number
          longest_streak?: number
          last_activity_date?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          user_id?: string
          total_xp?: number
          level?: number
          xp_in_level?: number
          streak_days?: number
          longest_streak?: number
          last_activity_date?: string | null
          created_at?: string
          updated_at?: string
        }
      }
      user_events: {
        Row: {
          id: string
          user_id: string
          event_type: string
          event_data: any
          session_id: string | null
          ip_address: string | null
          user_agent: string | null
          created_at: string
        }
        Insert: {
          id?: string
          user_id: string
          event_type: string
          event_data?: any
          session_id?: string | null
          ip_address?: string | null
          user_agent?: string | null
          created_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          event_type?: string
          event_data?: any
          session_id?: string | null
          ip_address?: string | null
          user_agent?: string | null
          created_at?: string
        }
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
  }
}