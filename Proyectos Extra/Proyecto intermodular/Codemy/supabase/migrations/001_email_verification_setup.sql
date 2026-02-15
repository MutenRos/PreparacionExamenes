-- =============================================
-- Configuración de Políticas y Tablas para Email Verification
-- CodeAcademy - Supabase Setup
-- =============================================

-- Habilitar extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================
-- 1. TABLA DE PERFILES DE USUARIO
-- =============================================

-- Crear tabla de perfiles si no existe
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  role TEXT DEFAULT 'student' CHECK (role IN ('student', 'teacher', 'admin')),
  avatar_url TEXT,
  bio TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Campos de progreso
  total_xp INTEGER DEFAULT 0,
  level INTEGER DEFAULT 1,
  streak_days INTEGER DEFAULT 0,
  last_activity_at TIMESTAMP WITH TIME ZONE,
  
  -- Verificación
  email_verified BOOLEAN DEFAULT FALSE,
  email_verified_at TIMESTAMP WITH TIME ZONE
);

-- Índices para mejor performance
CREATE INDEX IF NOT EXISTS idx_profiles_email ON public.profiles(email);
CREATE INDEX IF NOT EXISTS idx_profiles_role ON public.profiles(role);
CREATE INDEX IF NOT EXISTS idx_profiles_created_at ON public.profiles(created_at DESC);

-- =============================================
-- 2. ROW LEVEL SECURITY (RLS)
-- =============================================

-- Habilitar RLS en la tabla profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Los usuarios pueden ver todos los perfiles públicos
CREATE POLICY "Profiles are viewable by everyone"
  ON public.profiles FOR SELECT
  USING (true);

-- Policy: Los usuarios solo pueden actualizar su propio perfil
CREATE POLICY "Users can update own profile"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Policy: Los usuarios pueden insertar su propio perfil
CREATE POLICY "Users can insert own profile"
  ON public.profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- Policy: Solo admins pueden eliminar perfiles
CREATE POLICY "Only admins can delete profiles"
  ON public.profiles FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- =============================================
-- 3. FUNCIÓN PARA CREAR PERFIL AUTOMÁTICAMENTE
-- =============================================

-- Función que se ejecuta cuando un usuario se registra
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, name, role, email_verified, email_verified_at)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'name', split_part(NEW.email, '@', 1)),
    COALESCE(NEW.raw_user_meta_data->>'role', 'student'),
    CASE WHEN NEW.email_confirmed_at IS NOT NULL THEN TRUE ELSE FALSE END,
    NEW.email_confirmed_at
  )
  ON CONFLICT (id) DO UPDATE
  SET 
    email_verified = CASE WHEN NEW.email_confirmed_at IS NOT NULL THEN TRUE ELSE FALSE END,
    email_verified_at = NEW.email_confirmed_at,
    updated_at = NOW();
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger que ejecuta la función cuando se crea/actualiza un usuario
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT OR UPDATE ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- =============================================
-- 4. FUNCIÓN PARA ACTUALIZAR updated_at
-- =============================================

CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar updated_at automáticamente
DROP TRIGGER IF EXISTS handle_profiles_updated_at ON public.profiles;
CREATE TRIGGER handle_profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_updated_at();

-- =============================================
-- 5. VISTAS ÚTILES
-- =============================================

-- Vista para obtener estadísticas de verificación
CREATE OR REPLACE VIEW public.email_verification_stats AS
SELECT
  COUNT(*) as total_users,
  COUNT(CASE WHEN email_verified THEN 1 END) as verified_users,
  COUNT(CASE WHEN NOT email_verified THEN 1 END) as unverified_users,
  ROUND(
    (COUNT(CASE WHEN email_verified THEN 1 END)::numeric / NULLIF(COUNT(*)::numeric, 0)) * 100,
    2
  ) as verification_rate_percent
FROM public.profiles;

-- =============================================
-- 6. FUNCIONES DE UTILIDAD
-- =============================================

-- Función para obtener perfil completo del usuario actual
CREATE OR REPLACE FUNCTION public.get_current_user_profile()
RETURNS TABLE (
  id UUID,
  email TEXT,
  name TEXT,
  role TEXT,
  avatar_url TEXT,
  bio TEXT,
  total_xp INTEGER,
  level INTEGER,
  streak_days INTEGER,
  email_verified BOOLEAN,
  email_verified_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    p.id,
    p.email,
    p.name,
    p.role,
    p.avatar_url,
    p.bio,
    p.total_xp,
    p.level,
    p.streak_days,
    p.email_verified,
    p.email_verified_at,
    p.created_at
  FROM public.profiles p
  WHERE p.id = auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Función para verificar si un email ya está registrado
CREATE OR REPLACE FUNCTION public.is_email_taken(check_email TEXT)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM public.profiles WHERE email = check_email
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =============================================
-- 7. GRANTS Y PERMISOS
-- =============================================

-- Dar permisos de lectura a usuarios autenticados
GRANT SELECT ON public.profiles TO authenticated;
GRANT SELECT ON public.profiles TO anon;

-- Permitir operaciones en su propio perfil
GRANT UPDATE ON public.profiles TO authenticated;
GRANT INSERT ON public.profiles TO authenticated;

-- Permitir uso de funciones
GRANT EXECUTE ON FUNCTION public.get_current_user_profile() TO authenticated;
GRANT EXECUTE ON FUNCTION public.is_email_taken(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.is_email_taken(TEXT) TO anon;

-- =============================================
-- 8. DATOS INICIALES (OPCIONAL)
-- =============================================

-- Insertar un usuario admin de ejemplo (comentado por seguridad)
-- Recuerda crear este usuario primero desde Supabase Dashboard
/*
INSERT INTO public.profiles (id, email, name, role, email_verified)
VALUES (
  'tu-uuid-aqui',
  'admin@codeacademy.com',
  'Admin',
  'admin',
  TRUE
)
ON CONFLICT (id) DO NOTHING;
*/

-- =============================================
-- 9. VERIFICACIÓN
-- =============================================

-- Verificar que todo está configurado correctamente
DO $$
BEGIN
  -- Verificar tabla
  IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'profiles') THEN
    RAISE NOTICE '✅ Tabla profiles creada correctamente';
  ELSE
    RAISE EXCEPTION '❌ Error: Tabla profiles no existe';
  END IF;
  
  -- Verificar RLS
  IF EXISTS (
    SELECT 1 FROM pg_tables 
    WHERE schemaname = 'public' 
    AND tablename = 'profiles' 
    AND rowsecurity = true
  ) THEN
    RAISE NOTICE '✅ RLS habilitado en profiles';
  ELSE
    RAISE WARNING '⚠️  RLS no está habilitado en profiles';
  END IF;
  
  -- Verificar trigger
  IF EXISTS (
    SELECT 1 FROM pg_trigger 
    WHERE tgname = 'on_auth_user_created'
  ) THEN
    RAISE NOTICE '✅ Trigger on_auth_user_created configurado';
  ELSE
    RAISE WARNING '⚠️  Trigger on_auth_user_created no existe';
  END IF;
  
  RAISE NOTICE '✅ Configuración completada exitosamente';
END $$;

-- =============================================
-- FIN DE CONFIGURACIÓN
-- =============================================

-- Para ver las estadísticas de verificación:
-- SELECT * FROM public.email_verification_stats;

-- Para ver usuarios no verificados:
-- SELECT email, created_at 
-- FROM public.profiles 
-- WHERE NOT email_verified 
-- ORDER BY created_at DESC;
