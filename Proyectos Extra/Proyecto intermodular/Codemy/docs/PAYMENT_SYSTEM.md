/**
 * DOCUMENTACIÓN: Sistema de Pagos con PayPal
 * 
 * Este documento explica cómo funciona el sistema de verificación de pagos
 * y activación de acceso premium en Codemy.
 */

## 📋 ARQUITECTURA DEL SISTEMA

### 1. Base de Datos (Supabase)

**Tabla: `purchases`**
- Almacena todas las compras y suscripciones
- Campos clave:
  - `user_id`: Referencia al usuario
  - `type`: 'subscription' o 'product'
  - `plan_id`: 'starter', 'pro', 'family'
  - `product_id`: ID del skill tree comprado
  - `paypal_transaction_id`: ID único de PayPal
  - `status`: 'pending', 'completed', 'failed', 'refunded'
  - `expires_at`: Fecha de expiración (suscripciones)

**Funciones SQL:**
- `has_active_subscription(user_id, plan_id)`: Verifica suscripción activa
- `has_product_access(user_id, product_id)`: Verifica producto comprado
- `get_active_subscription(user_id)`: Obtiene detalles de suscripción
- `get_user_products(user_id)`: Lista productos del usuario

### 2. Flujo de Pago

```
1. Usuario selecciona plan/producto
   ↓
2. Página /checkout
   - Muestra resumen
   - Guarda datos en localStorage
   ↓
3. Redirect a PayPal.me/mutenros/{amount}
   - Usuario paga en PayPal
   ↓
4. Usuario vuelve a /payment/success
   - Muestra confirmación
   - Espera activación
   ↓
5. Webhook de PayPal (/api/webhooks/paypal)
   - Recibe notificación de pago
   - Valida transacción
   - Inserta en tabla purchases
   - Marca como 'completed'
   ↓
6. Acceso activado automáticamente
```

### 3. Verificación de Acceso

**Helpers en `/lib/access-control.ts`:**

```typescript
// Verificar suscripción activa
await hasActiveSubscription(userId, planId?)

// Verificar producto comprado
await hasProductAccess(productId, userId?)

// Obtener plan del usuario
await getUserPlanLevel(userId?) // 'free', 'starter', 'pro', 'family'

// Verificar permisos específicos
await canCreateSeminars(userId?) // Requiere Pro/Family
await canShareAccount(userId?)   // Requiere Family

// Verificar acceso premium (suscripción O compra)
await hasPremiumAccess(productId, userId?)
```

**Uso en componentes:**

```typescript
import { hasActiveSubscription, hasProductAccess } from '@/lib/access-control';

// En Server Component
const hasAccess = await hasActiveSubscription();
if (!hasAccess) {
  redirect('/checkout?plan=starter');
}

// En API Route
const canAccess = await hasProductAccess('python', userId);
if (!canAccess) {
  return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
}
```

### 4. Configuración de PayPal

**⚠️ IMPORTANTE: PayPal.me NO soporta webhooks automáticos**

Tienes 3 opciones:

#### Opción A: PayPal Standard (Actual - Manual)
- Usar PayPal.me para pagos simples
- Usuario confirma pago en /payment/success
- Admin verifica manualmente en panel PayPal
- Activa acceso manualmente en Supabase

#### Opción B: PayPal IPN (Semi-automático)
1. Ir a PayPal.com → Account Settings → Notifications
2. Configurar IPN URL: `https://tudominio.com/api/webhooks/paypal`
3. PayPal enviará notificaciones POST cuando reciba pagos
4. El webhook procesa automáticamente

#### Opción C: PayPal REST API + Buttons (Recomendado)
1. Crear app en https://developer.paypal.com/
2. Obtener Client ID y Secret
3. Usar PayPal Buttons SDK en checkout
4. Configurar webhooks en Dashboard
5. Activación 100% automática

**Para implementar Opción C:**

```bash
npm install @paypal/react-paypal-js
```

Actualizar checkout page:

```typescript
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";

<PayPalScriptProvider options={{ 
  "client-id": process.env.NEXT_PUBLIC_PAYPAL_CLIENT_ID 
}}>
  <PayPalButtons
    createOrder={(data, actions) => {
      return actions.order.create({
        purchase_units: [{
          amount: { value: price.toString() },
          custom_id: JSON.stringify({
            userId, planId, billing, productId
          })
        }]
      });
    }}
    onApprove={async (data, actions) => {
      // Capturar pago
      const order = await actions.order.capture();
      // Redirigir a success
      router.push('/payment/success');
    }}
  />
</PayPalScriptProvider>
```

### 5. Panel de Administración (Próximo)

Crear `/admin/payments` para:
- Ver pagos pendientes de verificación
- Aprobar/rechazar manualmente
- Ver estadísticas de suscripciones
- Gestionar reembolsos

### 6. Migraciones Supabase

**Ejecutar migración:**

```bash
cd codeacademy/supabase
supabase migration up
```

O manualmente en Supabase Dashboard → SQL Editor:
- Copiar contenido de `migrations/20241116000000_create_purchases.sql`
- Ejecutar

### 7. Variables de Entorno

Añadir a `.env.local`:

```env
# PayPal (cuando uses REST API)
NEXT_PUBLIC_PAYPAL_CLIENT_ID=tu_client_id
PAYPAL_CLIENT_SECRET=tu_secret

# Supabase
NEXT_PUBLIC_SUPABASE_URL=tu_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu_key
SUPABASE_SERVICE_ROLE_KEY=tu_service_key
```

### 8. Testing

**Test manual del flujo:**

1. Ir a `/checkout?plan=starter&billing=monthly`
2. Clic en "Pagar con PayPal"
3. Completar pago en PayPal Sandbox
4. Volver a /payment/success
5. Verificar en Supabase → tabla `purchases`

**Verificar acceso:**

```typescript
import { hasActiveSubscription } from '@/lib/access-control';

const subscription = await hasActiveSubscription();
console.log('Has access:', subscription);
```

### 9. Seguridad

**Webhook debe verificar:**
- Firma de PayPal (header PayPal-Transmission-Sig)
- IP de PayPal (whitelist)
- Transaction ID único (no duplicados)

**Agregar a webhook:**

```typescript
// Verificar firma PayPal
const isValid = await verifyPayPalSignature(request.headers);
if (!isValid) {
  return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
}
```

### 10. Roadmap

**Fase 1 (Actual):**
- ✅ Base de datos purchases
- ✅ Webhook endpoint
- ✅ Helpers de verificación
- ✅ Página de success
- ⚠️ Verificación manual

**Fase 2 (Próximo):**
- [ ] PayPal REST API integration
- [ ] Webhooks automáticos
- [ ] Panel de admin
- [ ] Emails de confirmación

**Fase 3 (Futuro):**
- [ ] Renovaciones automáticas
- [ ] Gestión de reembolsos
- [ ] Facturación automática
- [ ] Analytics de conversión

---

## 🚀 QUICK START

1. **Migrar base de datos:**
   ```bash
   supabase migration up
   ```

2. **Configurar PayPal IPN:**
   - PayPal.com → Notifications
   - URL: `https://codemy.com/api/webhooks/paypal`

3. **Probar checkout:**
   - Navegar a `/checkout?plan=starter`
   - Completar pago
   - Verificar en Supabase

4. **Verificar acceso en código:**
   ```typescript
   const hasAccess = await hasActiveSubscription();
   ```

## 📞 SOPORTE

Si necesitas ayuda:
- Email: soporte@codemy.com
- Docs: /docs/payments
- Slack: #payments
