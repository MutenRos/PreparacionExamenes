# ⚡ OmniERP

**Sistema de Gestión Empresarial Integral** - ERP moderno con diseño AAAAA profesional

## 🚀 Características Principales

- **Multi-tenant**: Arquitectura para múltiples organizaciones
- **Gestión Completa**: Inventario, Ventas, Compras, POS, Clientes
- **Reportes Avanzados**: Analytics y dashboards interactivos
- **Documentación Automática**: Generación de facturas y documentos fiscales
- **Calendario Integrado**: Gestión de eventos y tareas
- **IA Asistente**: Sugerencias inteligentes basadas en datos
- **Diseño AAAAA**: Animaciones premium y UX profesional

## 📦 Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM async para bases de datos
- **SQLite** - Base de datos (multi-tenant architecture)
- **Pydantic** - Validación de datos
- **Ollama/LLaMA** - IA local para asistente inteligente

### Frontend
- **HTML5/CSS3** - Interfaz responsive
- **Vanilla JavaScript** - Sin dependencias pesadas
- **CSS Variables** - Sistema de diseño profesional
- **Animations** - Micro-interacciones AAAAA

## 🎨 Sistema de Diseño

### Colores Profesionales
- **Primary**: `#2563eb` (Azul empresarial)
- **Secondary**: `#7c3aed` (Púrpura profesional)
- **Success**: `#059669` (Verde vibrante)
- **Danger**: `#dc2626` (Rojo limpio)

### Animaciones AAAAA
- 6 keyframes principales (scaleIn, rotateIn, pulse, shimmer, float, glow)
- Micro-interacciones en todos los elementos
- Spring easing para movimiento natural

## 🗄️ Base de Datos

### Persistencia
- **Master DB**: `/home/dario/src/data/erp.db`
- **Tenant DBs**: `/home/dario/src/data/org_dbs/org_{ID}.db`
- Las DBs **NO se borran** al reiniciar el servidor

## 🚦 Iniciar Servidor

```bash
cd /home/dario && ./.venv/bin/uvicorn dario_app.main:app --reload --host 0.0.0.0 --port 8000
```

**Acceso**: http://localhost:8000

---

**OmniERP v1.0.0** - La solución integral para tu negocio ⚡
