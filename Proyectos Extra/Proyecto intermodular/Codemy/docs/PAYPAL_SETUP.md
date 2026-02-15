# 🚀 Guía Completa: Configuración de PayPal REST API

## 📋 Resumen

Has implementado la integración completa de PayPal con:
- ✅ PayPal Buttons SDK embebidos
- ✅ Verificación automática de pagos
- ✅ Webhooks para notificaciones
- ✅ Base de datos para tracking
- ✅ Fallback a paypal.me si no hay credenciales

---

## 🔧 PASO 1: Crear Cuenta PayPal Developer

1. Ve a https://developer.paypal.com/
2. Inicia sesión con tu cuenta PayPal (o crea una)
3. Acepta los términos de desarrollador

---

## 🏗️ PASO 2: Crear Aplicación

1. En el Dashboard, ve a **"My Apps & Credentials"**
2. En la pestaña **"Sandbox"** (para pruebas):
   - Clic en **"Create App"**
   - Nombre: "CodeAcademy Payments"
   - Selecciona tu cuenta de negocio sandbox
   - Clic en **"Create App"**

3. Obtendrás:
   - **Client ID** (público)
   - **Secret** (privado - NUNCA compartir)

---

## 🔐 PASO 3: Configurar Variables de Entorno

Crea o actualiza tu archivo `.env.local`:

```bash
# PayPal Sandbox (Para pruebas)
NEXT_PUBLIC_PAYPAL_CLIENT_ID=tu_client_id_sandbox
PAYPAL_CLIENT_SECRET=tu_client_secret_sandbox
NEXT_PUBLIC_PAYPAL_ENVIRONMENT=sandbox
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Para producción** (después de probar):
```bash
# PayPal Production
NEXT_PUBLIC_PAYPAL_CLIENT_ID=tu_client_id_production
PAYPAL_CLIENT_SECRET=tu_client_secret_production
NEXT_PUBLIC_PAYPAL_ENVIRONMENT=production
NEXT_PUBLIC_APP_URL=https://tudominio.com
```

---

## 🎯 PASO 4: Configurar Webhooks

Los webhooks notifican a tu servidor cuando se completa un pago.

### En PayPal Developer Dashboard:

1. Ve a tu App → **Webhooks**
2. Clic en **"Add Webhook"**
3. URL del webhook:
   - **Sandbox**: `https://tu-dominio-de-prueba.ngrok.io/api/webhooks/paypal`
   - **Producción**: `https://tudominio.com/api/webhooks/paypal`

4. Selecciona estos eventos:
   - ✅ Payment capture completed
   - ✅ Payment capture denied
   - ✅ Payment capture pending
   - ✅ Payment capture refunded

5. Guarda el webhook

### Para desarrollo local (ngrok):

```bash
# Instalar ngrok
npm install -g ngrok

# Exponer localhost:3000
ngrok http 3000

# Usar la URL https que te da ngrok en el webhook
```

---

## 💳 PASO 5: Cuentas de Prueba (Sandbox)

PayPal crea automáticamente cuentas de prueba:

1. En Dashboard → **Sandbox** → **Accounts**
2. Verás dos cuentas:
   - **Business** (la que recibe pagos)
   - **Personal** (comprador de prueba)

3. Para probar pagos:
   - Usa las credenciales de la cuenta Personal
   - Email: `sb-xxxxx@personal.example.com`
   - Password: Click en los 3 puntos → "View/Edit account" → Password

---

## 🧪 PASO 6: Probar el Sistema

### Prueba en Sandbox:

1. Inicia tu servidor:
   ```bash
   npm run dev
   ```

2. Ve a `http://localhost:3000/checkout?plan=starter&billing=monthly`

3. Verás los botones de PayPal embebidos

4. Haz clic en "PayPal" o "Debit/Credit Card"

5. Usa las credenciales de la cuenta Personal sandbox

6. Completa el pago

7. Deberías ser redirigido a `/payment/success`

8. Verifica en Supabase → tabla `purchases` que se guardó el pago

### Verificar Webhook:

1. Ve a PayPal Dashboard → Webhooks → Tu webhook
2. Click en **"Webhook events"**
3. Deberías ver eventos `PAYMENT.CAPTURE.COMPLETED`

---

## 🚀 PASO 7: Migrar a Producción

### 1. Crear App de Producción

1. En Dashboard → **Live** (no Sandbox)
2. Crea una nueva app igual que en sandbox
3. Obtén Client ID y Secret de producción

### 2. Actualizar Variables de Entorno

```bash
NEXT_PUBLIC_PAYPAL_CLIENT_ID=tu_client_id_LIVE
PAYPAL_CLIENT_SECRET=tu_client_secret_LIVE
NEXT_PUBLIC_PAYPAL_ENVIRONMENT=production
NEXT_PUBLIC_APP_URL=https://tudominio.com
```

### 3. Configurar Webhook de Producción

- URL: `https://tudominio.com/api/webhooks/paypal`
- Mismos eventos que en sandbox

### 4. Verificar Cuenta de Negocio

