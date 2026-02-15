-- ================================================================
-- CODEACADEMY - SCHEMA SUPABASE
-- ================================================================
-- Versión: 1.0
-- Fecha: 12 noviembre 2025
-- Descripción: Esquema de base de datos para migrar de localStorage
--              a Supabase con persistencia en la nube
-- ================================================================

-- ================================================================
-- EXTENSIONES
-- ================================================================

-- UUID para IDs únicos
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ================================================================
-- TABLAS PRINCIPALES
-- ================================================================

-- ----------------------------------------------------------------
-- TABLA: users
-- Descripción: Perfil extendido de usuarios (complementa auth.users)
-- ----------------------------------------------------------------
CREATE TABLE public.users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  display_name TEXT,
  avatar_url TEXT,
  total_xp INTEGER DEFAULT 0,
  current_level INTEGER DEFAULT 1,
  streak_days INTEGER DEFAULT 0,
  last_visit_date DATE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para búsquedas rápidas
CREATE INDEX users_email_idx ON public.users(email);
CREATE INDEX users_level_idx ON public.users(current_level);
CREATE INDEX users_xp_idx ON public.users(total_xp);

-- ----------------------------------------------------------------
-- TABLA: courses
-- Descripción: Catálogo de cursos disponibles
-- ----------------------------------------------------------------
CREATE TABLE public.courses (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  icon TEXT,
  category TEXT,
  difficulty TEXT CHECK (difficulty IN ('foundation', 'intermediate', 'advanced', 'expert')),
  total_lessons INTEGER NOT NULL,
  total_xp INTEGER NOT NULL,
  xp_per_lesson INTEGER DEFAULT 50,
  bonus_xp INTEGER DEFAULT 100,
  prerequisites JSONB DEFAULT '[]'::jsonb,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Datos iniciales de cursos
INSERT INTO public.courses (id, title, description, icon, category, difficulty, total_lessons, total_xp, prerequisites) VALUES
('py-intro', 'Introducción a Python', 'Primeros pasos con Python', '🐍', 'python', 'foundation', 4, 200, '[]'),
('py-variables', 'Variables y Tipos', 'Manejo de datos en Python', '📦', 'python', 'foundation', 5, 250, '["py-intro"]'),
('py-control', 'Estructuras de Control', 'If, else, loops', '🔀', 'python', 'foundation', 6, 300, '["py-variables"]'),
('py-functions', 'Funciones', 'Código reutilizable', '⚡', 'python', 'intermediate', 6, 350, '["py-control"]'),
('py-classes', 'POO', 'Programación Orientada a Objetos', '🏗️', 'python', 'intermediate', 6, 400, '["py-functions"]'),
('py-files', 'Archivos', 'Persistencia de datos', '📁', 'python', 'intermediate', 6, 300, '["py-control"]');

-- ----------------------------------------------------------------
-- TABLA: lessons
-- Descripción: Lecciones individuales de cada curso
-- ----------------------------------------------------------------
CREATE TABLE public.lessons (
  id TEXT PRIMARY KEY,
  course_id TEXT NOT NULL REFERENCES public.courses(id) ON DELETE CASCADE,
  lesson_number INTEGER NOT NULL,
  title TEXT NOT NULL,
  duration TEXT,
  xp INTEGER DEFAULT 50,
  content JSONB,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(course_id, lesson_number)
);

-- Índices
CREATE INDEX lessons_course_id_idx ON public.lessons(course_id);
CREATE INDEX lessons_lesson_number_idx ON public.lessons(lesson_number);

-- ----------------------------------------------------------------
-- TABLA: user_progress
-- Descripción: Progreso de cada usuario en cada lección
-- ----------------------------------------------------------------
CREATE TABLE public.user_progress (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  course_id TEXT NOT NULL REFERENCES public.courses(id) ON DELETE CASCADE,
  lesson_id TEXT NOT NULL REFERENCES public.lessons(id) ON DELETE CASCADE,
  status TEXT CHECK (status IN ('locked', 'available', 'in-progress', 'completed')),
  xp_earned INTEGER DEFAULT 0,
  attempts INTEGER DEFAULT 0,
  last_code TEXT,
  completed_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, lesson_id)
);

-- Índices para consultas frecuentes
CREATE INDEX user_progress_user_id_idx ON public.user_progress(user_id);
CREATE INDEX user_progress_course_id_idx ON public.user_progress(course_id);
CREATE INDEX user_progress_status_idx ON public.user_progress(status);

-- ----------------------------------------------------------------
-- TABLA: user_courses
-- Descripción: Progreso agregado por curso
-- ----------------------------------------------------------------
CREATE TABLE public.user_courses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  course_id TEXT NOT NULL REFERENCES public.courses(id) ON DELETE CASCADE,
  progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
  lessons_completed INTEGER DEFAULT 0,
  status TEXT CHECK (status IN ('locked', 'available', 'in-progress', 'completed')),
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, course_id)
);

