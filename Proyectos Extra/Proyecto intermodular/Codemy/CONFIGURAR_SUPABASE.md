# 🚀 Configuración de Supabase - Guía Rápida

## Error Actual
```
Runtime Error: supabaseKey is required.
```

Esto significa que faltan las variables de entorno de Supabase.

---

## Opción 1: Script Automático (Recomendado) ⚡

Ejecuta este comando desde la raíz del proyecto:

```bash
bash scripts/setup-env.sh
```

El script te pedirá tus credenciales de Supabase y configurará todo automáticamente.

---

## Opción 2: Configuración Manual 📝

### Paso 1: Obtener credenciales de Supabase

1. Ve a [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. Selecciona tu proyecto (o crea uno nuevo)
3. Ve a **Settings** → **API**
4. Copia estos valores:
   - **Project URL** (ejemplo: `https://xxxxx.supabase.co`)
   - **anon/public key** (empieza con `eyJhbGciOiJIUzI1NiIsInR...`)
   - **service_role key** (empieza con `eyJhbGciOiJIUzI1NiIsInR...`)

### Paso 2: Editar archivo `.env.local`

Abre el archivo `apps/web/.env.local` y reemplaza estos valores:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.tu_anon_key_real
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.tu_service_role_key_real
```

### Paso 3: Configurar Base de Datos

Ejecuta las migraciones de la base de datos:

```bash
# Opción A: Script automático
bash scripts/setup-supabase-email.sh

# Opción B: SQL manual
# Ve a Supabase Dashboard → SQL Editor
# Ejecuta el archivo: supabase/migrations/001_email_verification_setup.sql
```

### Paso 4: Configurar Email (Opcional)

1. Ve a **Authentication** → **Email Templates**
2. Personaliza las plantillas de verificación de email
3. Configura el dominio de email en **Authentication** → **URL Configuration**

### Paso 5: Reiniciar servidor

```bash
cd apps/web
npm run dev
```

---

## Verificación ✅

Para verificar que todo funciona:

```bash
node scripts/configure-supabase.js
```

Este script validará tu conexión con Supabase.

---

## Si no tienes un proyecto de Supabase

### Crear proyecto nuevo (5 minutos)

1. Ve a [https://supabase.com](https://supabase.com)
2. Crea una cuenta gratis
3. Click en **New Project**
4. Completa:
   - **Name**: CodeAcademy MVP
   - **Database Password**: (guarda esto en un lugar seguro)
   - **Region**: Elige el más cercano a ti
   - **Pricing Plan**: Free (suficiente para MVP)
5. Espera 2-3 minutos a que se cree el proyecto
6. Sigue los pasos de arriba para obtener las credenciales

---

## Estructura de archivos

```
codeacademy/
├── apps/web/.env.local          ← Aquí van las variables
├── scripts/
│   ├── setup-env.sh             ← Script de configuración automática
│   ├── setup-supabase-email.sh  ← Script para email verification
│   └── configure-supabase.js    ← Script de validación
└── supabase/
    └── migrations/
        └── 001_email_verification_setup.sql  ← Estructura de BD
```

---

## Problemas comunes

### ❌ "Invalid API key"
- Verifica que copiaste la **anon key** completa (es muy larga)
- No confundas la anon key con la service role key

### ❌ "Project URL is invalid"
- La URL debe terminar en `.supabase.co`
- Ejemplo: `https://abcdefgh.supabase.co`

### ❌ "Cannot find module '@supabase/supabase-js'"
```bash
cd apps/web
npm install
```

---

## ¿Necesitas ayuda?

Si sigues teniendo problemas, dame tus credenciales de Supabase y yo configuro el `.env.local` por ti. Necesito:

1. **Project URL**
2. **Anon Key**
3. **Service Role Key**

(Son seguras de compartir en entorno de desarrollo, pero nunca en producción)
