-- =============================================
-- CodeAcademy Database Schema
-- MVP AAA - Academia completa de programación
-- =============================================

-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================
-- CORE TABLES - Usuarios y Autenticación
-- =============================================

-- Perfiles de usuario (extiende auth.users de Supabase)
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  role TEXT NOT NULL DEFAULT 'student' CHECK (role IN ('student', 'parent', 'teacher', 'admin')),
  age_group TEXT CHECK (age_group IN ('kids', 'teens', 'adults')),
  parent_id UUID REFERENCES profiles(id),
  display_name TEXT,
  avatar_url TEXT,
  country_code TEXT DEFAULT 'ES',
  language_code TEXT DEFAULT 'es',
  timezone TEXT DEFAULT 'Europe/Madrid',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Configuraciones de usuario
CREATE TABLE user_preferences (
  user_id UUID REFERENCES profiles(id) PRIMARY KEY,
  theme TEXT DEFAULT 'system' CHECK (theme IN ('light', 'dark', 'system')),
  notifications_enabled BOOLEAN DEFAULT true,
  email_digest BOOLEAN DEFAULT true,
  session_time_limit INTEGER, -- minutos para kids/teens
  difficulty_preference TEXT DEFAULT 'adaptive' CHECK (difficulty_preference IN ('easy', 'medium', 'hard', 'adaptive')),
  preferred_languages TEXT[] DEFAULT ARRAY['python', 'javascript'],
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- CURRICULUM - Sistema Modular
-- =============================================

-- Conceptos agnósticos de programación
CREATE TABLE concepts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  slug TEXT UNIQUE NOT NULL,
  title JSONB NOT NULL, -- {es: "Variables", en: "Variables"}
  description JSONB NOT NULL,
  level INTEGER NOT NULL CHECK (level >= 0 AND level <= 5),
  track TEXT NOT NULL, -- "fundamentals", "web", "data", "games", "mobile", "devops"
  prerequisites UUID[] DEFAULT '{}',
  estimated_minutes INTEGER DEFAULT 30,
  difficulty_score DECIMAL(3,2) DEFAULT 1.0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Bindings de conceptos por lenguaje
CREATE TABLE concept_bindings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  concept_id UUID REFERENCES concepts(id) ON DELETE CASCADE,
  language TEXT NOT NULL, -- "python", "javascript", "csharp"
  version TEXT NOT NULL DEFAULT 'latest',
  lesson_content TEXT NOT NULL, -- Markdown del contenido
  starter_code TEXT,
  solution_code TEXT,
  hints JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(concept_id, language, version)
);

-- Ejercicios por concepto
CREATE TABLE exercises (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  concept_id UUID REFERENCES concepts(id) ON DELETE CASCADE,
  title JSONB NOT NULL,
  description JSONB NOT NULL,
  difficulty INTEGER DEFAULT 1 CHECK (difficulty >= 1 AND difficulty <= 5),
  points INTEGER DEFAULT 10,
  time_limit_seconds INTEGER DEFAULT 300,
  memory_limit_mb INTEGER DEFAULT 128,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Bindings de ejercicios por lenguaje  
CREATE TABLE exercise_bindings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  exercise_id UUID REFERENCES exercises(id) ON DELETE CASCADE,
  language TEXT NOT NULL,
  template_code TEXT NOT NULL,
  test_cases TEXT NOT NULL, -- JSON con casos de test
  test_framework TEXT NOT NULL, -- "pytest", "jest", "nunit"
  runner_image TEXT NOT NULL, -- "codeacademy/python:3.12"
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(exercise_id, language)
);

-- =============================================
-- PROGRESO Y EVALUACIÓN
-- =============================================

-- Progreso del usuario en conceptos
CREATE TABLE concept_progress (
  user_id UUID REFERENCES profiles(id),
  concept_id UUID REFERENCES concepts(id),
  language TEXT NOT NULL,
  status TEXT DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed', 'mastered')),
  score INTEGER DEFAULT 0 CHECK (score >= 0 AND score <= 100),
  time_spent_minutes INTEGER DEFAULT 0,
  attempts INTEGER DEFAULT 0,
  first_completed_at TIMESTAMPTZ,
  last_activity_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, concept_id, language)
);

-- Envíos de ejercicios
CREATE TABLE submissions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id),
  exercise_id UUID REFERENCES exercises(id),
  language TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'passed', 'failed', 'timeout', 'error')),
  score INTEGER DEFAULT 0,
  execution_time_ms INTEGER,
  memory_used_mb DECIMAL(5,2),
  test_results JSONB,
  feedback JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- GAMIFICACIÓN
-- =============================================

