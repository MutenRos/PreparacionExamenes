# Configuración de Email en Supabase

## 🎯 Resumen
Sistema de verificación de email completamente integrado con Supabase Auth.

## 📋 Pasos de Configuración

### 1. Configurar Email Templates en Supabase Dashboard

Ve a tu proyecto de Supabase → **Authentication** → **Email Templates**

#### Template: Confirm Signup
```html
<h2>Verifica tu email en CodeAcademy</h2>
<p>¡Bienvenido a CodeAcademy! Haz clic en el enlace de abajo para verificar tu cuenta:</p>
<p><a href="{{ .ConfirmationURL }}">Verificar mi email</a></p>
<p>O copia y pega esta URL en tu navegador:</p>
<p>{{ .ConfirmationURL }}</p>
<p>Si no creaste una cuenta en CodeAcademy, puedes ignorar este email.</p>
```

### 2. Configurar Redirect URLs

En **Authentication** → **URL Configuration**:

**Site URL:**
- Desarrollo: `http://localhost:3000`
- Producción: `https://tu-dominio.com`

**Redirect URLs (agregar estas URLs):**
- `http://localhost:3000/auth/verify-email`
- `https://tu-dominio.com/auth/verify-email`
- `http://192.168.1.157:3000/auth/verify-email` (tu IP local)
- `http://88.17.157.221:3000/auth/verify-email` (tu IP pública)

### 3. Verificar Variables de Entorno

Asegúrate de que `.env.local` tenga:

```bash
NEXT_PUBLIC_SUPABASE_URL=tu_url_de_supabase
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu_anon_key
SUPABASE_SERVICE_ROLE_KEY=tu_service_role_key
```

### 4. Configurar SMTP (Opcional pero Recomendado)

Por defecto, Supabase usa su propio servicio de email, pero tiene límites.

Para producción, configura tu propio SMTP en **Project Settings** → **Auth** → **SMTP Settings**:

**Opciones populares:**
- **SendGrid** (12,000 emails/mes gratis)
- **Mailgun** (5,000 emails/mes gratis)
- **AWS SES** (muy económico)
- **Gmail SMTP** (para desarrollo)

## 🔄 Flujo Completo

### 1. Registro
```typescript
// apps/web/src/app/auth/register/page.tsx
const { error } = await supabase.auth.signUp({
  email: formData.email,
  password: formData.password,
  options: {
    data: { name, role },
    emailRedirectTo: `${window.location.origin}/auth/verify-email`
  }
});
```

**Resultado:**
- Usuario creado en Supabase (estado: no confirmado)
- Email enviado automáticamente
- UI muestra mensaje de verificación

### 2. Verificación
Usuario hace clic en el email → redirige a `/auth/verify-email?token=xxx`

```typescript
// apps/web/src/app/auth/verify-email/page.tsx
const { error } = await supabase.auth.verifyOtp({
  token_hash: token,
  type: 'email'
});
```

**Resultado:**
- Usuario confirmado en Supabase
- Sesión creada automáticamente
- Redirect a dashboard

### 3. Reenvío
Si el usuario no recibió el email:

```typescript
// apps/web/src/app/auth/resend-verification/page.tsx
const { error } = await supabase.auth.resend({
  type: 'signup',
  email: email,
  options: {
    emailRedirectTo: `${window.location.origin}/auth/verify-email`
  }
});
```

## 🧪 Testing

### Desarrollo Local
1. Inicia el servidor: `npm run dev`
2. Ve a `http://localhost:3000/auth/register`
3. Crea una cuenta con un email real
4. Revisa tu inbox
5. Haz clic en el enlace de verificación

### Verificar en Supabase Dashboard
- Ve a **Authentication** → **Users**
- Busca tu usuario
- Verifica que el campo `email_confirmed_at` tenga una fecha después de hacer clic

## 🎨 Personalización de Emails

### Variables disponibles en templates:
- `{{ .Email }}` - Email del usuario
- `{{ .ConfirmationURL }}` - URL de confirmación
- `{{ .Token }}` - Token de verificación
- `{{ .TokenHash }}` - Hash del token
- `{{ .SiteURL }}` - URL del sitio

