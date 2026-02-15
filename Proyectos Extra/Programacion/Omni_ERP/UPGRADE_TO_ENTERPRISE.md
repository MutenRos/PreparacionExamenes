# 🚀 Guía de Actualización a Enterprise Edition

## Paso 1: Instalar Dependencias

```bash
# Opción A: Con pip
pip install redis pyotp qrcode pillow httpx strawberry-graphql[fastapi]

# Opción B: Con requirements
pip install -r requirements-enterprise.txt

# Opción C: Actualizar pyproject.toml
pip install -e ".[enterprise]"
```

## Paso 2: Configurar Redis (Opcional)

### Instalación Redis

```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis

# macOS
brew install redis
brew services start redis

# Docker
docker run -d -p 6379:6379 redis:latest
```

### Configurar en .env

```bash
REDIS_URL=redis://localhost:6379/0
```

Si no instalas Redis, el sistema usará cache en memoria automáticamente.

## Paso 3: Configurar Variables de Entorno

```bash
# Copiar ejemplo
cp .env.example .env.production

# Editar .env.production
nano .env.production
```

Configurar:
```bash
# Seguridad
SECRET_KEY=<generar con: python -c "import secrets; print(secrets.token_hex(32))">
DATABASE_ENCRYPTION_KEY=<otro-secret-key>
CORS_ORIGINS=https://app.omnierp.com,https://omnierp.com

# Redis (opcional)
REDIS_URL=redis://localhost:6379/0

# Features
ENABLE_2FA=true
ENABLE_ANALYTICS=true
ENABLE_WEBHOOKS=true
ENABLE_GRAPHQL=true

# Email (opcional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@omnierp.com
SMTP_PASSWORD=<app-password>
```

## Paso 4: Ejecutar Migraciones

```bash
# Crear tablas de auditoría, webhooks, 2FA
cd /home/dario
python -c "
import asyncio
from dario_app.database import init_db
asyncio.run(init_db())
"
```

## Paso 5: Reiniciar Servidor

```bash
# Con systemd
sudo systemctl restart omnierp

# O manualmente
cd /home/dario
./.venv/bin/uvicorn dario_app.main:app --host 0.0.0.0 --port 8001
```

## Paso 6: Verificar Features

```bash
# Health check
curl http://localhost:8001/api/enterprise/health

# Expected response:
{
  "status": "healthy",
  "version": "2.0.0",
  "features": {
    "cache": true,
    "events": true,
    "webhooks": true,
    "2fa": true,
    "analytics": true,
    "graphql": true,
    "rate_limiting": true
  }
}
```

## Paso 7: Probar GraphQL (opcional)

Visita: http://localhost:8001/graphql

Ejemplo query:
```graphql
query {
  productos(limit: 5, activo: true) {
    id
    nombre
    precio_venta
    stock_actual
  }
}
```

## Paso 8: Configurar 2FA

1. Login al sistema
2. Ir a Configuración → Seguridad
3. Click "Activar 2FA"
4. Escanear QR code con Google Authenticator
5. Ingresar código de verificación
6. Guardar códigos de backup

## Características Disponibles

### ✅ Disponibles Sin Configuración Extra
- Event Bus (events en memoria)
- Rate Limiting
- Command Palette (Ctrl+K)
- Audit Logging (SQLite)
- Analytics avanzado
- GraphQL API

### ⚙️ Requieren Configuración
- Redis Cache (opcional)
- 2FA/TOTP (requiere pyotp)
- Webhooks (requiere httpx)
- Email notifications (requiere SMTP)

### 🔐 Seguridad Mejorada
- Rate limiting activo por defecto
- Audit trail completo
- 2FA disponible
- Webhook signature verification

## Rollback (Si es Necesario)

```bash
# Volver a versión 1.0.0
git checkout v1.0.0

# O desactivar features en .env
ENABLE_2FA=false
ENABLE_ANALYTICS=false
ENABLE_WEBHOOKS=false
ENABLE_GRAPHQL=false
```

## Soporte

- Documentación: [ENTERPRISE_FEATURES.md](ENTERPRISE_FEATURES.md)
- Issues: https://github.com/omnierp/omnierp/issues
- Email: enterprise@omnierp.com

---

**¡Bienvenido a OmniERP Enterprise Edition! 🚀**
