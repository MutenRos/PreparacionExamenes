# 🚀 Guía Rápida: Configuración de Email Verification

## ⚡ Setup en 5 minutos

### Opción 1: Script Automático (Recomendado)

```bash
# Ejecutar el script interactivo
bash scripts/setup-supabase-email.sh
```

El script te pedirá:
1. URL de tu proyecto Supabase
2. Anon Key
3. Service Role Key

Y configurará automáticamente:
- ✅ Variables de entorno (`.env.local`)
- ✅ Instrucciones para dashboard
- ✅ Email template listo para copiar

### Opción 2: Configuración Manual

#### 1️⃣ Obtén tus credenciales de Supabase

Ve a: https://app.supabase.com/project/_/settings/api

Copia:
- `Project URL` → NEXT_PUBLIC_SUPABASE_URL
- `anon/public` key → NEXT_PUBLIC_SUPABASE_ANON_KEY  
- `service_role` key → SUPABASE_SERVICE_ROLE_KEY

#### 2️⃣ Actualiza variables de entorno

Edita `.env.local` en la raíz del proyecto:

```bash
# ===== SUPABASE =====
NEXT_PUBLIC_SUPABASE_URL=https://tuproyecto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 3️⃣ Configura Email Templates en Supabase

**Ve a:** `Authentication` → `Email Templates` → `Confirm signup`

**Copia este template:**

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Verifica tu email - CodeAcademy</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #0f172a;">
  <table role="presentation" style="width: 100%; border-collapse: collapse;">
    <tr>
      <td align="center" style="padding: 40px 0;">
        <table role="presentation" style="width: 600px; border-collapse: collapse;">
          <!-- Header -->
          <tr>
            <td style="background: linear-gradient(to right, #9333ea, #ec4899); padding: 40px; text-align: center; border-radius: 8px 8px 0 0;">
              <h1 style="margin: 0; color: white; font-size: 32px;">CodeAcademy</h1>
            </td>
          </tr>
          <!-- Content -->
          <tr>
            <td style="background-color: #1e293b; padding: 40px; border-radius: 0 0 8px 8px;">
              <h2 style="color: white;">¡Bienvenido a CodeAcademy! 🎉</h2>
              <p style="color: #cbd5e1; font-size: 16px; line-height: 1.6;">
                Estás a un paso de comenzar tu viaje en programación.
              </p>
              <table role="presentation" style="margin: 30px 0;">
                <tr>
                  <td align="center">
                    <a href="{{ .ConfirmationURL }}" 
                       style="background: linear-gradient(to right, #9333ea, #ec4899); 
                              color: white; 
                              padding: 16px 32px; 
                              text-decoration: none; 
                              border-radius: 8px; 
                              display: inline-block;
                              font-weight: bold;">
                      Verificar mi email
                    </a>
                  </td>
                </tr>
              </table>
              <p style="color: #94a3b8; font-size: 14px;">
                O copia esta URL: {{ .ConfirmationURL }}
              </p>
              <hr style="border: none; border-top: 1px solid #334155; margin: 30px 0;">
              <p style="color: #64748b; font-size: 12px; margin: 0;">
                Si no creaste una cuenta, ignora este email.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

#### 4️⃣ Configura Redirect URLs

**Ve a:** `Authentication` → `URL Configuration`

**Agrega estas URLs:**
```
http://localhost:3000/auth/verify-email
http://192.168.1.157:3000/auth/verify-email
http://88.17.157.221:3000/auth/verify-email
```

**Site URL:**
```
http://localhost:3000
```

#### 5️⃣ Habilita Email Confirmation

**Ve a:** `Authentication` → `Providers` → `Email`

- ✅ Enable Email provider
- ✅ **Confirm email** (muy importante!)

#### 6️⃣ [OPCIONAL] Ejecuta la migración SQL

**Ve a:** `SQL Editor` en Supabase Dashboard

Ejecuta el contenido de: `supabase/migrations/001_email_verification_setup.sql`

Esto creará:
- Tabla `profiles` con campos de verificación
- Triggers automáticos para sincronizar con auth.users
- Row Level Security policies
- Funciones útiles

## 🧪 Testing

### Probar localmente:

```bash
# 1. Instalar dependencias (si no lo has hecho)
npm install

# 2. Iniciar el servidor
npm run dev

