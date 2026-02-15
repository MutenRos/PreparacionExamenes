# 📧 Configurar Email Real con Resend + Supabase

## Paso 1: Crear cuenta en Resend (GRATIS)

1. Ve a: https://resend.com/signup
2. Regístrate con tu email
3. Verifica tu cuenta

## Paso 2: Obtener API Key de Resend

1. Una vez dentro de Resend, ve a **API Keys**
2. Click en **"Create API Key"**
3. Dale un nombre: `Supabase CodeAcademy`
4. **Copia la API Key** (empieza con `re_...`)

## Paso 3: Configurar dominio (Opcional pero recomendado)

**Opción A: Usar dominio propio**
1. En Resend, ve a **Domains**
2. Add domain → Ingresa tu dominio
3. Añade los registros DNS que te indica
4. Verifica el dominio

**Opción B: Usar dominio de prueba de Resend**
- Resend te da un dominio `onboarding.resend.dev` para testing
- Emails solo se enviarán a tu email verificado
- Perfecto para desarrollo

## Paso 4: Configurar SMTP en Supabase

1. Ve a: https://supabase.com/dashboard/project/oubxugjtcxtvreyllsrb/settings/auth

2. Busca la sección **"SMTP Settings"** o **"Email"**

3. **Activa "Enable Custom SMTP"**

4. **Configura con estos valores:**

```
Host: smtp.resend.com
Port: 587 (o 465 para SSL)
Username: resend
Password: [Tu API Key que copiaste, empieza con re_...]
Sender email: noreply@tudominio.com (o onboarding@resend.dev)
Sender name: CodeAcademy
```

5. **Guarda los cambios**

## Paso 5: Configurar plantilla de email (Opcional)

1. En Supabase, ve a **Authentication → Email Templates**
2. Edita **"Confirm signup"**
3. Personaliza el mensaje (opcional)
4. Asegúrate que tenga `{{ .ConfirmationURL }}`

## Paso 6: Probar

1. Registra un nuevo usuario en tu app
2. Revisa tu bandeja de entrada
3. Deberías recibir el email de confirmación
4. Click en el link → Te redirige a `/auth/callback` → Dashboard

---

## 🆓 Límites de Resend (Plan Gratuito)

- ✅ 3,000 emails/mes GRATIS
- ✅ 100 emails/día
- ✅ Perfecto para desarrollo y MVP
- ✅ No requiere tarjeta de crédito

---

## ⚡ Configuración rápida (si no tienes dominio)

Si solo quieres testear rápido:

1. Crea cuenta en Resend
2. Obtén tu API Key
3. En Supabase SMTP:
   - Host: `smtp.resend.com`
   - Port: `587`
   - Username: `resend`
   - Password: `re_tu_api_key_aqui`
   - Sender: `onboarding@resend.dev`

4. Los emails se enviarán SOLO a tu email verificado en Resend
5. Suficiente para testing

---

## 🐛 Problemas comunes

### Email no llega
- Revisa spam/promociones
- Verifica que el email del sender está verificado en Resend
- Revisa los logs de Resend: https://resend.com/emails

### Error de autenticación
- Verifica que copiaste la API Key completa
- Asegúrate de usar `resend` como username (no tu email)

### Link roto en el email
- Verifica que configuraste las URLs en Supabase (ver CONFIGURAR_URLS_SUPABASE.md)
- Debe incluir: `http://localhost:3000/auth/callback`

---

## ✅ Checklist final

- [ ] Cuenta en Resend creada
- [ ] API Key obtenida
- [ ] SMTP configurado en Supabase
- [ ] URLs de redirect configuradas
- [ ] Email de prueba enviado
- [ ] Link de confirmación funciona

---

## Alternativas a Resend

Si prefieres otro proveedor:

**Gmail** (no recomendado para producción):
- Host: `smtp.gmail.com`, Port: `587`
- Usuario: tu-email@gmail.com
- Password: App Password (generar en configuración de Google)

**SendGrid**:
- Host: `smtp.sendgrid.net`, Port: `587`
- Usuario: `apikey`
- Password: Tu API key de SendGrid

**Mailgun**:
- Host: `smtp.mailgun.org`, Port: `587`
- Usuario: Tu usuario de Mailgun
- Password: Tu password de Mailgun
