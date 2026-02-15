# 🖥️ Deploy en Tu Servidor (SSH)

## ✅ BUILD EXITOSO

La aplicación está compilada y lista para producción.

---

## 🚀 Opción 1: Correr con PM2 (Recomendado)

PM2 mantiene la app corriendo 24/7, reinicia automáticamente si falla.

### Instalación

```bash
# Instalar PM2 globalmente
npm install -g pm2

# Iniciar la aplicación
cd /home/dario/codeacademy/apps/web
pm2 start npm --name "codeacademy" -- start

# Configurar PM2 para iniciar al arrancar el servidor
pm2 startup
pm2 save
```

### Comandos Útiles

```bash
# Ver logs en tiempo real
pm2 logs codeacademy

# Ver estado
pm2 status

# Reiniciar
pm2 restart codeacademy

# Detener
pm2 stop codeacademy

# Eliminar
pm2 delete codeacademy
```

---

## 🚀 Opción 2: Correr Directamente

```bash
cd /home/dario/codeacademy/apps/web
npm run start
```

**NOTA:** Esto bloqueará la terminal. Usa `screen` o `tmux` para mantenerlo corriendo:

```bash
# Con screen
screen -S codeacademy
cd /home/dario/codeacademy/apps/web
npm start
# Presiona Ctrl+A luego D para desconectar

# Reconectar
screen -r codeacademy
```

---

## 🌐 Configurar Nginx (Proxy Reverso)

Para servir en puerto 80/443 con dominio propio:

### 1. Instalar Nginx

```bash
sudo apt update
sudo apt install nginx
```

### 2. Crear configuración

```bash
sudo nano /etc/nginx/sites-available/codeacademy
```

**Contenido:**

```nginx
server {
    listen 80;
    server_name tu-dominio.com;  # Cambia esto
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Activar configuración

```bash
sudo ln -s /etc/nginx/sites-available/codeacademy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Configurar SSL (HTTPS) con Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

---

## ⚙️ Variables de Entorno de Producción

Antes de iniciar en producción, configura las variables reales:

```bash
cd /home/dario/codeacademy/apps/web
nano .env.local
```

**Reemplaza con tus valores reales:**

```bash
# Supabase (https://supabase.com/dashboard/project/_/settings/api)
NEXT_PUBLIC_SUPABASE_URL=https://tu-proyecto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu_anon_key_real
SUPABASE_SERVICE_ROLE_KEY=tu_service_role_key_real

# Stripe (https://dashboard.stripe.com/apikeys)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Price IDs (desde Stripe Dashboard)
NEXT_PUBLIC_PRICE_STARTER_MONTHLY=price_xxx
NEXT_PUBLIC_PRICE_STARTER_YEARLY=price_xxx
NEXT_PUBLIC_PRICE_PRO_MONTHLY=price_xxx
NEXT_PUBLIC_PRICE_PRO_YEARLY=price_xxx
NEXT_PUBLIC_PRICE_FAMILIA_MONTHLY=price_xxx
NEXT_PUBLIC_PRICE_FAMILIA_YEARLY=price_xxx

# App
NEXT_PUBLIC_APP_URL=https://tu-dominio.com
NEXTAUTH_SECRET=$(openssl rand -base64 32)
NODE_ENV=production
```

---

## 📊 Monitoring

### Ver logs

```bash
# PM2
pm2 logs codeacademy --lines 100

# Directo
cd /home/dario/codeacademy/apps/web
npm start 2>&1 | tee logs/app.log
```

### Health Check

```bash
curl http://localhost:3000/api/health
```

Respuesta esperada:
```json
{
  "status": "ok",
  "services": {
    "database": "ok",
    "stripe": "ok"
  }
}
```

---

## 🔥 Firewall

Abrir puertos necesarios:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
```

---

## 🎯 Checklist de Producción

- [ ] Variables de entorno configuradas
- [ ] Supabase en modo producción
- [ ] Stripe en Live Mode
- [ ] Webhook de Stripe configurado
- [ ] PM2 instalado y app corriendo
- [ ] Nginx configurado (si usas dominio)
- [ ] SSL activado con Certbot
- [ ] Firewall configurado
- [ ] Health check respondiendo OK

---

## 🆘 Troubleshooting

### Puerto 3000 ocupado

```bash
# Ver qué usa el puerto
sudo lsof -i :3000

# Matar proceso
sudo kill -9 PID
```

### Permisos

```bash
# Dar permisos a la carpeta
sudo chown -R $USER:$USER /home/dario/codeacademy
```

### Reiniciar después de cambios

```bash
# Rebuild
cd /home/dario/codeacademy/apps/web
npm run build

# Reiniciar PM2
pm2 restart codeacademy
```

---

## 🚀 ¡LISTO!

Tu aplicación CodeAcademy está corriendo en:

**Localmente:** http://localhost:3000  
**Con Nginx:** http://tu-dominio.com

**¡Felicidades por tu deploy! 🎉**
