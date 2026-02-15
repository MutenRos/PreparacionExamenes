# 🚀 OmniERP - Sistema ERP Completo

Sistema ERP empresarial con **100% paridad con Microsoft Dynamics 365**.

## ⚡ Quick Start

```bash
# 1. Inicializar base de datos
python init_db.py

# 2. Iniciar servidor
./quick-start.sh

# 3. Acceder al dashboard
# http://localhost:8001/app/dashboard
```

## 📋 Características Principales

### ✅ 74 Módulos Implementados
- **ERP Core**: Inventario, Ventas, Compras, Producción, Almacén
- **Finanzas**: Contabilidad, Gestión Financiera, Cashflow
- **RRHH**: Empleados, Nómina, Vacaciones, Partes de trabajo
- **Logistics**: Envíos, Rutas, Logística Interna, Puertas
- **Producción**: MES, BOM, Órdenes de Producción
- **CRM**: Ventas, Marketing, Customer Service
- **Enterprise**: Audit Logs, Webhooks, 2FA, GraphQL

### 🎯 Dynamics 365 Parity (40/40 módulos)
✅ Sales • Marketing • Customer Service • Field Service  
✅ Finance • Supply Chain • Manufacturing • Commerce  
✅ Project Operations • HR & Payroll • Business Central  
✅ Advanced Analytics • ML Platform • IoT Intelligence

## 🏗️ Arquitectura

- **Backend**: FastAPI 0.104+ (async/await)
- **Base de datos**: SQLite + SQLAlchemy 2.0 (async)
- **Autenticación**: JWT + 2FA + RBAC + SoD
- **API**: 775+ endpoints REST + GraphQL
- **Frontend**: HTML templates + Vanilla JS

## 📖 Documentación

- [Estructura del Proyecto](PROJECT_STRUCTURE.md)
- [Arquitectura del Sistema](ARQUITECTURA_SISTEMA.md)
- [Configuración de Base de Datos](DATABASE_INFO.md)
- [Configuración de Email](EMAIL_CONFIG.md)
- [Monitoreo del Servidor](SERVER_MONITORING.md)

## 🛠️ Scripts Útiles

```bash
# Limpieza del proyecto
./scripts/clean_project.sh

# Monitoreo del servidor
./scripts/monitor_server.sh

# Tests
./scripts/test_features.sh
```

## 📊 Estadísticas

- 🎯 **Módulos**: 74
- 📦 **Modelos**: 265+
- 🔌 **Endpoints**: 775+
- 🐍 **Archivos Python**: ~1400
- 📝 **Templates**: 50+

## 🔐 Seguridad

- JWT Authentication
- Two-Factor Authentication (2FA/TOTP)
- Role-Based Access Control (RBAC)
- Segregation of Duties (SoD)
- Audit Logs completos

## 🌐 URLs

- **Dashboard**: http://localhost:8001/app/dashboard
- **API Docs**: http://localhost:8001/docs
- **GraphQL**: http://localhost:8001/graphql
- **Health**: http://localhost:8001/api/enterprise/health

## 📦 Dependencias Principales

```txt
fastapi>=0.104.0
sqlalchemy>=2.0.0
aiosqlite
pydantic>=2.0.0
python-jose[cryptography]
passlib[bcrypt]
python-multipart
jinja2
```

## 🏃 Desarrollo

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar en modo desarrollo
uvicorn dario_app.main:app --reload --port 8001
```

## 📝 Licencia

Propietario - OmniERP 2025

---

**Versión**: 7.0 (Dynamics 365 Complete Parity)  
**Último update**: 25 Diciembre 2025