-- XP y nivel del usuario
CREATE TABLE user_xp (
  user_id UUID REFERENCES profiles(id) PRIMARY KEY,
  total_xp INTEGER DEFAULT 0,
  level INTEGER DEFAULT 1,
  xp_in_level INTEGER DEFAULT 0,
  streak_days INTEGER DEFAULT 0,
  longest_streak INTEGER DEFAULT 0,
  last_activity_date DATE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Definición de badges
CREATE TABLE badges (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  slug TEXT UNIQUE NOT NULL,
  name JSONB NOT NULL,
  description JSONB NOT NULL,
  icon TEXT NOT NULL, -- URL o emoji
  criteria JSONB NOT NULL, -- Condiciones para obtener el badge
  rarity TEXT DEFAULT 'common' CHECK (rarity IN ('common', 'rare', 'epic', 'legendary')),
  category TEXT DEFAULT 'general' CHECK (category IN ('general', 'language', 'streak', 'achievement', 'social')),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Badges obtenidos por usuarios
CREATE TABLE user_badges (
  user_id UUID REFERENCES profiles(id),
  badge_id UUID REFERENCES badges(id),
  earned_at TIMESTAMPTZ DEFAULT NOW(),
  progress JSONB, -- Para badges con progreso
  PRIMARY KEY (user_id, badge_id)
);

-- Retos semanales
CREATE TABLE challenges (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title JSONB NOT NULL,
  description JSONB NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('coding', 'streak', 'social', 'learning')),
  difficulty TEXT DEFAULT 'medium' CHECK (difficulty IN ('easy', 'medium', 'hard')),
  xp_reward INTEGER DEFAULT 100,
  start_date TIMESTAMPTZ NOT NULL,
  end_date TIMESTAMPTZ NOT NULL,
  max_participants INTEGER,
  criteria JSONB NOT NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Participación en retos
CREATE TABLE challenge_participations (
  user_id UUID REFERENCES profiles(id),
  challenge_id UUID REFERENCES challenges(id),
  status TEXT DEFAULT 'registered' CHECK (status IN ('registered', 'in_progress', 'completed', 'failed')),
  progress JSONB DEFAULT '{}',
  score INTEGER DEFAULT 0,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, challenge_id)
);

-- =============================================
-- MONETIZACIÓN
-- =============================================

-- Suscripciones
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id),
  stripe_customer_id TEXT UNIQUE,
  stripe_subscription_id TEXT UNIQUE,
  plan_id TEXT NOT NULL, -- "starter", "pro", "family"
  status TEXT DEFAULT 'trial' CHECK (status IN ('trial', 'active', 'canceled', 'past_due', 'unpaid')),
  current_period_start TIMESTAMPTZ,
  current_period_end TIMESTAMPTZ,
  trial_end TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Planes de suscripción
CREATE TABLE subscription_plans (
  id TEXT PRIMARY KEY,
  name JSONB NOT NULL,
  description JSONB NOT NULL,
  price_monthly INTEGER NOT NULL, -- céntimos
  price_yearly INTEGER, -- céntimos (si hay descuento anual)
  features JSONB NOT NULL,
  max_students INTEGER, -- para plan familiar
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- ANALÍTICAS Y MÉTRICAS
-- =============================================

-- Eventos de actividad del usuario
CREATE TABLE user_events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id),
  event_type TEXT NOT NULL, -- "lesson_start", "exercise_complete", "login", etc.
  event_data JSONB DEFAULT '{}',
  session_id TEXT,
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Métricas agregadas por día
CREATE TABLE daily_metrics (
  date DATE NOT NULL,
  user_id UUID REFERENCES profiles(id),
  time_spent_minutes INTEGER DEFAULT 0,
  exercises_completed INTEGER DEFAULT 0,
  concepts_learned INTEGER DEFAULT 0,
  xp_earned INTEGER DEFAULT 0,
  PRIMARY KEY (date, user_id)
);

-- =============================================
-- ÍNDICES PARA PERFORMANCE
-- =============================================

-- Índices para consultas frecuentes
CREATE INDEX idx_profiles_role ON profiles(role);
CREATE INDEX idx_profiles_age_group ON profiles(age_group);
CREATE INDEX idx_profiles_parent_id ON profiles(parent_id);

CREATE INDEX idx_concepts_track ON concepts(track);
CREATE INDEX idx_concepts_level ON concepts(level);

CREATE INDEX idx_submissions_user_exercise ON submissions(user_id, exercise_id);
CREATE INDEX idx_submissions_status ON submissions(status);
CREATE INDEX idx_submissions_created_at ON submissions(created_at);

CREATE INDEX idx_concept_progress_user ON concept_progress(user_id);
CREATE INDEX idx_concept_progress_status ON concept_progress(status);

CREATE INDEX idx_user_events_user_type ON user_events(user_id, event_type);
CREATE INDEX idx_user_events_created_at ON user_events(created_at);

-- =============================================
-- ROW LEVEL SECURITY (RLS)
-- =============================================

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE concept_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_xp ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_participations ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_metrics ENABLE ROW LEVEL SECURITY;

-- Políticas RLS básicas

-- Los usuarios pueden ver y editar su propio perfil
CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

-- Los padres pueden ver perfiles de sus hijos
CREATE POLICY "Parents can view children profiles" ON profiles
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM profiles 
      WHERE id = auth.uid() 
      AND role = 'parent'
    ) AND parent_id = auth.uid()
  );

-- Los usuarios pueden ver su progreso
CREATE POLICY "Users can view own progress" ON concept_progress
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update own progress" ON concept_progress
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Los usuarios pueden ver sus envíos
CREATE POLICY "Users can view own submissions" ON submissions
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create submissions" ON submissions
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Funciones helper para triggers
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para updated_at
CREATE TRIGGER profiles_updated_at 
    BEFORE UPDATE ON profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER user_preferences_updated_at 
    BEFORE UPDATE ON user_preferences 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();