-- Índices
CREATE INDEX user_courses_user_id_idx ON public.user_courses(user_id);
CREATE INDEX user_courses_status_idx ON public.user_courses(status);

-- ----------------------------------------------------------------
-- TABLA: achievements
-- Descripción: Catálogo de logros disponibles
-- ----------------------------------------------------------------
CREATE TABLE public.achievements (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  icon TEXT,
  rarity TEXT CHECK (rarity IN ('common', 'rare', 'epic', 'legendary')),
  xp_reward INTEGER DEFAULT 0,
  category TEXT,
  requirement_type TEXT,
  requirement_value INTEGER,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Datos iniciales de logros
INSERT INTO public.achievements (id, title, description, icon, rarity, xp_reward, category, requirement_type, requirement_value) VALUES
('first-steps', 'Primeros Pasos', 'Completa tu primera lección', '⭐', 'common', 50, 'course', 'lessons_completed', 1),
('python-basics', 'Fundamentos de Python', 'Completa el curso de Introducción a Python', '🏆', 'rare', 100, 'course', 'courses_completed', 1),
('level-5', 'Nivel 5 Alcanzado', 'Llega al nivel 5', '📈', 'rare', 150, 'level', 'level_reached', 5),
('level-10', 'Nivel 10 Alcanzado', 'Llega al nivel 10', '🎖️', 'epic', 250, 'level', 'level_reached', 10),
('dedicated-learner', 'Estudiante Dedicado', 'Completa 10 lecciones', '🎯', 'rare', 200, 'course', 'lessons_completed', 10),
('python-master', 'Maestro de Python', 'Completa 3 cursos de Python', '🏆', 'epic', 300, 'course', 'courses_completed', 3),
('xp-hunter', 'Cazador de XP', 'Acumula 1000 XP', '⚡', 'epic', 500, 'special', 'xp_earned', 1000),
('half-way', 'A Medio Camino', 'Completa 15 lecciones', '🎯', 'rare', 300, 'course', 'lessons_completed', 15),
('course-master', 'Maestro de Cursos', 'Completa 5 cursos completos', '🎖️', 'legendary', 500, 'course', 'courses_completed', 5);

-- ----------------------------------------------------------------
-- TABLA: user_achievements
-- Descripción: Logros desbloqueados por cada usuario
-- ----------------------------------------------------------------
CREATE TABLE public.user_achievements (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  achievement_id TEXT NOT NULL REFERENCES public.achievements(id) ON DELETE CASCADE,
  unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, achievement_id)
);

-- Índices
CREATE INDEX user_achievements_user_id_idx ON public.user_achievements(user_id);
CREATE INDEX user_achievements_unlocked_at_idx ON public.user_achievements(unlocked_at);

-- ----------------------------------------------------------------
-- TABLA: notifications
-- Descripción: Notificaciones del sistema para usuarios
-- ----------------------------------------------------------------
CREATE TABLE public.notifications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  type TEXT CHECK (type IN ('achievement', 'level_up', 'course_complete', 'info', 'error')),
  title TEXT NOT NULL,
  message TEXT,
  icon TEXT,
  read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX notifications_user_id_idx ON public.notifications(user_id);
CREATE INDEX notifications_read_idx ON public.notifications(read);
CREATE INDEX notifications_created_at_idx ON public.notifications(created_at DESC);

-- ----------------------------------------------------------------
-- TABLA: xp_history
-- Descripción: Historial de XP ganado (para analytics)
-- ----------------------------------------------------------------
CREATE TABLE public.xp_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  xp_amount INTEGER NOT NULL,
  source TEXT,
  source_id TEXT,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX xp_history_user_id_idx ON public.xp_history(user_id);
CREATE INDEX xp_history_created_at_idx ON public.xp_history(created_at DESC);

-- ================================================================
-- FUNCIONES Y TRIGGERS
-- ================================================================

-- ----------------------------------------------------------------
-- FUNCIÓN: update_updated_at
-- Descripción: Actualiza el campo updated_at automáticamente
-- ----------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a todas las tablas con updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_courses_updated_at BEFORE UPDATE ON public.courses
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_lessons_updated_at BEFORE UPDATE ON public.lessons
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_user_progress_updated_at BEFORE UPDATE ON public.user_progress
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_user_courses_updated_at BEFORE UPDATE ON public.user_courses
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ----------------------------------------------------------------
-- FUNCIÓN: calculate_course_progress
-- Descripción: Calcula el porcentaje de progreso de un curso
-- ----------------------------------------------------------------
CREATE OR REPLACE FUNCTION calculate_course_progress(p_user_id UUID, p_course_id TEXT)
RETURNS INTEGER AS $$
DECLARE
  total_lessons INTEGER;
  completed_lessons INTEGER;