### Template personalizado con branding:
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background: linear-gradient(to right, #9333ea, #ec4899); padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }
    .content { background: #1e293b; padding: 30px; border-radius: 0 0 8px 8px; }
    .button { display: inline-block; background: linear-gradient(to right, #9333ea, #ec4899); color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 style="margin: 0; color: white;">CodeAcademy</h1>
    </div>
    <div class="content">
      <h2>¡Bienvenido a CodeAcademy! 🎉</h2>
      <p>Estás a un paso de comenzar tu viaje en programación.</p>
      <p>Haz clic en el botón para verificar tu cuenta:</p>
      <a href="{{ .ConfirmationURL }}" class="button">Verificar mi email</a>
      <p style="color: #94a3b8; font-size: 14px;">
        O copia esta URL en tu navegador:<br>
        {{ .ConfirmationURL }}
      </p>
      <hr style="border: 1px solid #334155; margin: 30px 0;">
      <p style="color: #94a3b8; font-size: 12px;">
        Si no creaste una cuenta en CodeAcademy, ignora este email.
      </p>
    </div>
  </div>
</body>
</html>
```

## 🔒 Seguridad

### Rate Limiting
Supabase incluye rate limiting automático:
- Máximo 1 email cada 60 segundos por email
- Protección contra spam

### Token Expiration
- Los tokens expiran en 24 horas
- Después, el usuario debe usar "Reenviar verificación"

### Email Validation
- Validación de formato en frontend
- Validación de dominio en Supabase

## 📊 Monitoreo

### Ver estadísticas en Supabase:
1. **Authentication** → **Users** - Ver usuarios confirmados vs no confirmados
2. **Logs** → **Auth Logs** - Ver intentos de registro y verificación
3. **API** → **API Logs** - Ver llamadas a auth.signUp, verifyOtp, resend

### Queries útiles:
```sql
-- Usuarios no verificados
SELECT email, created_at 
FROM auth.users 
WHERE email_confirmed_at IS NULL;

-- Usuarios verificados hoy
SELECT email, email_confirmed_at 
FROM auth.users 
WHERE DATE(email_confirmed_at) = CURRENT_DATE;

-- Rate de verificación
SELECT 
  COUNT(*) as total,
  COUNT(email_confirmed_at) as verified,
  ROUND(COUNT(email_confirmed_at)::numeric / COUNT(*) * 100, 2) as verification_rate
FROM auth.users;
```

## 🐛 Troubleshooting

### El email no llega
1. Verifica spam/junk folder
2. Verifica que el email esté en redirect URLs
3. Revisa logs en Supabase: **Logs** → **Auth Logs**
4. Verifica SMTP configuration (si usas custom SMTP)

### Token inválido o expirado
- Tokens expiran en 24h
- Usa `/auth/resend-verification` para generar uno nuevo

### Redirect no funciona
- Verifica que la URL esté en **Redirect URLs** de Supabase
- Verifica formato: debe incluir protocolo (http:// o https://)
- No olvides agregar todas tus IPs/dominios

### Usuario no puede hacer login
- Verifica que `email_confirmed_at` NO sea NULL en Supabase
- Si es NULL, el usuario debe verificar su email primero

## ✅ Checklist de Producción

Antes de ir a producción:

- [ ] Email templates configurados y personalizados
- [ ] SMTP configurado (SendGrid, Mailgun, etc.)
- [ ] Todas las redirect URLs agregadas
- [ ] Site URL configurada correctamente
- [ ] Variables de entorno en producción
- [ ] Rate limiting configurado
- [ ] Emails de prueba enviados y verificados
- [ ] Logs monitoreados
- [ ] Backup de configuración documentado

## 🚀 Next Steps

1. **Password Reset:** Similar flow, ya está preparado en Supabase
2. **Email Change:** Requiere re-verificación automática
3. **Magic Links:** Login sin contraseña (alternativa al email/password)
4. **Social Auth:** Google, GitHub, etc. (ya está UI preparada)

## 📚 Recursos

- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
- [Email Templates Guide](https://supabase.com/docs/guides/auth/auth-email-templates)
- [SMTP Configuration](https://supabase.com/docs/guides/auth/auth-smtp)
