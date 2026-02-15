#!/bin/bash
# Health check script - verifica que PM2 y los servidores estén activos

# Verificar si PM2 está corriendo
if ! pgrep -f "PM2" > /dev/null; then
    echo "[$(date)] PM2 no está corriendo, reiniciando..."
    cd /home/dario/codeacademy
    pm2 resurrect || pm2 start ecosystem.config.js
    pm2 save
fi

# Verificar estado de las aplicaciones
pm2 list | grep -q "codedungeon.*online" || {
    echo "[$(date)] codedungeon caído, reiniciando..."
    pm2 restart codedungeon
}

pm2 list | grep -q "codedungeon-testing.*online" || {
    echo "[$(date)] codedungeon-testing caído, reiniciando..."
    pm2 restart codedungeon-testing
}

# Verificar que los puertos respondan
timeout 5 curl -s http://localhost:3000 > /dev/null || {
    echo "[$(date)] Puerto 3000 no responde, reiniciando codedungeon..."
    pm2 restart codedungeon
}

timeout 5 curl -s http://localhost:3001 > /dev/null || {
    echo "[$(date)] Puerto 3001 no responde, reiniciando codedungeon-testing..."
    pm2 restart codedungeon-testing
}

echo "[$(date)] Health check completado - Todo OK"