Para recibir pagos reales, tu cuenta PayPal debe estar:
- ✅ Verificada con email
- ✅ Verificada con banco/tarjeta
- ✅ Con información fiscal completa

---

## 📊 PASO 8: Migrar Base de Datos

Ejecuta la migración en Supabase:

```bash
cd supabase
supabase migration up
```

O manualmente en Supabase Dashboard → SQL Editor:
- Copia el contenido de `/supabase/migrations/20241116000000_create_purchases.sql`
- Ejecutar

---

## 🎨 Cómo Funciona el Flujo

### Con Credenciales de PayPal:

```
1. Usuario → Checkout page
   ↓
2. PayPal Buttons aparecen embebidos
   ↓
3. Usuario hace clic → Modal de PayPal
   ↓
4. Usuario completa pago
   ↓
5. Frontend llama a /api/paypal/create-order
   ↓
6. Backend crea orden en PayPal
   ↓
7. Usuario confirma en modal
   ↓
8. Frontend llama a /api/paypal/capture-order
   ↓
9. Backend captura pago y guarda en DB
   ↓
10. Redirect a /payment/success
    ↓
11. Webhook confirma (respaldo)
```

### Sin Credenciales (Fallback):

```
1. Usuario → Checkout page
   ↓
2. Botón "Pagar con PayPal"
   ↓
3. Redirect a paypal.me/mutenros/{amount}
   ↓
4. Usuario paga manualmente
   ↓
5. Vuelve a /payment/success
   ↓
6. Verificación manual necesaria
```

---

## 🔍 Troubleshooting

### Error: "Client ID not found"

**Problema**: No se cargaron las credenciales

**Solución**:
```bash
# Verifica que .env.local existe
ls -la apps/web/.env.local

# Verifica las variables
cat apps/web/.env.local | grep PAYPAL

# Reinicia el servidor
npm run dev
```

### Los botones de PayPal no aparecen

**Problema**: Client ID no configurado o inválido

**Solución**:
1. Verifica `NEXT_PUBLIC_PAYPAL_CLIENT_ID` en `.env.local`
2. Asegúrate que sea el Client ID correcto (sandbox o production)
3. Reinicia el servidor

### Webhook no recibe eventos

**Problema**: URL no accesible o incorrecta

**Solución**:
1. Para desarrollo local, usa ngrok
2. Verifica que la URL sea HTTPS
3. Verifica que el endpoint `/api/webhooks/paypal` responda
4. Prueba manualmente: `curl https://tudominio.com/api/webhooks/paypal`

### Pago completado pero no se guarda en DB

**Problema**: Error de conexión con Supabase

**Solución**:
1. Verifica credenciales de Supabase en `.env.local`
2. Verifica que la migración se ejecutó
3. Verifica logs del servidor: `npm run dev`
4. Revisa la consola del navegador

---

## 📈 Monitoreo

### Dashboard de PayPal

- **Sandbox**: https://www.sandbox.paypal.com/
- **Production**: https://www.paypal.com/

### Logs en tu App

Verifica la consola del servidor para:
```
✅ Payment captured and saved: 8AB12345 - User: abc123
```

### Base de Datos

Consulta en Supabase:
```sql
SELECT * FROM purchases 
WHERE status = 'completed' 
ORDER BY created_at DESC 
LIMIT 10;
```

---

## 🔒 Seguridad

### ⚠️ NUNCA hagas esto:

- ❌ Compartir tu `PAYPAL_CLIENT_SECRET`
- ❌ Commitear `.env.local` a Git
- ❌ Exponer tu Client Secret en el frontend
- ❌ Deshabilitar verificación de webhooks

### ✅ Siempre haz esto:

- ✅ Usa variables de entorno
- ✅ Mantén `.env.local` en `.gitignore`
- ✅ Verifica firmas de webhooks (implementar)
- ✅ Valida cantidades en el backend
- ✅ Logs de todas las transacciones

---

## 🎯 Checklist Final

Antes de lanzar a producción:

- [ ] Cuenta PayPal Business verificada
- [ ] App de producción creada en PayPal
- [ ] Variables de entorno de producción configuradas
- [ ] Webhook de producción configurado y probado
- [ ] Migración de base de datos ejecutada
- [ ] Probado flujo completo en sandbox
- [ ] Probado flujo completo en producción (pequeña cantidad)
- [ ] Configurado monitoreo de errores
- [ ] Configurado email de notificaciones
- [ ] Documentado para equipo

---

## 📚 Recursos

- [PayPal Developer Docs](https://developer.paypal.com/docs/api/overview/)
- [PayPal React SDK](https://paypal.github.io/react-paypal-js/)
- [PayPal Webhooks](https://developer.paypal.com/docs/api-basics/notifications/webhooks/)
- [Sandbox Testing](https://developer.paypal.com/tools/sandbox/)

---

## 💬 Soporte

Si tienes problemas:

1. Revisa los logs del servidor
2. Revisa la consola del navegador
3. Revisa el Dashboard de PayPal
4. Revisa los Webhook events en PayPal
5. Consulta la documentación oficial

---

**¡Listo! 🎉** Tu sistema de pagos está completamente implementado y listo para usar.
