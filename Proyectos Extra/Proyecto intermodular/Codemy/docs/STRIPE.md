# 💳 Stripe Integration - CodeAcademy

Sistema completo de pagos y suscripciones integrado con Stripe.

## 📋 Configuración Inicial

### 1. Crear Cuenta Stripe

1. Regístrate en [Stripe](https://stripe.com)
2. Activa el modo de prueba (Test Mode)
3. Obtén tus API Keys en Dashboard > Developers > API Keys

### 2. Variables de Entorno

Copia y completa en `.env.local`:

```bash
# Stripe Keys
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx  # Después de configurar webhook
```

### 3. Configurar Productos y Precios

Ejecuta el script de setup:

```bash
cd apps/web
node scripts/setup-stripe.js
```

Esto creará automáticamente:
- ✅ 3 productos (Starter, Pro, Familia)
- ✅ 6 precios (mensual y anual para cada plan)
- ✅ IDs para agregar a `.env.local`

### 4. Configurar Webhooks

1. Instala Stripe CLI:
```bash
# Linux
curl -s https://packages.stripe.com/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg
echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.com/stripe-cli-debian-local stable main" | sudo tee -a /etc/apt/sources.list.d/stripe.list
sudo apt update
sudo apt install stripe

# macOS
brew install stripe/stripe-cli/stripe
```

2. Login en Stripe CLI:
```bash
stripe login
```

3. Configurar webhook local (desarrollo):
```bash
stripe listen --forward-to localhost:3000/api/stripe/webhook
```

Copia el `webhook secret` (whsec_xxx) a `.env.local`

4. Configurar webhook producción:
   - Ve a Dashboard > Developers > Webhooks
   - Añade endpoint: `https://tudominio.com/api/stripe/webhook`
   - Selecciona eventos:
     - `checkout.session.completed`
     - `customer.subscription.created`
     - `customer.subscription.updated`
     - `customer.subscription.deleted`
     - `invoice.paid`
     - `invoice.payment_failed`

## 🏗️ Arquitectura

### Flujo de Checkout

```
Usuario → PricingCard → useStripe Hook → /api/stripe/checkout
         ↓
Stripe Checkout Session ← Stripe API
         ↓
Usuario completa pago
         ↓
Webhook → /api/stripe/webhook → Actualiza DB
         ↓
Usuario redirigido → /dashboard
```

### Estructura de Archivos

```
apps/web/
├── src/
│   ├── lib/
│   │   └── stripe.ts              # Configuración y helpers
│   ├── hooks/
│   │   └── useStripe.ts           # Hook para checkout y billing
│   ├── components/
│   │   ├── PricingCard.tsx        # Tarjeta de plan con Stripe
│   │   └── SubscriptionManager.tsx # Gestión de suscripción
│   └── app/
│       └── api/
│           ├── stripe/
│           │   ├── checkout/route.ts   # Crear sesión
│           │   ├── webhook/route.ts    # Procesar eventos
│           │   └── portal/route.ts     # Customer Portal
│           └── subscription/route.ts    # CRUD suscripciones
└── scripts/
    └── setup-stripe.js            # Setup inicial
```

## 🎯 Planes y Precios

### Plan Starter - €19.90/mes
- 1 estudiante
- Acceso completo a cursos
- Certificados digitales
- Comunidad privada

### Plan Pro - €39.90/mes
- Todo lo de Starter
- Talleres en vivo
- Mentoría 1-a-1
- Proyectos premium
- Acceso anticipado

### Plan Familia - €79.90/mes
- Hasta 4 estudiantes
- Todo lo de Pro
- Panel parental
- Reportes de progreso
- Control de contenido

**Ahorro Anual:** 16% pagando anualmente

**Trial:** 14 días gratis en todos los planes

## 🔧 Uso en Componentes

### Checkout desde Pricing

```tsx
import { PricingCard } from '@/components/PricingCard';

export default function PricingPage() {
  return (
    <PricingCard
      name="Plan Pro"
      description="Perfecto para estudiantes avanzados"
      price={{ monthly: 39.90, yearly: 399 }}
      priceIds={{
        monthly: process.env.NEXT_PUBLIC_PRICE_PRO_MONTHLY!,
        yearly: process.env.NEXT_PUBLIC_PRICE_PRO_YEARLY!,
      }}
      features={[
        'Acceso completo a todos los cursos',
        'Talleres en vivo semanales',
        // ...
      ]}
      planType="pro"
      userId={user?.id}
      popular
    />
  );
}
```

### Gestión de Suscripción

```tsx
import { SubscriptionManager } from '@/components/SubscriptionManager';

export default function SettingsPage() {
  return (
    <div>
      <h1>Configuración</h1>
      <SubscriptionManager userId={user.id} />
    </div>
  );
}
```

### Hook useStripe

```tsx
'use client';

import { useStripe } from '@/hooks/useStripe';

export function MyComponent() {
  const { createCheckoutSession, loading, error } = useStripe();

  const handleSubscribe = async () => {
    await createCheckoutSession({
      priceId: 'price_xxx',
      userId: 'user_123',
      planType: 'pro',
      billingInterval: 'monthly',
    });
  };

  return (
    <button onClick={handleSubscribe} disabled={loading}>
      {loading ? 'Procesando...' : 'Suscribirse'}
    </button>
  );
}
```

## 🧪 Testing

### Test Mode

Usa estas tarjetas de prueba:

```
✅ Éxito:          4242 4242 4242 4242
❌ Declined:       4000 0000 0000 0002
⚠️ Requiere SCA:   4000 0025 0000 3155

CVC: Cualquier 3 dígitos
Fecha: Cualquier fecha futura
```

### Webhooks Locales

```bash
# Terminal 1: App
npm run dev

# Terminal 2: Stripe CLI
stripe listen --forward-to localhost:3000/api/stripe/webhook

# Terminal 3: Trigger eventos de prueba
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
```

## 📊 Customer Portal

Stripe Customer Portal permite a los usuarios:

- ✅ Ver historial de pagos
- ✅ Actualizar método de pago
- ✅ Cambiar plan
- ✅ Cancelar suscripción
- ✅ Descargar facturas

Configuración:
1. Dashboard > Settings > Billing > Customer Portal
2. Activa funcionalidades que necesites
3. Personaliza branding

## 🔒 Seguridad

### Validación de Webhooks

```typescript
// Siempre verifica la firma
const signature = headers().get('stripe-signature');
const event = stripe.webhooks.constructEvent(
  body,
  signature,
  webhookSecret
);
```

### Keys Seguras

- ❌ NUNCA expongas `STRIPE_SECRET_KEY` en frontend
- ✅ Solo `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` es público
- ✅ Webhook secret debe estar en variables de entorno

### Row Level Security (RLS)

```sql
-- Solo el usuario puede ver su suscripción
CREATE POLICY "Users can view own subscription"
  ON subscriptions FOR SELECT
  USING (auth.uid() = user_id);
```

## 📈 Monitoreo

### Dashboard Stripe

- Pagos en tiempo real
- Métricas de suscripciones
- Tasa de churn
- MRR (Monthly Recurring Revenue)
- Customer Lifetime Value

### Logs

```bash
# Ver logs de webhooks
stripe logs tail

# Ver eventos específicos
stripe events list --limit 10
```

## 🚀 Producción

### Checklist

- [ ] Cambiar a Live Mode en Stripe
- [ ] Actualizar keys en producción (pk_live_, sk_live_)
- [ ] Configurar webhook production endpoint
- [ ] Configurar Customer Portal branding
- [ ] Habilitar emails transaccionales
- [ ] Configurar tax collection (si aplica)
- [ ] Setup Stripe Radar (anti-fraud)
- [ ] Revisar términos y condiciones
- [ ] Test checkout flow end-to-end

### Variables de Entorno Producción

```bash
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx  # Endpoint producción
```

## 🆘 Troubleshooting

### Webhook no recibe eventos

```bash
# Verificar endpoint
curl -X POST https://tudominio.com/api/stripe/webhook

# Ver logs
stripe logs tail --filter-event-type customer.subscription.created
```

### Error "No such price"

Verifica que los IDs en `.env.local` coincidan con Stripe Dashboard.

### Customer duplicado

Siempre busca customer existente antes de crear:

```typescript
const customers = await stripe.customers.list({ email });
const customer = customers.data[0] || await stripe.customers.create({ email });
```

## 📚 Recursos

- [Stripe Docs](https://stripe.com/docs)
- [Stripe Testing](https://stripe.com/docs/testing)
- [Webhooks Guide](https://stripe.com/docs/webhooks)
- [Customer Portal](https://stripe.com/docs/billing/subscriptions/customer-portal)

---

**¿Necesitas ayuda?** Contacta al equipo de desarrollo o consulta la [documentación de Stripe](https://stripe.com/docs).
