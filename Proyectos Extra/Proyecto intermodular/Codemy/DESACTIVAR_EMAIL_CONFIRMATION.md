# 🔧 Desactivar Confirmación de Email en Desarrollo

Para que el registro funcione sin necesidad de verificar el email (útil en desarrollo), sigue estos pasos:

## Opción 1: Desactivar confirmación de email (Recomendado para desarrollo)

1. **Ve a**: https://supabase.com/dashboard/project/oubxugjtcxtvreyllsrb/auth/providers

2. **Busca la sección "Email"**

3. **Desactiva "Enable email confirmations"**
   - Esto permitirá que los usuarios se registren sin necesidad de confirmar el email
   - Útil para desarrollo y testing

4. **Guarda los cambios**

## Opción 2: Configurar SMTP para envío de emails real

Si prefieres que se envíen emails reales:

1. **Ve a**: https://supabase.com/dashboard/project/oubxugjtcxtvreyllsrb/settings/auth

2. **Busca "SMTP Settings"**

3. **Configura tu proveedor de email:**
   - **Gmail**: 
     - Host: `smtp.gmail.com`
     - Port: `587`
     - User: tu email
     - Password: App password (no tu contraseña normal)
   
   - **Resend** (recomendado):
     - Host: `smtp.resend.com`
     - Port: `587`
     - User: `resend`
     - Password: Tu API key de Resend
   
   - **Mailgun, SendGrid, etc.**: Usa sus credenciales SMTP

4. **Sender email**: El email que aparecerá como remitente

5. **Guarda y prueba**

## Opción 3: Ver el "magic link" en los logs de Supabase

Durante el desarrollo, Supabase NO envía emails reales a menos que configures SMTP.

**Para ver el link de confirmación:**

1. Ve a: https://supabase.com/dashboard/project/oubxugjtcxtvreyllsrb/logs/explorer

2. Ejecuta esta query SQL en el SQL Editor:
   ```sql
   SELECT * FROM auth.users 
   ORDER BY created_at DESC 
   LIMIT 10;
   ```

3. O simplemente desactiva la confirmación (Opción 1) para desarrollo

## ✅ Configuración recomendada para desarrollo:

**Desactivar "Enable email confirmations"** es lo más simple y rápido para desarrollo local.

Podrás reactivarlo más tarde cuando subas a producción y tengas SMTP configurado.

## 📧 Estado actual:

- ✅ Supabase configurado
- ✅ Variables de entorno correctas
- ❌ SMTP no configurado (emails no se envían)
- 🔧 Solución: Desactivar confirmación de email para desarrollo

---

## Después de desactivar la confirmación:

1. Los usuarios se registrarán inmediatamente sin verificación
2. Podrán hacer login de inmediato
3. No recibirán emails de confirmación
4. Perfecto para desarrollo y testing

Cuando subas a producción, reactiva la confirmación y configura SMTP.