BEGIN
  -- Obtener total de lecciones del curso
  SELECT total_lessons INTO total_lessons
  FROM public.courses
  WHERE id = p_course_id;
  
  -- Contar lecciones completadas por el usuario
  SELECT COUNT(*) INTO completed_lessons
  FROM public.user_progress
  WHERE user_id = p_user_id
    AND course_id = p_course_id
    AND status = 'completed';
  
  -- Calcular porcentaje
  IF total_lessons > 0 THEN
    RETURN (completed_lessons * 100) / total_lessons;
  ELSE
    RETURN 0;
  END IF;
END;
$$ LANGUAGE plpgsql;

-- ----------------------------------------------------------------
-- FUNCIÓN: calculate_total_xp
-- Descripción: Calcula el XP total de un usuario
-- ----------------------------------------------------------------
CREATE OR REPLACE FUNCTION calculate_total_xp(p_user_id UUID)
RETURNS INTEGER AS $$
DECLARE
  total INTEGER;
BEGIN
  SELECT COALESCE(SUM(xp_amount), 0) INTO total
  FROM public.xp_history
  WHERE user_id = p_user_id;
  
  RETURN total;
END;
$$ LANGUAGE plpgsql;

-- ----------------------------------------------------------------
-- FUNCIÓN: calculate_level
-- Descripción: Calcula el nivel basado en XP (100 XP por nivel)
-- ----------------------------------------------------------------
CREATE OR REPLACE FUNCTION calculate_level(p_xp INTEGER)
RETURNS INTEGER AS $$
BEGIN
  RETURN FLOOR(p_xp / 100) + 1;
END;
$$ LANGUAGE plpgsql;

-- ----------------------------------------------------------------
-- FUNCIÓN: update_user_xp_and_level
-- Descripción: Actualiza XP y nivel cuando se gana XP
-- ----------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_user_xp_and_level()
RETURNS TRIGGER AS $$
DECLARE
  new_total_xp INTEGER;
  new_level INTEGER;
  old_level INTEGER;
BEGIN
  -- Calcular nuevo XP total
  new_total_xp := calculate_total_xp(NEW.user_id);
  new_level := calculate_level(new_total_xp);
  
  -- Obtener nivel anterior
  SELECT current_level INTO old_level
  FROM public.users
  WHERE id = NEW.user_id;
  
  -- Actualizar usuario
  UPDATE public.users
  SET total_xp = new_total_xp,
      current_level = new_level
  WHERE id = NEW.user_id;
  
  -- Si subió de nivel, crear notificación
  IF new_level > old_level THEN
    INSERT INTO public.notifications (user_id, type, title, message, icon)
    VALUES (
      NEW.user_id,
      'level_up',
      '¡Subiste de Nivel!',
      'Alcanzaste el nivel ' || new_level::TEXT,
      '🎉'
    );
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar XP automáticamente
CREATE TRIGGER update_user_xp_on_history_insert
AFTER INSERT ON public.xp_history
FOR EACH ROW EXECUTE FUNCTION update_user_xp_and_level();

-- ----------------------------------------------------------------
-- FUNCIÓN: complete_lesson
-- Descripción: Marca una lección como completada y otorga XP
-- ----------------------------------------------------------------
CREATE OR REPLACE FUNCTION complete_lesson(
  p_user_id UUID,
  p_course_id TEXT,
  p_lesson_id TEXT,
  p_code TEXT DEFAULT NULL
)
RETURNS JSON AS $$
DECLARE
  lesson_xp INTEGER;
  result JSON;
