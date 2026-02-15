# 🚀 Guía de Deployment - CodeAcademy

## Deployment en Vercel (Recomendado)

### Prerrequisitos

- [ ] Cuenta de GitHub
- [ ] Cuenta de Vercel
- [ ] Supabase proyecto creado
- [ ] Stripe configurado en Live Mode
- [ ] Domain registrado (opcional)

---

## 📋 Paso 1: Preparar el Repositorio

### 1.1 Inicializar Git (si no está hecho)

```bash
cd /home/dario/codeacademy
git init
git add .
git commit -m "Initial commit: CodeAcademy MVP AAA"
```

### 1.2 Crear Repositorio en GitHub

1. Ir a [github.com/new](https://github.com/new)
2. Nombre: `codeacademy`
3. Privado o Público (tu elección)
4. NO inicializar con README

```bash
git remote add origin https://github.com/TU_USUARIO/codeacademy.git
git branch -M main
git push -u origin main
```

### 1.3 Verificar .gitignore

```bash
cat .gitignore
```

Debe incluir:
```
node_modules/
.next/
.env.local
.env*.local
.vercel
.turbo
```

---

## 📋 Paso 2: Configurar Vercel

### 2.1 Conectar con GitHub

1. Ir a [vercel.com](https://vercel.com)
2. Login con GitHub
3. Click "Add New" → "Project"
4. Importar tu repositorio `codeacademy`

### 2.2 Configurar Build Settings

```
Framework Preset: Next.js
Root Directory: apps/web
Build Command: cd ../.. && turbo run build --filter=@codeacademy/web
Output Directory: .next
Install Command: npm install --legacy-peer-deps
```

### 2.3 Variables de Entorno

Ir a Project Settings → Environment Variables

**Copiar desde `.env.production.example`:**

#### Supabase
```bash
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGci...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGci...
```

#### Stripe (LIVE MODE)
```bash
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...  # Configurar después
```

#### Precios Stripe
```bash
NEXT_PUBLIC_PRICE_STARTER_MONTHLY=price_...
NEXT_PUBLIC_PRICE_STARTER_YEARLY=price_...
NEXT_PUBLIC_PRICE_PRO_MONTHLY=price_...
NEXT_PUBLIC_PRICE_PRO_YEARLY=price_...
NEXT_PUBLIC_PRICE_FAMILIA_MONTHLY=price_...
NEXT_PUBLIC_PRICE_FAMILIA_YEARLY=price_...
```

#### App
```bash
NEXT_PUBLIC_APP_URL=https://codeacademy.dev
NEXT_PUBLIC_ENVIRONMENT=production
NEXTAUTH_URL=https://codeacademy.dev
NEXTAUTH_SECRET=generar_uno_nuevo_aqui
NODE_ENV=production
```

**Generar NEXTAUTH_SECRET:**
```bash
openssl rand -base64 32
```

### 2.4 Deploy

```bash
# Click "Deploy"
# Esperar 2-5 minutos
```

Tu app estará en: `https://tu-proyecto.vercel.app`

---

## 📋 Paso 3: Configurar Dominio Personalizado

### 3.1 Añadir Dominio en Vercel

1. Project Settings → Domains
2. Añadir: `codeacademy.dev` y `www.codeacademy.dev`

### 3.2 Configurar DNS

En tu proveedor de dominios (Namecheap, GoDaddy, etc.):

**Registros A:**
```
@ → 76.76.21.21
www → 76.76.21.98
```

**O CNAME (alternativo):**
```
www → cname.vercel-dns.com
```

### 3.3 Esperar Propagación

- DNS: 1-48 horas
- SSL: Automático (Let's Encrypt)

---

## 📋 Paso 4: Configurar Stripe Production

### 4.1 Activar Live Mode

Dashboard Stripe → Toggle "Test Mode" OFF

### 4.2 Configurar Webhook Production

1. Developers → Webhooks → "Add endpoint"
2. URL: `https://codeacademy.dev/api/stripe/webhook`
3. Eventos a escuchar:
   ```
   checkout.session.completed
   customer.subscription.created
   customer.subscription.updated
   customer.subscription.deleted
   invoice.paid
   invoice.payment_failed
   ```
4. Copiar el **Signing secret** (whsec_...)
5. Actualizar en Vercel:
   ```
   STRIPE_WEBHOOK_SECRET=whsec_...
   ```

### 4.3 Verificar Productos

```bash
# Ejecutar en tu máquina local con Live keys
STRIPE_SECRET_KEY=sk_live_... node apps/web/scripts/setup-stripe.js
```

### 4.4 Configurar Customer Portal

1. Settings → Billing → Customer Portal
2. Activar:
   - Update payment method
   - View invoices
   - Cancel subscription
3. Branding:
   - Logo
   - Colores
   - Email de soporte

---

## 📋 Paso 5: Configurar Supabase Production

### 5.1 Verificar RLS Policies

```sql
-- En SQL Editor
-- Verificar que todas las tablas tengan RLS activado
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename NOT IN (
  SELECT tablename FROM pg_policies
);
```

### 5.2 Configurar Auth

1. Authentication → Settings
2. Site URL: `https://codeacademy.dev`
3. Redirect URLs:
   ```
   https://codeacademy.dev/**
   https://codeacademy.dev/auth/callback
   ```

### 5.3 Email Templates

1. Authentication → Email Templates
2. Personalizar:
   - Confirm signup
   - Magic Link
   - Change Email
   - Reset Password

---

## 📋 Paso 6: Monitoring y Analytics

### 6.1 Vercel Analytics

```bash
npm install @vercel/analytics --legacy-peer-deps
```

`apps/web/src/app/layout.tsx`:
```typescript
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### 6.2 Sentry (Error Tracking)

```bash
npm install @sentry/nextjs --legacy-peer-deps
npx @sentry/wizard@latest -i nextjs
```

Configurar en Vercel:
```bash
SENTRY_DSN=https://...
SENTRY_AUTH_TOKEN=...
```

### 6.3 PostHog (Product Analytics)

```bash
npm install posthog-js --legacy-peer-deps
```

Crear `apps/web/src/lib/posthog.ts`:
```typescript
import posthog from 'posthog-js';

export function initPostHog() {
  if (typeof window !== 'undefined') {
    posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
      api_host: 'https://app.posthog.com',
    });
  }
}
```

---

## 📋 Paso 7: SEO y Performance

### 7.1 Verificar SEO

```bash
# Google Search Console
https://search.google.com/search-console

# Añadir propiedad: codeacademy.dev
# Verificar con método DNS o archivo HTML
```

### 7.2 Sitemap

Crear `apps/web/src/app/sitemap.ts`:
```typescript
import { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://codeacademy.dev',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: 'https://codeacademy.dev/pricing',
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    // ... más páginas
  ];
}
```

### 7.3 Performance Audit

```bash
# Lighthouse en Chrome DevTools
# O usar:
npm install -g lighthouse

