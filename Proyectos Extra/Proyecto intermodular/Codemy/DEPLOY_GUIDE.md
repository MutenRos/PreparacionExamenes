# 🚀 Guía de Despliegue - Code Dungeon

## ✅ Pre-requisitos Verificados

- ✅ Sin errores de compilación
- ✅ TypeScript correctamente configurado
- ✅ Todas las rutas funcionando
- ✅ Tema dungeon 100% aplicado
- ✅ Sistema de retos implementado
- ✅ Sistema social completo
- ✅ Sistema de coins y recompensas
- ✅ Performance optimizado

---

## 📦 Opción 1: Deploy en Vercel (Recomendado)

### Paso 1: Instalar Vercel CLI
```bash
npm i -g vercel
```

### Paso 2: Login
```bash
vercel login
```

### Paso 3: Configurar Variables de Entorno
Crea un archivo `.env.production` basado en `.env.example`:

```bash
cp .env.example .env.production
```

Edita `.env.production` con tus valores reales:
```bash
# SUPABASE
NEXT_PUBLIC_SUPABASE_URL=https://tu-proyecto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu_anon_key_aqui
SUPABASE_SERVICE_ROLE_KEY=tu_service_role_key

# STRIPE
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# OTROS
NEXTAUTH_URL=https://tu-dominio.com
NEXTAUTH_SECRET=$(openssl rand -base64 32)
NODE_ENV=production
```

### Paso 4: Deploy
```bash
cd apps/web
vercel --prod
```

### Paso 5: Configurar Variables en Vercel
```bash
# Subir variables de entorno
vercel env add NEXT_PUBLIC_SUPABASE_URL
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY
vercel env add STRIPE_SECRET_KEY
# ... etc
```

O desde el dashboard: https://vercel.com/tu-proyecto/settings/environment-variables

---

## 🐳 Opción 2: Deploy con Docker

### Crear Dockerfile
```dockerfile
FROM node:18-alpine AS base

# Dependencias
FROM base AS deps
WORKDIR /app
COPY package*.json ./
COPY apps/web/package.json ./apps/web/
RUN npm install

# Builder
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Runner
FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/apps/web/.next ./apps/web/.next
COPY --from=builder /app/apps/web/public ./apps/web/public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
CMD ["npm", "start"]
```

### Build y Run
```bash
docker build -t code-dungeon .
docker run -p 3000:3000 --env-file .env.production code-dungeon
```

---

## 🖥️ Opción 3: VPS/Servidor Propio

### Requisitos
- Ubuntu 20.04+ / Debian 11+
- Node.js 18+
- Nginx (opcional, para reverse proxy)
- PM2 (para gestión de procesos)

### Paso 1: Preparar Servidor
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Instalar PM2
sudo npm install -g pm2

# Instalar Nginx (opcional)
sudo apt install -y nginx
```

### Paso 2: Clonar Proyecto
```bash
cd /var/www
git clone https://github.com/tu-usuario/codeacademy.git
cd codeacademy
```

### Paso 3: Configurar Variables
```bash
cp .env.example .env.production
nano .env.production
# Edita con tus valores reales
```

### Paso 4: Instalar y Build
```bash
npm install
npm run build
```

### Paso 5: Iniciar con PM2
```bash
cd apps/web
pm2 start npm --name "code-dungeon" -- start
pm2 save
pm2 startup
```

### Paso 6: Configurar Nginx (Opcional)
```bash
sudo nano /etc/nginx/sites-available/code-dungeon
```

Contenido:
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Activar:
```bash
sudo ln -s /etc/nginx/sites-available/code-dungeon /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Paso 7: SSL con Let's Encrypt
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

---

## 🔧 Configuración Post-Deploy

### 1. Configurar Supabase

#### Crear Proyecto
1. Ve a https://supabase.com/dashboard
2. Crea un nuevo proyecto
3. Copia URL y API Keys
4. Actualiza variables de entorno

#### Ejecutar Migraciones (si las tienes)
```bash
npx supabase db push
```

### 2. Configurar Stripe

#### Crear Cuenta
1. Ve a https://dashboard.stripe.com
2. Activa modo producción
3. Crea productos y precios
4. Configura webhooks

#### Configurar Webhooks
```bash
# URL del webhook
https://tu-dominio.com/api/webhooks/stripe

# Eventos a escuchar:
- checkout.session.completed
- customer.subscription.created
- customer.subscription.updated
- customer.subscription.deleted
```

### 3. Configurar Analytics (Opcional)

#### PostHog
```bash
NEXT_PUBLIC_POSTHOG_KEY=tu_key_aqui
```

#### Sentry
```bash
SENTRY_DSN=tu_dsn_aqui
```

---

## 🧪 Verificación Post-Deploy

### Checklist de Verificación
```bash
# 1. Verificar que el sitio carga
curl -I https://tu-dominio.com

# 2. Verificar rutas principales
curl https://tu-dominio.com/
curl https://tu-dominio.com/dashboard
curl https://tu-dominio.com/challenges
curl https://tu-dominio.com/social

# 3. Verificar API
curl https://tu-dominio.com/api/health

# 4. Verificar SSL
curl -vI https://tu-dominio.com 2>&1 | grep "SSL connection"
```

### Tests Manuales
- [ ] Landing page carga correctamente
- [ ] Registro de usuario funciona
- [ ] Login funciona
- [ ] Dashboard muestra datos
- [ ] Cursos se cargan
- [ ] Skill trees interactivos funcionan
- [ ] Sistema de retos activo
- [ ] Sistema social operativo
- [ ] Tienda de recompensas accesible
- [ ] Perfil personalizable
- [ ] Playground ejecuta código
- [ ] Pagos con Stripe funcionan (modo test primero)

---

## 📊 Monitoreo

### PM2 Monitoring
```bash
# Ver estado
pm2 status

# Ver logs
pm2 logs code-dungeon

# Monitoreo en tiempo real
pm2 monit
```

### Nginx Logs
```bash
# Access log
sudo tail -f /var/log/nginx/access.log

# Error log
sudo tail -f /var/log/nginx/error.log
```

---

## 🔄 Actualizaciones

### Deploy de Nuevas Versiones

#### Con Vercel
```bash
git push origin main
# Vercel auto-deploya
```

#### Con PM2
```bash
cd /var/www/codeacademy
git pull origin main
npm install
npm run build
pm2 reload code-dungeon --update-env
```

---

## 🆘 Troubleshooting

### Error: Cannot find module
```bash
# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Error: Port already in use
```bash
# Liberar puerto 3000
sudo lsof -ti:3000 | xargs kill -9
```

### Error: Build failed
```bash
# Limpiar cache
npm run clean
rm -rf .next
npm run build
```

### Error: Database connection
```bash
# Verificar variables de entorno
printenv | grep SUPABASE
```

---

## 📞 Soporte

- **Documentación**: Ver README.md
- **Issues**: Abrir issue en GitHub
- **Email**: soporte@codeacademy.dev

---

## 🎉 ¡Listo!

Tu plataforma Code Dungeon está lista para producción. 

**Próximos pasos recomendados:**
1. Configurar dominio personalizado
2. Activar SSL
3. Configurar CDN (Cloudflare)
4. Activar analytics
5. Configurar backup automático
6. Monitorear performance
7. ¡Lanzar! 🚀

---

**Versión**: 1.0.0  
**Última actualización**: 16 de Noviembre de 2025
