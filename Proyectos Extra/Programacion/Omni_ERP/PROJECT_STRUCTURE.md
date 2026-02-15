# 📁 Estructura del Proyecto OmniERP

## 🎯 Descripción General
Sistema ERP completo con 100% paridad con Microsoft Dynamics 365 (74 módulos, 40+ módulos D365).

## 📂 Estructura Principal

```
/home/dario/
├── src/dario_app/          # 💻 Aplicación principal
│   ├── api/                # API endpoints consolidados
│   ├── modules/            # 74 módulos del sistema
│   ├── database/           # Configuración de base de datos
│   ├── templates/          # Templates HTML
│   ├── static/             # Archivos estáticos (CSS, JS)
│   └── main.py             # Punto de entrada FastAPI
│
├── scripts/                # 🛠️ Scripts de utilidad
│   ├── clean_project.sh    # Limpieza automática
│   ├── monitor_*.sh        # Scripts de monitoreo
│   └── test_*.sh           # Scripts de testing
│
├── archive/                # 📦 Archivos históricos
│   ├── scripts/            # Scripts obsoletos de seeding/fixes
│   ├── docs/               # Documentación de fases anteriores
│   └── *.log               # Logs históricos
│
├── init_db.py              # 🔧 Inicialización de base de datos
├── setup_db.py             # Configuración de DB
├── setup_quick.py          # Setup rápido
├── setup_workers.py        # Configuración de workers
│
├── README.md               # 📖 Documentación principal
├── ARQUITECTURA_SISTEMA.md # Arquitectura técnica
├── DATABASE_INFO.md        # Información de base de datos
├── EMAIL_CONFIG.md         # Configuración de email
└── .gitignore              # Exclusiones de Git
```

## 🏗️ Módulos del Sistema (74 total)

### Core ERP
- Inventario, Almacén, POS, Ventas, Compras
- Producción, Oficina Técnica, Logística
- Contabilidad, Finanzas, RRHH

### Dynamics 365 Parity (40 módulos)
- Sales, Marketing, Customer Service
- Field Service, Project Operations
- Supply Chain, Finance Operations
- HR & Payroll, Commerce
- Manufacturing Execution System (MES)
- Advanced Analytics & ML Platform

### Enterprise Features
- Audit Logs, Webhooks, 2FA/TOTP
- GraphQL API, Cache Management
- Command Palette, Advanced Analytics

## 🚀 Scripts Principales

### Desarrollo
```bash
./quick-start.sh              # Inicio rápido del servidor
./start_backend.sh            # Iniciar backend en puerto 8001
python init_db.py             # Inicializar base de datos
```

### Mantenimiento
```bash
./scripts/clean_project.sh    # Limpieza completa del proyecto
./scripts/monitor_server.sh   # Monitoreo del servidor
```

## 📊 Estadísticas del Proyecto

- **Módulos**: 74
- **Modelos SQLAlchemy**: 265+
- **Endpoints REST**: 775+
- **Archivos Python**: ~1400
- **Templates HTML**: 50+

## 🔗 URLs Importantes

- Dashboard: http://localhost:8001/app/dashboard
- API Docs: http://localhost:8001/docs
- GraphQL: http://localhost:8001/graphql
- Health Check: http://localhost:8001/api/enterprise/health

## 📝 Convenciones

- **Puerto**: 8001 (servidor principal)
- **Base de datos**: SQLite con async (aiosqlite)
- **Autenticación**: JWT + 2FA + RBAC
- **API**: FastAPI con OpenAPI/Swagger

## 🗂️ Archivos Archivados

Los siguientes tipos de archivos se han movido a `archive/`:
- Scripts de seeding antiguos (seed_*.py, add_*.py)
- Scripts de fixes temporales (fix_*.py)
- Documentación de fases (FASE_*.md, RESUMEN_*.md)
- Logs históricos (*.log)
- Documentos de auditoría y estados pasados

## 🧹 Mantenimiento

El proyecto incluye limpieza automática de:
- Cache de Python (__pycache__, *.pyc)
- Archivos temporales (*~, *.swp)
- Logs antiguos (>7 días en archive/)

Ejecutar limpieza: `./scripts/clean_project.sh`
