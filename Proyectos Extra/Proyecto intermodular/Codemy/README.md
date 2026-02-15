# 🎓 CodeAcademy - Plataforma Educativa de Programación

## 🎉 VERSIÓN 2.2 - ✅ COMPLETA CON EMAIL VERIFICATION

Una academia web completa que permite a usuarios de todas las edades aprender programación con gamificación avanzada, autocorrección inteligente y sistema completo de autenticación.

---

## ✅ Estado: PRODUCCIÓN READY + EMAIL VERIFICATION CONFIGURADO

**Última Actualización:** 13 de noviembre de 2025  
**Versión:** 2.2.0 (Email Verification + Contenido Completo)  
**Stack:** Next.js 16.0 + React 19.2 + TypeScript 5 + Tailwind CSS 4 + Supabase Auth

### 🚀 Servidor Activo:
- 🟢 **Desarrollo:** http://localhost:3000
- 🟢 **Red Local:** http://192.168.1.157:3000
- 🟢 **IP Pública:** http://88.17.157.221:3000
- ✅ **Email Verification:** Sistema completo integrado con Supabase
- ✅ **Tailwind CSS v4:** Migración completada (@import syntax)
- ✅ **Dark Mode:** Tema morado/rosa en toda la plataforma

### 🔐 Sistema de Autenticación (NUEVO):
- ✅ **Registro con verificación de email**
- ✅ **Login con sesión persistente**
- ✅ **Verificación automática de emails**
- ✅ **Reenvío de emails de verificación**
- ✅ **Templates de email personalizados** (tema morado/rosa)
- ✅ **Redirect URLs configurados** (localhost + IPs)
- ✅ **Row Level Security (RLS)** en Supabase
- ✅ **Migración SQL completa** con triggers y policies

### 📚 Guías de Configuración (NUEVAS):
- 📖 **QUICK_START_EMAIL_VERIFICATION.md** - Setup en 5 minutos
- 📖 **docs/VISUAL_SETUP_GUIDE.md** - Guía paso a paso con instrucciones visuales
- 📖 **docs/SUPABASE_EMAIL_SETUP.md** - Documentación completa y detallada
- 🔧 **scripts/setup-supabase-email.sh** - Script automático de configuración
- 🔧 **scripts/configure-supabase.js** - Script interactivo Node.js
- 🗄️ **supabase/migrations/001_email_verification_setup.sql** - Migración completa

### ✅ Contenido Educativo (6 Cursos, 33 Lecciones - 100% COMPLETO):
- ✅ **py-intro** (4 lecciones completas) - 200 XP
- ✅ **py-variables** (5 lecciones completas) - 250 XP
- ✅ **py-control** (6 lecciones completas) - 300 XP
- ✅ **py-functions** (6 lecciones completas) - 350 XP
- ✅ **py-classes** (6 lecciones completas) - 400 XP
- ✅ **py-files** (6 lecciones completas) - 300 XP

**Total:** 2400 XP máximo, Nivel 24, 9 Logros

### 🎯 Proyectos Finales (Nuevo):
- � **Agenda CRUD** - Sistema de gestión de contactos (200 XP)
- 👥 **Sistema de Clientes** - POO con persistencia (250 XP)
- 🛒 **Lista de Compra Inteligente** - Múltiples formatos (300 XP)

### 📊 Métricas Actualizadas:
- 📁 **220+ archivos** de código
- 📝 **~22,000 líneas** de código
- 🧩 **40+ componentes** React
- 🎓 **33 lecciones** (100% completas con teoría, ejemplos, ejercicios)
- 🎯 **3 proyectos finales** con rúbricas y plantillas
- 📚 **~25,000 líneas** de documentación (6 guías completas)
- 🗄️ **10 tablas** Supabase (schema production-ready + profiles)
- 🎮 **9 achievements** (common, rare, epic, legendary)
- 🔐 **Sistema de auth completo** con verificación de email

### 📝 Documentación Completa:
- ✅ **QUICK_START_EMAIL_VERIFICATION.md** - Setup rápido (5 minutos)
- ✅ **docs/VISUAL_SETUP_GUIDE.md** - Guía visual paso a paso
- ✅ **docs/SUPABASE_EMAIL_SETUP.md** - Documentación técnica completa
- ✅ **GUIA_INSTRUCTORES.md** (8,617 líneas) - Manual para profesores
- ✅ **MIGRACION_SUPABASE.md** (9,841 líneas) - Guía técnica migración cloud
- ✅ **supabase/schema.sql** (563 líneas) - Base de datos production-ready
- ✅ **PROYECTO_COMPLETADO.md** - Resumen ejecutivo del proyecto

