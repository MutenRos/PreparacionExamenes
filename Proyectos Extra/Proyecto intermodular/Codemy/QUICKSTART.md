# 🚀 Guía de Inicio Rápido - CodeAcademy

## ⚡ Comenzar en 5 Minutos

### 1️⃣ Clonar e Instalar

```bash
cd /home/dario/codeacademy
npm install --legacy-peer-deps
```

### 2️⃣ Configurar Variables de Entorno

```bash
# Copiar archivos de ejemplo
cp .env.example .env.local

# Editar con tus valores
nano .env.local
```

**Mínimo requerido para desarrollo:**
```bash
# Supabase (local o cloud)
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu_anon_key

# Stripe (test mode)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
```

### 3️⃣ Iniciar Servidor de Desarrollo

```bash
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000) 🎉

---

## 🗄️ Setup Base de Datos (Supabase)

### Opción A: Supabase Cloud (Recomendado)

1. **Crear cuenta**: [supabase.com](https://supabase.com)
2. **Nuevo proyecto**: Click "New Project"
3. **Copiar credenciales**:
   - Project URL → `NEXT_PUBLIC_SUPABASE_URL`
   - Anon Key → `NEXT_PUBLIC_SUPABASE_ANON_KEY`

4. **Ejecutar migrations**:
```bash
# En SQL Editor de Supabase
# Pega el contenido de:
cat packages/database/schema.sql
```

### Opción B: Supabase Local

```bash
# Instalar Supabase CLI
brew install supabase/tap/supabase  # macOS
# o
npm install -g supabase             # npm

# Iniciar
supabase start

# Aplicar schema
supabase db push
```

---

## 💳 Setup Stripe

### 1. Crear Cuenta Stripe

1. Ir a [stripe.com](https://stripe.com)
2. Registrarse / Login
3. Activar **Test Mode** (toggle arriba derecha)

### 2. Obtener API Keys

Dashboard → Developers → API Keys:
- **Publishable key** → `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
- **Secret key** → `STRIPE_SECRET_KEY`

### 3. Crear Productos

```bash
cd apps/web
node scripts/setup-stripe.js
```

Este script:
- ✅ Crea 3 productos (Starter, Pro, Familia)
- ✅ Crea 6 precios (mensual + anual)
- ✅ Te da los IDs para `.env.local`

### 4. Configurar Webhook (Local)

**Terminal 1** (App):
```bash
npm run dev
```

**Terminal 2** (Stripe):
```bash
# Instalar Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks
stripe listen --forward-to localhost:3000/api/stripe/webhook
```

Copia el **webhook secret** (whsec_xxx) a `.env.local`:
```bash
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

---

## 📝 Archivo .env.local Completo

```bash
# =============================================
# CodeAcademy - Configuración de Desarrollo
# =============================================

# ===== SUPABASE =====
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxx
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxx

# ===== STRIPE =====
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# ===== PRECIOS STRIPE (después de setup-stripe.js) =====
NEXT_PUBLIC_PRICE_STARTER_MONTHLY=price_xxx
NEXT_PUBLIC_PRICE_STARTER_YEARLY=price_xxx
NEXT_PUBLIC_PRICE_PRO_MONTHLY=price_xxx
NEXT_PUBLIC_PRICE_PRO_YEARLY=price_xxx
NEXT_PUBLIC_PRICE_FAMILIA_MONTHLY=price_xxx
NEXT_PUBLIC_PRICE_FAMILIA_YEARLY=price_xxx

# ===== ANALYTICS (Opcional) =====
NEXT_PUBLIC_POSTHOG_KEY=phc_xxx
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx

# ===== EMAIL (Opcional) =====
RESEND_API_KEY=re_xxx
FROM_EMAIL=hola@codeacademy.dev

