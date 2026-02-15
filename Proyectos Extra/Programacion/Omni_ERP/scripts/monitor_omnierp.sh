#!/bin/bash

# Monitor OmniERP Server Health
# Verifica estado cada 5 minutos y registra en log

LOG_FILE="/home/dario/omnierp_monitor.log"
HEALTH_URL="http://localhost:8001/health"
MAX_RETRIES=3
RETRY_DELAY=5

check_health() {
    local response=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_URL" 2>/dev/null)
    [ "$response" = "200" ]
}

restart_service() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Server down, intentando reiniciar..." >> "$LOG_FILE"
    sudo systemctl restart omnierp
    sleep 5
    if check_health; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ Servidor reiniciado exitosamente" >> "$LOG_FILE"
        return 0
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✗ Error al reiniciar servidor" >> "$LOG_FILE"
        return 1
    fi
}

# Verificar estado
if ! check_health; then
    retry_count=0
    while [ $retry_count -lt $MAX_RETRIES ]; do
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Intento de conexión $((retry_count + 1))/$MAX_RETRIES..." >> "$LOG_FILE"
        sleep $RETRY_DELAY
        if check_health; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ Servidor volvió a estar disponible" >> "$LOG_FILE"
            exit 0
        fi
        ((retry_count++))
    done
    
    # Si sigue sin responder, reiniciar
    restart_service
else
    # Verificación exitosa - registrar
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ Server health check OK" >> "$LOG_FILE"
fi
