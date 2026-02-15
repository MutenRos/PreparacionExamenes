# 📸 Guía Visual: Configurar Email Verification en Supabase Dashboard

## Paso 1: Acceder a tu proyecto de Supabase

1. Ve a: **https://app.supabase.com**
2. Selecciona tu proyecto (o crea uno nuevo)
3. Toma nota de tu **Project URL** (la verás en la esquina superior)

---

## Paso 2: Obtener las credenciales

### 📍 Ubicación: `Settings` (ícono de engranaje) → `API`

Verás tres secciones importantes:

### ✅ Project URL
```
https://tuproyecto.supabase.co
```
**Copia esto:** Esta es tu `NEXT_PUBLIC_SUPABASE_URL`

### ✅ Project API keys

**anon/public key:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
```
**Copia esto:** Esta es tu `NEXT_PUBLIC_SUPABASE_ANON_KEY`

**service_role key:** (⚠️ SECRETO - nunca expongas en el cliente)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU
```
**Copia esto:** Esta es tu `SUPABASE_SERVICE_ROLE_KEY`

---

## Paso 3: Actualizar variables de entorno

Edita `.env.local` en la raíz de tu proyecto:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://tuproyecto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGci... (tu clave aquí)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGci... (tu clave aquí)
```

**Reinicia el servidor:**
```bash
pkill -f "next dev"
npm run dev
```

---

## Paso 4: Configurar Email Template

### 📍 Ubicación: `Authentication` → `Email Templates` → `Confirm signup`

1. En el menú lateral, haz clic en **Authentication** (ícono de candado)
2. Luego en **Email Templates** (submenú)
3. Busca **"Confirm signup"** en la lista
4. Haz clic para editarlo

### Template HTML a usar:

Borra todo el contenido actual y pega esto:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verifica tu email - CodeAcademy</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #0f172a;">
  <table role="presentation" style="width: 100%; border-collapse: collapse;">
    <tr>
      <td align="center" style="padding: 40px 0;">
        <table role="presentation" style="width: 600px; border-collapse: collapse;">
          <!-- Header con gradient morado/rosa -->
          <tr>
            <td style="background: linear-gradient(to right, #9333ea, #ec4899); padding: 40px; text-align: center; border-radius: 8px 8px 0 0;">
              <h1 style="margin: 0; color: white; font-size: 32px; font-weight: bold;">CodeAcademy</h1>
            </td>
          </tr>
          <!-- Contenido -->
          <tr>
            <td style="background-color: #1e293b; padding: 40px; border-radius: 0 0 8px 8px;">
              <h2 style="color: white; margin-top: 0;">¡Bienvenido a CodeAcademy! 🎉</h2>
              <p style="color: #cbd5e1; font-size: 16px; line-height: 1.6;">
                Estás a un paso de comenzar tu viaje en programación.
              </p>
              <p style="color: #cbd5e1; font-size: 16px; line-height: 1.6;">
                Haz clic en el botón para verificar tu cuenta:
              </p>
              <!-- Botón -->
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
                              font-weight: bold;
                              font-size: 16px;">
                      Verificar mi email
                    </a>
                  </td>
                </tr>
              </table>
              <p style="color: #94a3b8; font-size: 14px; line-height: 1.6;">
                O copia y pega esta URL en tu navegador:
              </p>
              <p style="background-color: #0f172a; 
                        padding: 12px; 
                        border-radius: 4px; 
                        color: #a78bfa; 
                        font-size: 12px; 
                        word-break: break-all;
                        border: 1px solid #334155;">
                {{ .ConfirmationURL }}
              </p>
              <hr style="border: none; border-top: 1px solid #334155; margin: 30px 0;">
              <p style="color: #64748b; font-size: 12px; line-height: 1.6; margin: 0;">
                Si no creaste una cuenta en CodeAcademy, puedes ignorar este email.
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

**⚠️ IMPORTANTE:** No modifiques `{{ .ConfirmationURL }}` - es una variable de Supabase

5. Haz clic en **"Save"** abajo

---

## Paso 5: Configurar Redirect URLs

### 📍 Ubicación: `Authentication` → `URL Configuration`

1. En el menú lateral, **Authentication**
2. Luego **URL Configuration**
3. Busca la sección **"Redirect URLs"**

### URLs a agregar:

Haz clic en **"Add URL"** y agrega una por una:

```
http://localhost:3000/auth/verify-email
http://192.168.1.157:3000/auth/verify-email
http://88.17.157.221:3000/auth/verify-email
```

💡 **Tip:** Cuando tengas un dominio de producción, agrega también:
```
https://tudominio.com/auth/verify-email
```

### Site URL:

En el campo **"Site URL"**, asegúrate que esté:
```
http://localhost:3000
```

(Cámbialo a tu dominio de producción cuando despliegues)

4. Haz clic en **"Save"**

---

## Paso 6: Habilitar Email Confirmation

### 📍 Ubicación: `Authentication` → `Providers` → `Email`

1. En el menú lateral, **Authentication**
2. Luego **Providers**
3. Busca **"Email"** en la lista
4. Haz clic en **"Email"** para expandir

### Configuración:

✅ **Enable Email provider** - Debe estar ON (azul)

✅ **Confirm email** - ⚠️ **MUY IMPORTANTE** - Debe estar ON (azul)
   - Esto hace que Supabase envíe el email de verificación automáticamente

Otras opciones (puedes dejarlas por defecto):
- Secure email change: ON (recomendado)
- Secure password change: ON (recomendado)

5. No olvides hacer clic en **"Save"** si hiciste cambios

---

## Paso 7: [OPCIONAL] Ejecutar migración SQL

### 📍 Ubicación: `SQL Editor`

1. En el menú lateral, haz clic en **SQL Editor** (ícono de </> )
2. Haz clic en **"New query"**
3. Copia y pega el contenido completo de:
   ```
   supabase/migrations/001_email_verification_setup.sql
   ```
4. Haz clic en **"Run"** (botón azul abajo a la derecha)

Esto creará:
- ✅ Tabla `profiles` con campos de usuario
- ✅ Row Level Security (RLS) policies
- ✅ Triggers automáticos
- ✅ Funciones útiles

**Verás al final:**
```
✅ Tabla profiles creada correctamente
✅ RLS habilitado en profiles
✅ Trigger on_auth_user_created configurado
✅ Configuración completada exitosamente
```

---

## Paso 8: [OPCIONAL] Configurar SMTP Custom

⚠️ **Solo para producción** - El SMTP de Supabase tiene límites diarios

### 📍 Ubicación: `Project Settings` → `Auth` → `SMTP Settings`

1. En el menú lateral, **Settings** (ícono de engranaje)
2. Luego **Auth** (en el submenú)
3. Scroll hasta **"SMTP Settings"**

### Opciones populares:

#### SendGrid (Recomendado - 100 emails/día gratis):
```
SMTP Host: smtp.sendgrid.net
SMTP Port: 587
SMTP User: apikey
SMTP Password: tu_sendgrid_api_key
```

#### Mailgun:
```
SMTP Host: smtp.mailgun.org
SMTP Port: 587
SMTP User: tu_usuario@mg.tudominio.com
SMTP Password: tu_password
```

#### Gmail (Solo desarrollo):
```
SMTP Host: smtp.gmail.com
SMTP Port: 587
SMTP User: tu_email@gmail.com
SMTP Password: tu_app_password (no tu password normal)
```

4. **Enable Custom SMTP** - ON
5. **Sender email:** tu-email@tudominio.com
6. **Sender name:** CodeAcademy
7. Haz clic en **"Save"**

---

## ✅ Verificación Final

### Checklist antes de testear:

- [ ] Variables de entorno actualizadas en `.env.local`
- [ ] Servidor reiniciado (`npm run dev`)
- [ ] Email template configurado con el HTML proporcionado
- [ ] Redirect URLs agregadas (al menos localhost)
- [ ] Site URL configurado
- [ ] Email provider habilitado
- [ ] **Confirm email** habilitado ⚠️
- [ ] [Opcional] Migración SQL ejecutada
- [ ] [Opcional] SMTP custom configurado

---

## 🧪 Testear el sistema

### Test local:

1. Abre: http://localhost:3000/auth/register
2. Completa el formulario con **un email real**
3. Haz clic en "Crear cuenta"
4. Deberías ver: "¡Cuenta creada! Hemos enviado un email de verificación..."

### Verificar email enviado:

1. Revisa tu inbox (puede tardar 1-2 minutos)
2. **También revisa spam/junk** (importante!)
3. Busca un email de "noreply@mail.app.supabase.co"
4. Debería tener el diseño morado/rosa de CodeAcademy

### Hacer clic en verificación:

1. Haz clic en "Verificar mi email" en el email
2. Te redirigirá a: `http://localhost:3000/auth/verify-email?token=...`
3. Verás un spinner y luego: "¡Email verificado!"
4. Auto-redirige al dashboard después de 3 segundos

### Verificar en Supabase:

1. Ve a **Authentication** → **Users**
2. Busca tu email
3. Deberías ver:
   - Estado: **"Confirmed"** ✅
   - `Email Confirmed At`: Una fecha (no vacío)

---

## 🎉 ¡Listo!

Tu sistema de email verification está completamente configurado.

### Si algo no funciona:

1. Revisa la sección de **Troubleshooting** en `QUICK_START_EMAIL_VERIFICATION.md`
2. Verifica los logs en: **Logs** → **Auth Logs** en Supabase
3. Asegúrate que "Confirm email" esté habilitado (paso más común que se olvida)

### Próximos pasos:

- Testea desde diferentes dispositivos
- Configura SMTP custom para producción
- Personaliza más el email template
- Agrega tu dominio a las redirect URLs

---

## 📚 Más información:

- `QUICK_START_EMAIL_VERIFICATION.md` - Guía rápida
- `docs/SUPABASE_EMAIL_SETUP.md` - Documentación completa
- Scripts automatizados en `scripts/`