# 3. Abrir en navegador
http://localhost:3000/auth/register
```

### Probar desde red local:

```bash
http://192.168.1.157:3000/auth/register
```

### Probar desde internet:

```bash
http://88.17.157.221:3000/auth/register
```

### Flujo completo:

1. ✅ Crear cuenta con email real
2. ✅ Ver mensaje de "Email enviado"
3. ✅ Revisar inbox (y spam)
4. ✅ Hacer clic en "Verificar mi email"
5. ✅ Redirige a `/auth/verify-email?token=...`
6. ✅ Muestra "Email verificado!"
7. ✅ Auto-redirige al dashboard

## 🔍 Verificar que funciona

### Opción 1: Supabase Dashboard

**Ve a:** `Authentication` → `Users`

Busca tu usuario y verifica:
- ✅ `email_confirmed_at` tiene una fecha (no NULL)
- ✅ Estado: "Confirmed"

### Opción 2: SQL Query

En `SQL Editor`:

```sql
-- Ver usuarios no verificados
SELECT email, created_at, email_confirmed_at
FROM auth.users
WHERE email_confirmed_at IS NULL;

-- Ver usuarios verificados hoy
SELECT email, email_confirmed_at
FROM auth.users
WHERE DATE(email_confirmed_at) = CURRENT_DATE;

-- Estadísticas generales
SELECT 
  COUNT(*) as total,
  COUNT(email_confirmed_at) as verified,
  ROUND(COUNT(email_confirmed_at)::numeric / COUNT(*) * 100, 2) as rate
FROM auth.users;
```

### Opción 3: Auth Logs

**Ve a:** `Logs` → `Auth Logs`

Verás:
- `signup` - Cuando usuario se registra
- `verify` - Cuando hace clic en el email
- `token_refreshed` - Cuando se crea la sesión

## 🐛 Troubleshooting

### El email no llega

**Causa común:** Supabase free tier tiene límites

**Soluciones:**
1. Revisa carpeta de spam/junk
2. Espera 1-2 minutos (puede demorar)
3. Ve a `Logs` → `Auth Logs` y busca errores
4. Verifica que el email template tenga `{{ .ConfirmationURL }}`

**Para producción:** Configura SMTP custom (SendGrid, Mailgun)

### Token inválido o expirado

**Causa:** Los tokens expiran en 24 horas

**Solución:** 
- Ve a `/auth/resend-verification`
- Ingresa tu email
- Solicita nuevo email

### Redirect no funciona

**Causa:** URL no está en la whitelist

**Solución:**
1. Ve a `Authentication` → `URL Configuration`
2. Verifica que tu URL esté en "Redirect URLs"
3. Formato correcto: `http://localhost:3000/auth/verify-email`
4. No olvides el protocolo (`http://` o `https://`)

### Usuario no puede hacer login

**Causa:** Email no verificado

**Síntomas:**
- Error: "Email not confirmed"
- `email_confirmed_at` es NULL en la base de datos

**Solución:**
1. El usuario debe verificar su email primero
2. O usa `/auth/resend-verification`

### Cambios en .env.local no se aplican

**Solución:**
```bash
# Reinicia el servidor
pkill -f "next dev"
npm run dev
```

## 📊 Monitoreo en Producción

### Ver estadísticas:

```sql
SELECT * FROM public.email_verification_stats;
```

### Usuarios sin verificar (para recordatorios):

```sql
SELECT 
  email, 
  created_at,
  EXTRACT(day FROM NOW() - created_at) as days_since_signup
FROM auth.users
WHERE email_confirmed_at IS NULL
ORDER BY created_at DESC;
```

### Rate limiting automático:

Supabase incluye:
- Máximo 1 email cada 60 segundos por dirección
- Protección contra spam automática

## 🔒 Seguridad

### ✅ Lo que YA está protegido:

- Tokens únicos por usuario
- Expiran en 24 horas
- Rate limiting automático
- HTTPS en producción (Supabase)
- Row Level Security (RLS) en la base de datos

### 🚨 Para producción:

1. **SMTP Custom**: No uses el SMTP de Supabase (tiene límites)
2. **Email Validation**: Ya implementada en frontend
3. **Monitoring**: Usa Sentry o LogRocket
4. **Backups**: Activa backups automáticos en Supabase

## 📚 Recursos Adicionales

- [Documentación completa](./SUPABASE_EMAIL_SETUP.md)
- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
- [Email Templates](https://supabase.com/docs/guides/auth/auth-email-templates)
- [SMTP Setup](https://supabase.com/docs/guides/auth/auth-smtp)

## ✅ Checklist de Producción

Antes de lanzar:

- [ ] Variables de entorno en producción
- [ ] Email template personalizado
- [ ] SMTP custom configurado (SendGrid/Mailgun)
- [ ] Todas las redirect URLs agregadas (incluye dominio de producción)
- [ ] Site URL apuntando al dominio de producción
- [ ] Migración SQL ejecutada
- [ ] Email de prueba enviado y verificado
- [ ] Monitoreo configurado (Sentry/LogRocket)
- [ ] Rate limiting verificado
- [ ] Backups automáticos activados

## 🎉 ¡Listo!

Tu sistema de verificación de email está configurado y listo para usar.

**Cualquier duda:** Revisa `docs/SUPABASE_EMAIL_SETUP.md` para más detalles.
