# 🔧 Guía de Configuración Completa - CodeAcademy

## 📋 Índice
1. [Configurar Supabase](#1-configurar-supabase)
2. [Configurar Stripe](#2-configurar-stripe)
3. [Variables de Entorno](#3-variables-de-entorno)
4. [Iniciar en Producción](#4-iniciar-en-producción)

---

## 1. Configurar Supabase

### Paso 1: Crear proyecto

1. Ve a https://supabase.com
2. Click "New Project"
3. Nombre: `codeacademy`
4. Password: (Guarda esto seguro)
5. Region: Elige la más cercana (Europe West para España)
6. Click "Create Project" (tarda ~2 minutos)

### Paso 2: Copiar credenciales

Ve a `Settings → API`:

```bash
Project URL: https://xxxxx.supabase.co
anon public: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (¡Secreto!)
```

### Paso 3: Crear tablas

Ve a `SQL Editor` y ejecuta este script:

```sql
-- Tabla de perfiles de usuario
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT DEFAULT 'student' CHECK (role IN ('student', 'parent', 'teacher', 'admin')),
  age_group TEXT CHECK (age_group IN ('kids', 'teens', 'adults')),
  parent_id UUID REFERENCES profiles(id),
  display_name TEXT,
  avatar_url TEXT,
  preferred_language TEXT DEFAULT 'python',
  learning_style TEXT,
  goals TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de suscripciones
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  stripe_subscription_id TEXT UNIQUE,
  stripe_customer_id TEXT,
  status TEXT,
  plan_type TEXT,
  billing_interval TEXT,
  current_period_start TIMESTAMPTZ,
  current_period_end TIMESTAMPTZ,
  cancel_at_period_end BOOLEAN DEFAULT FALSE,
  canceled_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de pagos
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stripe_invoice_id TEXT UNIQUE,
  stripe_subscription_id TEXT,
  amount INTEGER,
  currency TEXT,
  status TEXT,
  paid_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de XP de usuario
CREATE TABLE user_xp (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE UNIQUE,
  total_xp INTEGER DEFAULT 0,
  level INTEGER DEFAULT 1,
  xp_in_level INTEGER DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_xp ENABLE ROW LEVEL SECURITY;

-- Políticas de seguridad
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

CREATE POLICY "Users can view own subscription"
  ON subscriptions FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can view own XP"
  ON user_xp FOR SELECT
  USING (auth.uid() = user_id);

-- Función para crear perfil automáticamente
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, display_name)
  VALUES (new.id, new.email);
  
  INSERT INTO public.user_xp (user_id)
  VALUES (new.id);
  
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger para nuevos usuarios
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

### Paso 4: Configurar Email Templates (opcional)

Ve a `Authentication → Email Templates` y personaliza los emails.

---

## 2. Configurar Stripe

### Paso 1: Crear cuenta

1. Ve a https://dashboard.stripe.com/register
2. Completa el registro
3. Activa tu cuenta (verificación de identidad)

### Paso 2: Crear productos

Ve a `Products → Add Product`:

#### Producto 1: Plan Starter
- Nombre: **CodeAcademy Starter**
- Descripción: Perfecto para comenzar tu viaje en programación
- Precio Mensual: €19.90
- Precio Anual: €199.00 (ahorra €39)
- Guarda los Price IDs: `price_xxxxx`

#### Producto 2: Plan Pro
- Nombre: **CodeAcademy Pro**
- Descripción: Para estudiantes serios que quieren dominar la programación
- Precio Mensual: €39.90
- Precio Anual: €399.00 (ahorra €80)
- Guarda los Price IDs: `price_xxxxx`

#### Producto 3: Plan Familia
- Nombre: **CodeAcademy Familia**
- Descripción: Hasta 5 miembros de la familia
- Precio Mensual: €79.90
- Precio Anual: €799.00 (ahorra €160)
- Guarda los Price IDs: `price_xxxxx`

### Paso 3: Configurar Trial Period

Para cada precio:
1. Click en el precio
2. "Add trial period"
3. 14 días
4. Save

### Paso 4: Configurar Webhook

1. Ve a `Developers → Webhooks`
2. Click "Add endpoint"
3. URL: `https://tu-dominio.com/api/stripe/webhook`
   (Por ahora usa: `http://tu-ip:3000/api/stripe/webhook`)
4. Events a escuchar:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
5. Guarda el **Signing Secret**: `whsec_xxxxx`

### Paso 5: Customer Portal

1. Ve a `Settings → Customer Portal`
2. Activa "Allow customers to..."
   - ✅ Update payment method
   - ✅ Cancel subscription
   - ✅ View invoice history
3. Save

### Paso 6: Copiar API Keys

Ve a `Developers → API Keys`:

**Test Mode** (para desarrollo):
```
Publishable key: pk_test_xxxxx
Secret key: sk_test_xxxxx
```

**Live Mode** (para producción):
```
Publishable key: pk_live_xxxxx
Secret key: sk_live_xxxxx
```

---

## 3. Variables de Entorno

### Para Desarrollo (ya configurado)

Archivo: `/home/dario/codeacademy/apps/web/.env.local`

Las variables de prueba ya están configuradas.

### Para Producción

Crea `/home/dario/codeacademy/apps/web/.env.production`:

```bash
# === SUPABASE (de Settings → API) ===
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx

# === STRIPE LIVE MODE ===
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxxxx
STRIPE_SECRET_KEY=sk_live_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx

# === PRICE IDS (de tus productos en Stripe) ===
NEXT_PUBLIC_PRICE_STARTER_MONTHLY=price_xxxxx
NEXT_PUBLIC_PRICE_STARTER_YEARLY=price_xxxxx
NEXT_PUBLIC_PRICE_PRO_MONTHLY=price_xxxxx
NEXT_PUBLIC_PRICE_PRO_YEARLY=price_xxxxx
NEXT_PUBLIC_PRICE_FAMILIA_MONTHLY=price_xxxxx
NEXT_PUBLIC_PRICE_FAMILIA_YEARLY=price_xxxxx

# === APP CONFIGURATION ===
NEXT_PUBLIC_APP_URL=https://tu-dominio.com
NODE_ENV=production

# === NEXTAUTH SECRET (genera uno único) ===
NEXTAUTH_SECRET=$(openssl rand -base64 32)
```

### Generar NEXTAUTH_SECRET

```bash
openssl rand -base64 32
```

Copia el resultado y pégalo en `.env.production`

---

## 4. Iniciar en Producción

### Opción A: Con PM2 (Recomendado)

```bash
# Instalar PM2
npm install -g pm2

# Configurar variables de producción
cd /home/dario/codeacademy/apps/web
cp .env.production .env.local  # O edita .env.local con valores reales

# Build de producción
npm run build

# Iniciar con PM2
pm2 start npm --name "codeacademy" -- start

# Configurar para que inicie al arrancar
pm2 startup
pm2 save

# Ver logs
pm2 logs codeacademy
```

### Opción B: Con systemd (alternativa)

Crea `/etc/systemd/system/codeacademy.service`:

```ini
[Unit]
Description=CodeAcademy Next.js App
After=network.target

[Service]
Type=simple
User=dario
WorkingDirectory=/home/dario/codeacademy/apps/web
ExecStart=/usr/bin/npm start
Restart=on-failure
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable codeacademy
sudo systemctl start codeacademy
sudo systemctl status codeacademy
```

---

## 5. Configurar Nginx + SSL

### Instalar Nginx

```bash
sudo apt update
sudo apt install nginx
```

### Crear configuración

```bash
sudo nano /etc/nginx/sites-available/codeacademy
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Aumentar timeout para Stripe webhooks
    location /api/stripe/webhook {
        proxy_pass http://localhost:3000;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }
}
```

### Activar sitio

```bash
sudo ln -s /etc/nginx/sites-available/codeacademy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Instalar SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

Certbot configurará automáticamente HTTPS.

---

## 6. Testing

### Health Check

```bash
curl http://localhost:3000/api/health
```

Debería responder:
```json
{
  "status": "ok",
  "services": {
    "database": "ok",
    "stripe": "ok"
  }
}
```

### Test de Registro

1. Ve a tu dominio
2. Click "Sign Up"
3. Regístrate con email
4. Verifica que se cree perfil en Supabase

### Test de Stripe

1. Ve a `/pricing`
2. Selecciona un plan
3. Usa tarjeta de prueba: `4242 4242 4242 4242`
4. Verifica webhook en Stripe Dashboard

---

## 📋 Checklist Final

- [ ] Supabase configurado y tablas creadas
- [ ] Productos Stripe creados (3 planes x 2 intervalos = 6 precios)
- [ ] Webhook Stripe configurado
- [ ] Variables de entorno actualizadas
- [ ] Build de producción exitoso
- [ ] PM2 corriendo la app
- [ ] Nginx configurado
- [ ] SSL activo
- [ ] Health check OK
- [ ] Test de registro funciona
- [ ] Test de pago funciona

---

## 🆘 Soporte

Si tienes problemas:

1. Revisa logs: `pm2 logs codeacademy`
2. Verifica variables: `echo $NEXT_PUBLIC_SUPABASE_URL`
3. Health check: `curl http://localhost:3000/api/health`
4. Nginx logs: `sudo tail -f /var/log/nginx/error.log`

---

**¡Tu CodeAcademy estará 100% funcional cuando completes estos pasos!** 🚀
