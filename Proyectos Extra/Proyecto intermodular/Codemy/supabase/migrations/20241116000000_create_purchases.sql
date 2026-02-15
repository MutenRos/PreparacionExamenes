-- Tabla para almacenar las compras y suscripciones
CREATE TABLE IF NOT EXISTS purchases (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  
  -- Tipo de compra
  type text NOT NULL CHECK (type IN ('subscription', 'product')),
  
  -- Para suscripciones (starter, pro, family)
  plan_id text,
  billing_period text CHECK (billing_period IN ('monthly', 'yearly')),
  
  -- Para productos individuales (skill trees)
  product_id text,
  
  -- Datos de PayPal
  paypal_transaction_id text UNIQUE,
  paypal_payer_email text,
  paypal_payer_id text,
  
  -- Detalles financieros
  amount decimal(10, 2) NOT NULL,
  currency text DEFAULT 'EUR',
  
  -- Estado del pago
  status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed', 'refunded', 'cancelled')),
  
  -- Fechas
  created_at timestamptz DEFAULT now(),
  completed_at timestamptz,
  expires_at timestamptz, -- Para suscripciones
  
  -- Metadata adicional
  metadata jsonb DEFAULT '{}'::jsonb,
  
  created_at_utc timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Índices para búsquedas rápidas
CREATE INDEX idx_purchases_user_id ON purchases(user_id);
CREATE INDEX idx_purchases_status ON purchases(status);
CREATE INDEX idx_purchases_type ON purchases(type);
CREATE INDEX idx_purchases_paypal_transaction_id ON purchases(paypal_transaction_id);
CREATE INDEX idx_purchases_expires_at ON purchases(expires_at) WHERE expires_at IS NOT NULL;

-- Función para verificar si un usuario tiene acceso activo a un plan
CREATE OR REPLACE FUNCTION has_active_subscription(p_user_id uuid, p_plan_id text DEFAULT NULL)
RETURNS boolean AS $$
BEGIN
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

-- Función para verificar si un usuario tiene acceso a un producto
CREATE OR REPLACE FUNCTION has_product_access(p_user_id uuid, p_product_id text)
RETURNS boolean AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM purchases
    WHERE user_id = p_user_id
      AND type = 'product'
      AND status = 'completed'
      AND product_id = p_product_id
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Función para obtener la suscripción activa de un usuario
CREATE OR REPLACE FUNCTION get_active_subscription(p_user_id uuid)
RETURNS TABLE (
  plan_id text,
  billing_period text,
  expires_at timestamptz,
  created_at timestamptz
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    p.plan_id,
    p.billing_period,
    p.expires_at,
    p.created_at
  FROM purchases p
  WHERE p.user_id = p_user_id
    AND p.type = 'subscription'
    AND p.status = 'completed'
    AND (p.expires_at IS NULL OR p.expires_at > now())
  ORDER BY p.created_at DESC
  LIMIT 1;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Función para obtener todos los productos comprados por un usuario
CREATE OR REPLACE FUNCTION get_user_products(p_user_id uuid)
RETURNS TABLE (
  product_id text,
  amount decimal,
  created_at timestamptz
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    p.product_id,
    p.amount,
    p.created_at
  FROM purchases p
  WHERE p.user_id = p_user_id
    AND p.type = 'product'
    AND p.status = 'completed'
  ORDER BY p.created_at DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger para actualizar updated_at
CREATE OR REPLACE FUNCTION update_purchases_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER purchases_updated_at
  BEFORE UPDATE ON purchases
  FOR EACH ROW
  EXECUTE FUNCTION update_purchases_updated_at();

-- RLS Policies
ALTER TABLE purchases ENABLE ROW LEVEL SECURITY;

-- Los usuarios solo pueden ver sus propias compras
CREATE POLICY "Users can view own purchases"
  ON purchases FOR SELECT
  USING (auth.uid() = user_id);

-- Solo el sistema puede insertar compras (vía webhook)
CREATE POLICY "System can insert purchases"
  ON purchases FOR INSERT
  WITH CHECK (true);

-- Solo el sistema puede actualizar compras
CREATE POLICY "System can update purchases"
  ON purchases FOR UPDATE
  USING (true);

-- Comentarios
COMMENT ON TABLE purchases IS 'Almacena todas las compras y suscripciones de usuarios';
COMMENT ON COLUMN purchases.type IS 'Tipo: subscription (planes recurrentes) o product (compra única)';
COMMENT ON COLUMN purchases.status IS 'Estado: pending, completed, failed, refunded, cancelled';
COMMENT ON COLUMN purchases.expires_at IS 'Fecha de expiración para suscripciones (NULL = lifetime)';
