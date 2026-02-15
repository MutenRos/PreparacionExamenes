// Database Types - Generados desde el schema de Supabase

export interface Profile {
  id: string;
  role: 'student' | 'parent' | 'teacher' | 'admin';
  age_group?: 'kids' | 'teens' | 'adults';
  parent_id?: string;
  display_name?: string;
  avatar_url?: string;
  country_code?: string;
  language_code?: string;
  timezone?: string;
  created_at: string;
  updated_at: string;
}

export interface UserPreferences {
  user_id: string;
  theme: 'light' | 'dark' | 'system';
  notifications_enabled: boolean;
  email_digest: boolean;
  session_time_limit?: number;
  difficulty_preference: 'easy' | 'medium' | 'hard' | 'adaptive';
  preferred_languages: string[];
  created_at: string;
  updated_at: string;
}

export interface Concept {
  id: string;
  slug: string;
  title: Record<string, string>; // {es: "Variables", en: "Variables"}
  description: Record<string, string>;
  level: number; // 0-5
  track: 'fundamentals' | 'web' | 'data' | 'games' | 'mobile' | 'devops';
  prerequisites: string[];
  estimated_minutes: number;
  difficulty_score: number;
  created_at: string;
  updated_at: string;
}

export interface ConceptBinding {
  id: string;
  concept_id: string;
  language: string;
  version: string;
  lesson_content: string;
  starter_code?: string;
  solution_code?: string;
  hints: string[];
  created_at: string;
}

export interface Exercise {
  id: string;
  concept_id: string;
  title: Record<string, string>;
  description: Record<string, string>;
  difficulty: number; // 1-5
  points: number;
  time_limit_seconds: number;
  memory_limit_mb: number;
  created_at: string;
}

export interface ExerciseBinding {
  id: string;
  exercise_id: string;
  language: string;
  template_code: string;
  test_cases: string; // JSON
  test_framework: string;
  runner_image: string;
  created_at: string;
}

export interface ConceptProgress {
  user_id: string;
  concept_id: string;
  language: string;
  status: 'not_started' | 'in_progress' | 'completed' | 'mastered';
  score: number;
  time_spent_minutes: number;
  attempts: number;
  first_completed_at?: string;
  last_activity_at: string;
}

export interface Submission {
  id: string;
  user_id: string;
  exercise_id: string;
  language: string;
  code: string;
  status: 'pending' | 'running' | 'passed' | 'failed' | 'timeout' | 'error';
  score: number;
  execution_time_ms?: number;
  memory_used_mb?: number;
  test_results?: Record<string, any>;
  feedback?: Record<string, any>;
  created_at: string;
}

export interface UserXP {
  user_id: string;
  total_xp: number;
  level: number;
  xp_in_level: number;
  streak_days: number;
  longest_streak: number;
  last_activity_date?: string;
  created_at: string;
  updated_at: string;
}

export interface Badge {
  id: string;
  slug: string;
  name: Record<string, string>;
  description: Record<string, string>;
  icon: string;
  criteria: Record<string, any>;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
  category: 'general' | 'language' | 'streak' | 'achievement' | 'social';
  is_active: boolean;
  created_at: string;
}

export interface UserBadge {
  user_id: string;
  badge_id: string;
  earned_at: string;
  progress?: Record<string, any>;
}

export interface Challenge {
  id: string;
  title: Record<string, string>;
  description: Record<string, string>;
  type: 'coding' | 'streak' | 'social' | 'learning';
  difficulty: 'easy' | 'medium' | 'hard';
  xp_reward: number;
  start_date: string;
  end_date: string;
  max_participants?: number;
  criteria: Record<string, any>;
  is_active: boolean;
  created_at: string;
}

export interface ChallengeParticipation {
  user_id: string;
  challenge_id: string;
  status: 'registered' | 'in_progress' | 'completed' | 'failed';
  progress: Record<string, any>;
  score: number;
  completed_at?: string;
  created_at: string;
}

export interface Subscription {
  id: string;
  user_id: string;
  stripe_customer_id?: string;
  stripe_subscription_id?: string;
  plan_id: string;
  status: 'trial' | 'active' | 'canceled' | 'past_due' | 'unpaid';
  current_period_start?: string;
  current_period_end?: string;
  trial_end?: string;
  created_at: string;
  updated_at: string;
}

export interface SubscriptionPlan {
  id: string;
  name: Record<string, string>;
  description: Record<string, string>;
  price_monthly: number;
  price_yearly?: number;
  features: Record<string, any>;
  max_students?: number;
  is_active: boolean;
  created_at: string;
}

export interface UserEvent {
  id: string;
  user_id: string;
  event_type: string;
  event_data: Record<string, any>;
  session_id?: string;
  ip_address?: string;
  user_agent?: string;
  created_at: string;
}

export interface DailyMetrics {
  date: string;
  user_id: string;
  time_spent_minutes: number;
  exercises_completed: number;
  concepts_learned: number;
  xp_earned: number;
}

// Helper types
export type Language = 'python' | 'javascript' | 'csharp' | 'java' | 'cpp' | 'rust' | 'go';
export type Track = Concept['track'];
export type UserRole = Profile['role'];
export type SubmissionStatus = Submission['status'];
export type PlanId = 'starter' | 'pro' | 'family';