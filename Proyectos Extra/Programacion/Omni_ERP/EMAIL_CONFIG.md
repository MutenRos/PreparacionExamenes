# Configuración de Email para ERP Dario

## Variables de Entorno para SMTP

Para habilitar el envío automático de facturas por correo, configura las siguientes variables de entorno:

```bash
# Configuración SMTP (ejemplo con Gmail)
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="tu-email@gmail.com"
export SMTP_PASSWORD="tu-contraseña-de-aplicacion"
export FROM_EMAIL="tu-email@gmail.com"
export FROM_NAME="Tu Empresa"
```

## Configuración con Gmail

1. Ve a tu cuenta de Google
2. Activa la verificación en 2 pasos
3. Genera una "Contraseña de aplicación" en: https://myaccount.google.com/apppasswords
4. Usa esa contraseña en `SMTP_PASSWORD`

## Configuración con otros proveedores

### Outlook/Hotmail
```bash
export SMTP_HOST="smtp-mail.outlook.com"
export SMTP_PORT="587"
```

### SendGrid
```bash
export SMTP_HOST="smtp.sendgrid.net"
export SMTP_PORT="587"
export SMTP_USER="apikey"
export SMTP_PASSWORD="tu-api-key-de-sendgrid"
```

### Mailgun
```bash
export SMTP_HOST="smtp.mailgun.org"
export SMTP_PORT="587"
export SMTP_USER="postmaster@tu-dominio.mailgun.org"
```

## Archivo .env (Opcional)

Crea un archivo `.env` en `/home/dario/src/`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-contraseña
FROM_EMAIL=tu-email@gmail.com
FROM_NAME=ERP Dario
```

Luego carga las variables antes de iniciar el servidor:

```bash
cd /home/dario/src
source .env
python3 -m dario_app.server
```

## Modo Desarrollo (Sin SMTP)

Si NO configuras SMTP, el sistema:
- ✅ Generará las facturas PDF
- ✅ Marcará como `factura_generada=True`
- ⚠️ NO enviará emails (solo registrará en logs)
- ⚠️ Marcará como `factura_enviada=False`

Útil para desarrollo/pruebas sin necesidad de configurar email real.

## Prueba de Email

Endpoint de prueba:
```bash
POST /api/ventas/test-email
{
  "email": "destinatario@example.com"
}
```

## Logs

Los intentos de envío se registran en la consola:
```
[EMAIL] Would send invoice F-00001 to cliente@example.com
[EMAIL] PDF filename: F-00001.pdf
[EMAIL] SMTP not configured - email not sent
```

## Producción

Para producción, considera usar:
- **SendGrid** (hasta 100 emails/día gratis)
- **Mailgun** (hasta 5,000 emails/mes gratis)
- **Amazon SES** (muy económico, $0.10 por 1,000 emails)

¡Recuerda nunca commitear tus credenciales SMTP en el repositorio!
