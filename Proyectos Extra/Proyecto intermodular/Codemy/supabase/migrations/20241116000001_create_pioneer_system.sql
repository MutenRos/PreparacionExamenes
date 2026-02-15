-- Sistema de Usuarios Pioneros (Primeras 100 cuentas con acceso de por vida)
-- 
-- Las primeras 100 personas que se registren obtienen acceso completo GRATIS de por vida

-- Tabla para rastrear usuarios pioneros
CREATE TABLE IF NOT EXISTS pioneer_users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
  pioneer_number int NOT NULL UNIQUE CHECK (pioneer_number BETWEEN 1 AND 100),
  granted_at timestamptz DEFAULT now(),
  is_active boolean DEFAULT true,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now()
);

-- Índices
CREATE INDEX idx_pioneer_users_user_id ON pioneer_users(user_id);
CREATE INDEX idx_pioneer_users_pioneer_number ON pioneer_users(pioneer_number);
CREATE INDEX idx_pioneer_users_granted_at ON pioneer_users(granted_at);

-- Tabla de configuración del sistema pionero
CREATE TABLE IF NOT EXISTS pioneer_config (
  id int PRIMARY KEY DEFAULT 1,
  total_slots int DEFAULT 100,
  slots_remaining int DEFAULT 100,
  is_active boolean DEFAULT true,
  started_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  CONSTRAINT single_config CHECK (id = 1)
);

-- Insertar configuración inicial
INSERT INTO pioneer_config (id, total_slots, slots_remaining, is_active)
VALUES (1, 100, 100, true)
ON CONFLICT (id) DO NOTHING;

-- Función para obtener slots disponibles
CREATE OR REPLACE FUNCTION get_pioneer_slots_remaining()
RETURNS int AS $$
BEGIN
  RETURN (SELECT slots_remaining FROM pioneer_config WHERE id = 1);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Función para asignar status pionero a un usuario
CREATE OR REPLACE FUNCTION assign_pioneer_status(p_user_id uuid)
RETURNS TABLE (
  success boolean,
  pioneer_number int,
  message text
) AS $$
DECLARE
  v_slots_remaining int;
  v_next_number int;
  v_config_active boolean;
BEGIN
  -- Verificar si el programa pionero está activo
  SELECT is_active INTO v_config_active FROM pioneer_config WHERE id = 1;
  
  IF NOT v_config_active THEN
    RETURN QUERY SELECT false, NULL::int, 'Programa pionero no activo'::text;
    RETURN;
  END IF;

  -- Verificar si el usuario ya es pionero
  IF EXISTS (SELECT 1 FROM pioneer_users WHERE user_id = p_user_id) THEN
    SELECT pioneer_number INTO v_next_number FROM pioneer_users WHERE user_id = p_user_id;
    RETURN QUERY SELECT true, v_next_number, 'Usuario ya es pionero'::text;
    RETURN;
  END IF;

  -- Obtener slots disponibles con lock
  SELECT slots_remaining INTO v_slots_remaining 
  FROM pioneer_config 
  WHERE id = 1 
  FOR UPDATE;

  -- Verificar si quedan slots
  IF v_slots_remaining <= 0 THEN
    RETURN QUERY SELECT false, NULL::int, 'No quedan slots pioneros disponibles'::text;
    RETURN;
  END IF;

  -- Calcular siguiente número pionero
  v_next_number := (SELECT total_slots FROM pioneer_config WHERE id = 1) - v_slots_remaining + 1;

  -- Insertar usuario pionero
  INSERT INTO pioneer_users (user_id, pioneer_number)
  VALUES (p_user_id, v_next_number);

  -- Decrementar slots disponibles
  UPDATE pioneer_config 
  SET slots_remaining = slots_remaining - 1,
      updated_at = now()
  WHERE id = 1;

  RETURN QUERY SELECT true, v_next_number, 'Status pionero asignado exitosamente'::text;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Función para verificar si un usuario es pionero
CREATE OR REPLACE FUNCTION is_pioneer_user(p_user_id uuid)
RETURNS boolean AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM pioneer_users 
    WHERE user_id = p_user_id 
    AND is_active = true
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Función para obtener información del usuario pionero
CREATE OR REPLACE FUNCTION get_pioneer_info(p_user_id uuid)
RETURNS TABLE (
  is_pioneer boolean,
  pioneer_number int,
  granted_at timestamptz
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    true,
    pu.pioneer_number,
    pu.granted_at
  FROM pioneer_users pu
  WHERE pu.user_id = p_user_id
  AND pu.is_active = true;
  
  IF NOT FOUND THEN
    RETURN QUERY SELECT false, NULL::int, NULL::timestamptz;
  END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Actualizar función has_active_subscription para incluir pioneros
CREATE OR REPLACE FUNCTION has_active_subscription(p_user_id uuid, p_plan_id text DEFAULT NULL)
RETURNS boolean AS $$
BEGIN
  -- Primero verificar si es usuario pionero
  IF is_pioneer_user(p_user_id) THEN
    RETURN true;
  END IF;

  -- Verificar suscripción normal
  RETURN EXISTS (
    SELECT 1 FROM purchases
    WHERE user_id = p_user_id
      AND type = 'subscription'
      AND status = 'completed'
      AND (expires_at IS NULL OR expires_at > now())
      AND (p_plan_id IS NULL OR plan_id = p_plan_id)
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger para actualizar updated_at en pioneer_config
CREATE OR REPLACE FUNCTION update_pioneer_config_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER pioneer_config_updated_at
  BEFORE UPDATE ON pioneer_config
  FOR EACH ROW
  EXECUTE FUNCTION update_pioneer_config_updated_at();

-- RLS Policies
ALTER TABLE pioneer_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE pioneer_config ENABLE ROW LEVEL SECURITY;

-- Los usuarios pueden ver su propio status pionero
CREATE POLICY "Users can view own pioneer status"
  ON pioneer_users FOR SELECT
  USING (auth.uid() = user_id);

-- Todos pueden ver el contador de slots disponibles
CREATE POLICY "Anyone can view pioneer config"
  ON pioneer_config FOR SELECT
  USING (true);

-- Solo el sistema puede insertar/actualizar
CREATE POLICY "System can manage pioneer users"
  ON pioneer_users FOR ALL
  USING (true);

CREATE POLICY "System can manage pioneer config"
  ON pioneer_config FOR ALL
  USING (true);

-- Comentarios
COMMENT ON TABLE pioneer_users IS 'Usuarios pioneros - primeras 100 cuentas con acceso de por vida';
COMMENT ON TABLE pioneer_config IS 'Configuración del programa pionero';
COMMENT ON FUNCTION assign_pioneer_status IS 'Asigna status pionero al registrarse (si hay slots)';
COMMENT ON FUNCTION is_pioneer_user IS 'Verifica si un usuario tiene status pionero activo';
COMMENT ON FUNCTION get_pioneer_slots_remaining IS 'Retorna cuántos slots pioneros quedan disponibles';
