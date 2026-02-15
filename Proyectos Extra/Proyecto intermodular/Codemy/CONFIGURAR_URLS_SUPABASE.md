# 🔧 Configurar URLs de Redirección en Supabase

Para que el link del email de confirmación funcione correctamente, necesitas configurar las URLs permitidas en Supabase.

## Paso 1: Acceder a la configuración

1. Ve a https://supabase.com/dashboard/project/oubxugjtcxtvreyllsrb/auth/url-configuration
2. O navega manualmente:
   - Dashboard de Supabase
   - Tu proyecto
   - Authentication → URL Configuration

## Paso 2: Configurar Site URL

En **"Site URL"**, añade:
```
http://localhost:3000
```

## Paso 3: Configurar Redirect URLs

En **"Redirect URLs"**, añade estas URLs (una por línea):

```
http://localhost:3000/auth/callback
http://localhost:3000/auth/verify-email
http://localhost:3000/dashboard
```

También añade tu dominio de producción cuando lo tengas:
```
https://tudominio.com/auth/callback
https://tudominio.com/auth/verify-email
https://tudominio.com/dashboard
```

## Paso 4: Guardar cambios

Click en **"Save"** en la parte inferior de la página.

## Paso 5: Probar

1. Reinicia el servidor de desarrollo (ya está hecho)
2. Registra un nuevo usuario
3. Revisa tu email
4. Click en el link de confirmación
5. Deberías ser redirigido a `/auth/callback` y luego a `/dashboard`

---

## ✅ URLs configuradas en la app:

- **Email redirect**: `http://localhost:3000/auth/callback`
- **Callback handler**: Route API que procesa el código de verificación
- **Success redirect**: `/dashboard`

---

## 🔍 Para debugging:

Si el link sigue sin funcionar:

1. Verifica que las URLs en Supabase coincidan exactamente (sin slash final)
2. Revisa la consola del navegador (F12) para ver errores
3. Comprueba que el email tenga un link válido (no `about:blank`)

---

## 📧 Configuración opcional de Email:

Para personalizar los emails, ve a:
- Authentication → Email Templates
- Edita "Confirm signup"
- Asegúrate que use `{{ .ConfirmationURL }}`