BEGIN
  -- Obtener XP de la lección
  SELECT xp INTO lesson_xp
  FROM public.lessons
  WHERE id = p_lesson_id;
  
  -- Actualizar progreso de la lección
  INSERT INTO public.user_progress (user_id, course_id, lesson_id, status, xp_earned, last_code, completed_at)
  VALUES (p_user_id, p_course_id, p_lesson_id, 'completed', lesson_xp, p_code, NOW())
  ON CONFLICT (user_id, lesson_id)
  DO UPDATE SET
    status = 'completed',
    xp_earned = EXCLUDED.xp_earned,
    last_code = EXCLUDED.last_code,
    completed_at = EXCLUDED.completed_at,
    attempts = public.user_progress.attempts + 1;
  
  -- Registrar XP ganado
  INSERT INTO public.xp_history (user_id, xp_amount, source, source_id, description)
  VALUES (p_user_id, lesson_xp, 'lesson', p_lesson_id, 'Completó lección ' || p_lesson_id);
  
  -- Actualizar progreso del curso
  INSERT INTO public.user_courses (user_id, course_id, progress_percentage, lessons_completed, status, started_at)
  VALUES (
    p_user_id,
    p_course_id,
    calculate_course_progress(p_user_id, p_course_id),
    1,
    'in-progress',
    NOW()
  )
  ON CONFLICT (user_id, course_id)
  DO UPDATE SET
    progress_percentage = calculate_course_progress(p_user_id, p_course_id),
    lessons_completed = public.user_courses.lessons_completed + 1,
    status = CASE
      WHEN calculate_course_progress(p_user_id, p_course_id) = 100 THEN 'completed'
      ELSE 'in-progress'
    END,
    completed_at = CASE
      WHEN calculate_course_progress(p_user_id, p_course_id) = 100 THEN NOW()
      ELSE NULL
    END;
  
  -- Retornar resultado
  SELECT json_build_object(
    'success', TRUE,
    'xp_earned', lesson_xp,
    'new_total_xp', calculate_total_xp(p_user_id),
    'new_level', calculate_level(calculate_total_xp(p_user_id))
  ) INTO result;
  
  RETURN result;
END;
$$ LANGUAGE plpgsql;

-- ================================================================
-- ROW LEVEL SECURITY (RLS)
-- ================================================================

-- Habilitar RLS en todas las tablas
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.xp_history ENABLE ROW LEVEL SECURITY;

-- Políticas para users
CREATE POLICY "Users can view own profile"
  ON public.users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON public.users FOR UPDATE
  USING (auth.uid() = id);

-- Políticas para user_progress
CREATE POLICY "Users can view own progress"
  ON public.user_progress FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own progress"
  ON public.user_progress FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own progress"
  ON public.user_progress FOR UPDATE
  USING (auth.uid() = user_id);

-- Políticas para user_courses
CREATE POLICY "Users can view own courses"
  ON public.user_courses FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own courses"
  ON public.user_courses FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own courses"
  ON public.user_courses FOR UPDATE
  USING (auth.uid() = user_id);

-- Políticas para achievements
CREATE POLICY "Users can view own achievements"
  ON public.user_achievements FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own achievements"
  ON public.user_achievements FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Políticas para notifications
CREATE POLICY "Users can view own notifications"
  ON public.notifications FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update own notifications"
  ON public.notifications FOR UPDATE
  USING (auth.uid() = user_id);

-- Políticas para xp_history
CREATE POLICY "Users can view own xp history"
  ON public.xp_history FOR SELECT
  USING (auth.uid() = user_id);

-- Permitir lectura pública de cursos, lecciones y achievements
CREATE POLICY "Public read access to courses"
  ON public.courses FOR SELECT
  TO public
  USING (TRUE);

CREATE POLICY "Public read access to lessons"
  ON public.lessons FOR SELECT
  TO public
  USING (TRUE);

CREATE POLICY "Public read access to achievements catalog"
  ON public.achievements FOR SELECT
  TO public
  USING (TRUE);

-- ================================================================
-- VISTAS
-- ================================================================

-- ----------------------------------------------------------------
-- VISTA: user_dashboard
-- Descripción: Vista consolidada del dashboard del usuario
-- ----------------------------------------------------------------
CREATE OR REPLACE VIEW user_dashboard AS
SELECT
  u.id as user_id,
  u.display_name,
  u.total_xp,
  u.current_level,
  u.streak_days,
  (SELECT COUNT(*) FROM public.user_progress WHERE user_id = u.id AND status = 'completed') as lessons_completed,
  (SELECT COUNT(*) FROM public.user_courses WHERE user_id = u.id AND status = 'completed') as courses_completed,
  (SELECT COUNT(*) FROM public.user_achievements WHERE user_id = u.id) as achievements_unlocked,
  (SELECT COUNT(*) FROM public.notifications WHERE user_id = u.id AND read = FALSE) as unread_notifications
FROM public.users u;

-- ================================================================
-- COMENTARIOS
-- ================================================================

COMMENT ON TABLE public.users IS 'Perfil extendido de usuarios';
COMMENT ON TABLE public.courses IS 'Catálogo de cursos disponibles';
COMMENT ON TABLE public.lessons IS 'Lecciones individuales de cada curso';
COMMENT ON TABLE public.user_progress IS 'Progreso de usuarios en lecciones';
COMMENT ON TABLE public.user_courses IS 'Progreso agregado por curso';
COMMENT ON TABLE public.achievements IS 'Catálogo de logros';
COMMENT ON TABLE public.user_achievements IS 'Logros desbloqueados por usuarios';
COMMENT ON TABLE public.notifications IS 'Notificaciones del sistema';
COMMENT ON TABLE public.xp_history IS 'Historial de XP ganado';

-- ================================================================
-- FIN DEL SCHEMA
-- ================================================================