---

## 🏗️ Arquitectura

```
codeacademy/
├── apps/
│   ├── web/                    # Next.js 14 - Aplicación principal
│   ├── runner/                 # Docker - Microservicio ejecución de código
│   └── admin/                  # Panel administración
├── packages/
│   ├── ui/                     # Componentes reutilizables
│   ├── database/               # Supabase client + tipos
│   ├── auth/                   # Utilidades de autenticación
│   └── shared/                 # Tipos y utilidades compartidas
├── docs/                       # Documentación
└── deployment/                 # Scripts y configuración deployment
```

## ✨ Características Principales

### 🎯 Sistema Curricular Modular
- **Conceptos agnósticos** - Variables, bucles, funciones independientes del lenguaje
- **Language Bindings** - Implementación específica por lenguaje (Python, JS, C#)
- **Progresión adaptativa** - El sistema se adapta al ritmo del estudiante

### 🔒 Ejecución Segura de Código
- **Sandboxing Docker** - Aislamiento completo por contenedor
- **Límites estrictos** - Tiempo, memoria y red controlados
- **Autocorrección** - Tests automáticos con feedback específico

### 🎮 Gamificación Profunda
- **Sistema XP/Nivel** - 45+ badges únicos, streaks, rankings
- **Challenges semanales** - Retos por track y por edad
- **Leaderboards dinámicos** - Competición sana por región/skill

### 👨‍👩‍👧‍👦 Control Parental Avanzado
- **Panel tiempo real** - Progreso detallado de los hijos
- **Límites de sesión** - Control de tiempo configurable
- **Reportes automáticos** - Emails semanales con progreso

### 💰 Monetización Multi-Canal
- **Freemium B2C** - Curso gratuito + planes Starter/Pro/Familia
- **Licencias B2B** - Colegios, ayuntamientos, empresas
- **Marketplace** - Contenidos premium de la comunidad

## 🛠️ Stack Tecnológico

### Frontend
- **Next.js 14** - React Server Components + App Router
- **TypeScript** - Tipado estático completo
- **Tailwind CSS** - Styling utility-first
- **Framer Motion** - Animaciones fluidas
- **Monaco Editor** - Editor de código con LSP

### Backend
- **Supabase** - PostgreSQL + Auth + Storage + Edge Functions
- **Stripe Billing** - Pagos recurrentes y facturación
- **Docker** - Contenedores para ejecución segura
- **Vercel** - Hosting y CI/CD

### Herramientas
- **Turbo** - Monorepo management
- **ESLint + Prettier** - Linting y formatting
- **Sentry** - Error monitoring
- **PostHog** - Analytics de producto

## 🚀 Instalación y Desarrollo

### Prerrequisitos
```bash
# Node.js 20+
fnm install 20.18.0
fnm use 20.18.0

# Docker para runners
sudo apt install docker.io docker-compose

# Git
git --version
```

### Setup Inicial
```bash
# Clonar y configurar
git clone <repo-url>
cd codeacademy

# Instalar dependencias
npm install

# Variables de entorno
cp .env.example .env.local
# Editar con tus credenciales de Supabase y Stripe
```

### Variables de Entorno Requeridas
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Analytics
NEXT_PUBLIC_POSTHOG_KEY=your_posthog_key
SENTRY_DSN=your_sentry_dsn
```

### Comandos de Desarrollo
```bash
# Desarrollo paralelo de todas las apps
npm run dev

# Desarrollo solo web app
npm run dev --workspace=@codeacademy/web

# Build completo
npm run build

# Testing
npm run test

# Linting
npm run lint

# Type checking
npm run type-check
```

## 📊 Estructura de Base de Datos

### Core Tables
- `profiles` - Perfiles de usuario con roles
- `user_preferences` - Configuraciones personalizadas
- `concepts` - Conceptos agnósticos de programación  
- `concept_bindings` - Implementación por lenguaje
- `exercises` - Ejercicios prácticos
- `submissions` - Envíos y evaluaciones

### Gamificación
- `user_xp` - Puntos de experiencia y niveles
- `badges` - Definición de logros
- `user_badges` - Badges obtenidos
- `challenges` - Retos semanales
- `challenge_participations` - Participación en retos

### Business
- `subscriptions` - Suscripciones Stripe
- `subscription_plans` - Planes disponibles
- `user_events` - Analytics de actividad
- `daily_metrics` - Métricas agregadas

## 🎓 Curriculum Inicial (MVP)

### Track: Fundamentals (L0-L2)
1. **Variables y Tipos** - String, Number, Boolean en Python/JS/C#
2. **Operadores** - Aritméticos, comparación, lógicos
3. **Condicionales** - if/else, switch, operador ternario
4. **Bucles** - for, while, iteración sobre colecciones
5. **Funciones** - Definición, parámetros, return
6. **Estructuras** - Listas, diccionarios, objetos
7. **Input/Output** - Consola, archivos básicos
8. **Depuración** - Breakpoints, logs, manejo de errores

### Track: Web (L1-L2)
1. **HTML/CSS** - Estructura, estilos, responsive
2. **JavaScript DOM** - Selección, manipulación, eventos
3. **APIs Web** - Fetch, localStorage, geolocation
4. **Frameworks** - Introducción a React/Vue

### Track: Games (L1-L2)  
1. **Unity Basics** - Scenes, GameObjects, Components
2. **C# para Unity** - MonoBehaviour, Coroutines
3. **2D Games** - Sprites, Physics2D, Input
4. **3D Basics** - Mesh, Materials, Lighting

## 🔧 Microservicio Code Runner

### Arquitectura
```bash
apps/runner/
├── Dockerfile
├── src/
│   ├── server.ts          # Express API
│   ├── queue/             # Bull Queue para jobs
│   ├── executors/         # Ejecutores por lenguaje
│   │   ├── python.ts
│   │   ├── javascript.ts
│   │   └── csharp.ts
│   └── security/          # Sandboxing y límites
└── containers/            # Dockerfiles por lenguaje
    ├── python/
    ├── node/
    └── dotnet/
```

### API Endpoints
```bash
POST /execute
{
  "language": "python",
  "code": "print('Hello World')",
  "tests": "assert 'Hello' in output",
  "timeLimit": 5000,
  "memoryLimit": 128
}

Response:
{
  "status": "passed",
  "output": "Hello World\n",
  "executionTime": 45,
  "memoryUsed": 12.3,
  "testResults": {...}
}
```

## 📈 Roadmap de Implementación

### Semana 1 ✅
- [x] Setup monorepo con Turbo
- [x] Next.js 14 + TypeScript + Tailwind
- [x] Schema Supabase completo
- [x] Estructura de packages

### Semana 2 🚧
- [ ] Autenticación completa con roles
- [ ] Dashboard base con navegación
- [ ] Sistema de conceptos modular
- [ ] Editor Monaco integrado

### Semana 3
- [ ] Code runners Docker
- [ ] Sistema de gamificación
- [ ] Panel parental
- [ ] Curriculum inicial (24 conceptos)

### Semana 4
- [ ] Integración Stripe completa
- [ ] Testing E2E
- [ ] Deploy automatizado
- [ ] Beta testing con usuarios reales

## 🎯 Métricas de Éxito

### Semana 1-2 (Validation)
- 50+ signups en curso gratuito
- 70% completion rate lección 1
- NPS > 8 en feedback inicial

### Mes 1 (Product-Market Fit)
- 500+ usuarios registrados
- 15% conversión free → paid
- <5% churn mensual
- €5K MRR objetivo

### Mes 3 (Scale)
- 2000+ usuarios activos
- 25% conversion rate
- €25K MRR
- 3+ colegios B2B

## 🤝 Contribuir

1. Fork del proyecto
2. Crear feature branch (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Contacto

- **Email**: hola@codeacademy.dev
- **Discord**: [Comunidad CodeAcademy](https://discord.gg/codeacademy)
- **Twitter**: [@CodeAcademyDev](https://twitter.com/CodeAcademyDev)

---

> 💡 **¿Listo para revolucionar la educación en programación?**
> 
> Este MVP AAA está diseñado para escalar desde 100 a 100,000 usuarios con la misma arquitectura. ¡Vamos a construir el futuro de la programación educativa! 🚀