# ===== OTROS =====
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=dev-secret-change-in-production
NODE_ENV=development
```

---

## 🧪 Probar la Aplicación

### 1. Landing Page
```
http://localhost:3000
```
Deberías ver:
- ✅ Navegación
- ✅ Hero con estadísticas
- ✅ Features
- ✅ Pricing
- ✅ Footer

### 2. Test Checkout

```
http://localhost:3000/pricing
```

Click en "Comenzar Prueba Gratuita":
- Usa tarjeta de prueba: `4242 4242 4242 4242`
- CVC: `123`
- Fecha: Cualquier futura

### 3. Panel Parental

```
http://localhost:3000/parent/dashboard
```

### 4. Curso Gratuito

```
http://localhost:3000/course/free/que-es-programacion
```

---

## 🔥 Comandos Útiles

```bash
# Desarrollo
npm run dev              # Iniciar dev server
npm run build            # Build para producción
npm run lint             # Ejecutar linter
npm run type-check       # Verificar tipos TypeScript

# Stripe
node apps/web/scripts/setup-stripe.js          # Setup productos
stripe listen --forward-to localhost:3000/api/stripe/webhook
stripe trigger checkout.session.completed      # Test webhook

# Supabase
supabase start           # Iniciar local
supabase stop            # Detener
supabase db reset        # Reset DB
supabase db push         # Push migrations
supabase gen types typescript --local > packages/database/database.types.ts

# Monorepo
turbo run dev            # Run dev en todos los workspaces
turbo run build          # Build todo
turbo run lint           # Lint todo
```

---

## 🐛 Troubleshooting

### Error: "Module not found: @supabase/supabase-js"
```bash
cd apps/web
npm install @supabase/supabase-js --legacy-peer-deps
```

### Error: "Cannot find module './database.types'"
```bash
# Generar types desde Supabase
supabase gen types typescript --project-id YOUR_PROJECT_ID > packages/database/database.types.ts
```

### Error: Stripe webhook signature invalid
```bash
# Asegúrate de que el webhook secret está correcto
stripe listen --print-secret
# Copia el secret a .env.local
```

### Error: Node version
```bash
# Necesitas Node.js 20+
node --version

# Si es menor:
fnm install 20
fnm use 20
```

### Puerto 3000 ocupado
```bash
# Cambiar puerto
npm run dev -- -p 3001
```

---

## 📚 Estructura del Proyecto

```
codeacademy/
├── apps/
│   └── web/                        # Next.js app
│       ├── src/
│       │   ├── app/               # Routes
│       │   │   ├── page.tsx      # Landing
│       │   │   ├── api/          # API routes
│       │   │   ├── parent/       # Panel parental
│       │   │   └── course/       # Cursos
│       │   ├── components/       # React components
│       │   ├── hooks/            # Custom hooks
│       │   ├── lib/              # Utilities
│       │   └── data/             # Static data
│       └── scripts/              # Setup scripts
├── packages/
│   └── database/                  # Supabase client
│       ├── client.ts             # Supabase config
│       ├── schema.sql            # DB schema
│       └── database.types.ts     # TypeScript types
├── docs/                          # Documentation
│   ├── STRIPE.md
│   └── ...
└── [config files]
```

---

## 🎯 Siguientes Pasos

1. ✅ **Setup completado** - App funcionando localmente
2. 🔨 **Generar types** - `supabase gen types`
3. 🎨 **Personalizar** - Colores, logos, textos
4. 📝 **Contenido** - Crear cursos adicionales
5. 🧪 **Testing** - Tests E2E
6. 🚀 **Deploy** - Vercel + Stripe Live

---

## 📖 Recursos

- [Documentación Next.js](https://nextjs.org/docs)
- [Supabase Docs](https://supabase.com/docs)
- [Stripe Docs](https://stripe.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

## 🆘 Ayuda

¿Problemas? Revisa:
1. **README.md** - Overview completo
2. **PROGRESO.md** - Estado detallado
3. **STRIPE.md** - Guía de Stripe
4. **Este archivo** - Quick start

O contacta: hola@codeacademy.dev

---

**¡Disfruta construyendo CodeAcademy! 🚀**