lighthouse https://codeacademy.dev --view
```

**Targets:**
- Performance: >90
- Accessibility: >95
- Best Practices: >90
- SEO: >95

---

## 📋 Paso 8: Testing en Producción

### 8.1 Smoke Tests

- [ ] Landing page carga correctamente
- [ ] Navegación funciona
- [ ] Pricing muestra planes
- [ ] Checkout redirect a Stripe
- [ ] Webhook recibe eventos
- [ ] Dashboard carga (después de login)
- [ ] Panel parental accesible

### 8.2 Test de Pago Real

**⚠️ Usar tarjeta real en pequeña cantidad**

1. Ir a `/pricing`
2. Seleccionar plan Starter
3. Completar checkout
4. Verificar:
   - Email de confirmación
   - Dashboard actualizado
   - Stripe Dashboard muestra pago
   - Supabase actualizado

5. Cancelar suscripción de prueba

---

## 📋 Paso 9: Backup y Seguridad

### 9.1 Backup de Base de Datos

Supabase → Settings → Database → Point in Time Recovery

Activar backups automáticos

### 9.2 Secrets Rotation

Programar rotación cada 90 días:
- [ ] NEXTAUTH_SECRET
- [ ] SUPABASE_SERVICE_ROLE_KEY
- [ ] STRIPE_SECRET_KEY

### 9.3 Rate Limiting

Vercel automáticamente incluye:
- DDoS protection
- Rate limiting por IP
- Edge caching

---

## 📋 Paso 10: Go Live! 🚀

### 10.1 Checklist Final

- [ ] Dominio funcionando con SSL
- [ ] Todas las variables de entorno configuradas
- [ ] Stripe webhooks recibiendo eventos
- [ ] Supabase Auth funcionando
- [ ] Email templates personalizados
- [ ] Analytics instalado
- [ ] Error tracking configurado
- [ ] Sitemap generado
- [ ] robots.txt correcto
- [ ] SEO metadata completa
- [ ] Performance >90
- [ ] Tests de pago exitosos

### 10.2 Anuncio

```bash
# Twitter
🚀 ¡CodeAcademy está LIVE!

Aprende programación con gamificación real
✅ Cursos para todas las edades
✅ Python, JS, C#, Unity
✅ 14 días gratis

👉 https://codeacademy.dev

# LinkedIn, Facebook, etc.
```

### 10.3 Monitoring Post-Launch

Primeras 24 horas:
- Revisar Vercel Analytics cada 2h
- Monitorear Sentry para errores
- Verificar Stripe Dashboard
- Responder feedback usuarios

---

## 🔧 Troubleshooting

### Build Failed

```bash
# Ver logs completos
vercel logs --follow

# Rebuild localmente
npm run build

# Limpiar cache
vercel --force
```

### Stripe Webhook No Funciona

```bash
# Verificar signature
curl https://codeacademy.dev/api/stripe/webhook

# Ver logs en Stripe Dashboard
Developers → Webhooks → [tu endpoint] → Events
```

### Variables de Entorno No Aplican

```bash
# Redeploy forzado
vercel --prod --force

# O desde dashboard:
Deployments → [...] → Redeploy
```

---

## 📈 Métricas de Éxito

### Mes 1
- 🎯 100 usuarios registrados
- 🎯 20 suscriptores de pago
- 🎯 €500 MRR
- 🎯 <1% error rate

### Mes 3
- 🎯 500 usuarios registrados
- 🎯 100 suscriptores
- 🎯 €3,000 MRR
- 🎯 80% retention

### Mes 6
- 🎯 2,000 usuarios
- 🎯 400 suscriptores
- 🎯 €12,000 MRR
- 🎯 Product-market fit

---

## 📚 Recursos

- [Vercel Docs](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Stripe Go Live](https://stripe.com/docs/development/checklist)
- [Supabase Production](https://supabase.com/docs/guides/platform/going-into-prod)

---

**¡Éxito con tu lanzamiento! 🎉**
