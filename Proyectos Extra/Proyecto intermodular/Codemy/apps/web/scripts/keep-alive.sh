#!/bin/bash

# Script para mantener el servidor Next.js siempre activo
# Se reinicia automáticamente si se cae

PORT=3000
PROJECT_DIR="/home/dario/codeacademy/apps/web"
LOG_FILE="$PROJECT_DIR/keep-alive.log"
PID_FILE="$PROJECT_DIR/server.pid"

# Función para logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Función para limpiar procesos zombies
cleanup_zombies() {
    log "🧹 Limpiando procesos zombies..."
    pkill -9 -f "next dev" 2>/dev/null || true
    pkill -9 -f "node.*next" 2>/dev/null || true
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    rm -f "$PID_FILE" 2>/dev/null || true
    sleep 3
}

# Función para iniciar el servidor
start_server() {
    log "🚀 Iniciando servidor en puerto $PORT..."
    cd "$PROJECT_DIR"
    
    # Limpiar antes de iniciar
    cleanup_zombies
    
    # Iniciar servidor en background
    nohup npm run dev > "$PROJECT_DIR/server.log" 2>&1 &
    echo $! > "$PID_FILE"
    
    # Esperar a que arranque
    sleep 8
    
    # Verificar que arrancó
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        log "✅ Servidor iniciado correctamente (PID: $(cat $PID_FILE 2>/dev/null || echo 'unknown'))"
        return 0
    else
        log "❌ ERROR: Servidor no pudo iniciar"
        return 1
    fi
}

# Trap para manejar señales
trap 'log "🛑 Recibida señal de terminación"; cleanup_zombies; exit 0' SIGTERM SIGINT

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "🛡️  Servidor INMORTAL activado - Keep Alive Daemon"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Iniciar servidor por primera vez
start_server

# Loop infinito de monitoreo
CONSECUTIVE_FAILURES=0
while true; do
    sleep 10
    
    # Verificar si el servidor está corriendo
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        # Servidor OK
        if [ $CONSECUTIVE_FAILURES -gt 0 ]; then
            log "✓ Servidor recuperado y estable"
        fi
        CONSECUTIVE_FAILURES=0
    else
        # Servidor caído
        CONSECUTIVE_FAILURES=$((CONSECUTIVE_FAILURES + 1))
        log "⚠️  ALERTA: Servidor caído (fallo #$CONSECUTIVE_FAILURES)"
        
        # Reiniciar inmediatamente
        log "🔄 Iniciando recuperación automática..."
        
        if start_server; then
            log "✅ Recuperación exitosa"
            CONSECUTIVE_FAILURES=0
        else
            log "❌ Fallo en recuperación #$CONSECUTIVE_FAILURES"
            
            if [ $CONSECUTIVE_FAILURES -ge 3 ]; then
                log "💀 Múltiples fallos detectados. Limpieza profunda..."
                cleanup_zombies
                sleep 5
                start_server
                CONSECUTIVE_FAILURES=0
            fi
        fi
    fi
done
