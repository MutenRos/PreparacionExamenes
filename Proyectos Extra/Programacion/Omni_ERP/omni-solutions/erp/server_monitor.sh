#!/bin/bash

###############################################################################
# Server Monitor - Verifica y reinicia el servidor FastAPI cada 2 minutos
# Ubicación: /home/dario/omni-solutions/erp/server_monitor.sh
# Ejecución: bash server_monitor.sh
###############################################################################

# Configuración
SERVER_PORT=8001
SERVER_URL="http://localhost:${SERVER_PORT}/health"
VENV_PATH="/home/dario/omni-solutions/erp/venv"
SRC_PATH="/home/dario/src"
LOG_FILE="/tmp/erp_server_monitor.log"
CHECK_INTERVAL=120  # 2 minutos en segundos

# Función para escribir logs
log_message() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] $1" | tee -a "$LOG_FILE"
}

# Función para verificar si el servidor está corriendo
is_server_running() {
    if timeout 3 curl -s -o /dev/null -w "%{http_code}" "$SERVER_URL" 2>/dev/null | grep -q "200"; then
        return 0
    else
        return 1
    fi
}

# Función para iniciar el servidor
start_server() {
    log_message "🚀 Iniciando servidor FastAPI en puerto ${SERVER_PORT}..."
    
    # Matar cualquier proceso previo que esté escuchando en el puerto
    pkill -f "uvicorn.*${SERVER_PORT}" 2>/dev/null || true
    sleep 1
    
    # Iniciar nuevo proceso en background
    cd "$SRC_PATH"
    source "${VENV_PATH}/bin/activate"
    nohup uvicorn dario_app.main:app \
        --host 0.0.0.0 \
        --port ${SERVER_PORT} \
        --reload \
        > /tmp/erp_server.log 2>&1 &
    
    local pid=$!
    log_message "✅ Servidor iniciado con PID: $pid"
    
    # Esperar a que el servidor esté listo
    sleep 3
    
    if is_server_running; then
        log_message "✓ Servidor respondiendo correctamente"
        return 0
    else
        log_message "❌ Error: El servidor no responde después del inicio"
        return 1
    fi
}

# Función principal de monitoreo
monitor_server() {
    log_message "════════════════════════════════════════════════════"
    log_message "Monitor de Servidor ERP iniciado"
    log_message "Puerto: ${SERVER_PORT}"
    log_message "Intervalo de chequeo: ${CHECK_INTERVAL} segundos (2 minutos)"
    log_message "════════════════════════════════════════════════════"
    
    while true; do
        if is_server_running; then
            log_message "✓ Servidor OK (HTTP 200)"
        else
            log_message "⚠️  ¡Servidor no responde! Reiniciando..."
            start_server
            
            if ! is_server_running; then
                log_message "❌ CRÍTICO: No se pudo reiniciar el servidor"
                log_message "Verifique los logs: tail -f /tmp/erp_server.log"
            fi
        fi
        
        # Esperar antes del próximo chequeo
        sleep "$CHECK_INTERVAL"
    done
}

# Manejador de SIGINT/SIGTERM para salida limpia
cleanup() {
    log_message "⛔ Monitor detenido por el usuario"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar monitoreo
monitor_server
