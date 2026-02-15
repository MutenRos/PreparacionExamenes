#!/bin/bash
# Monitor y mantener el servidor OmniERP corriendo
# - Comprueba cada 2 minutos que está activo
# - Reinicia cada 2 horas
# - Reinicia automáticamente si se cae

set -e

SERVER_DIR="/home/dario"
VENV_PYTHON="$SERVER_DIR/.venv/bin/python3"
UVICORN_CMD="$SERVER_DIR/.venv/bin/uvicorn"
PORT=8001
APP_MODULE="dario_app.main:app"
LOG_FILE="/tmp/omnierp_monitor.log"
PID_FILE="/tmp/omnierp_server.pid"
STARTUP_TIME_FILE="/tmp/omnierp_startup_time"

# Colores para logs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ $1${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ $1${NC}" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  $1${NC}" | tee -a "$LOG_FILE"
}

start_server() {
    log "Iniciando servidor OmniERP..."
    
    cd "$SERVER_DIR"
    
    # Kill existing processes
    pkill -9 -f "uvicorn dario_app" 2>/dev/null || true
    sleep 2
    
    # Start server in background
    nohup $UVICORN_CMD $APP_MODULE --reload --host 0.0.0.0 --port $PORT > /tmp/omnierp_server.log 2>&1 &
    SERVER_PID=$!
    echo $SERVER_PID > "$PID_FILE"
    
    # Record startup time for 2-hour restart
    echo $(date +%s) > "$STARTUP_TIME_FILE"
    
    sleep 3
    
    # Verify it started by checking port
    if ss -tuln 2>/dev/null | grep -q ":$PORT " || netstat -tuln 2>/dev/null | grep -q ":$PORT "; then
        log_success "Servidor iniciado correctamente (PID: $SERVER_PID)"
        return 0
    else
        log_error "El servidor no respondió después de iniciar"
        cat /tmp/omnierp_server.log | tail -20 >> "$LOG_FILE"
        return 1
    fi
}

check_server() {
    # Check if process is running
    if ! pgrep -f "uvicorn dario_app" > /dev/null; then
        log_warning "Servidor no está corriendo"
        return 1
    fi
    
    # Check if port is listening
    if ! netstat -tuln 2>/dev/null | grep -q ":$PORT " && ! ss -tuln 2>/dev/null | grep -q ":$PORT "; then
        log_warning "Puerto $PORT no está escuchando"
        return 1
    fi
    
    # Try HTTP health check
    if curl -s http://localhost:$PORT/app/dashboard > /dev/null 2>&1; then
        log_success "Servidor está sano"
        return 0
    else
        log_warning "Servidor responde pero no es saludable"
        return 1
    fi
}

restart_server() {
    log_warning "Reiniciando servidor..."
    pkill -f "uvicorn dario_app" 2>/dev/null || true
    sleep 1
    start_server
}

should_restart_for_uptime() {
    if [ ! -f "$STARTUP_TIME_FILE" ]; then
        return 1
    fi
    
    STARTUP_TIME=$(cat "$STARTUP_TIME_FILE")
    CURRENT_TIME=$(date +%s)
    UPTIME=$((CURRENT_TIME - STARTUP_TIME))
    
    # 2 horas = 7200 segundos
    if [ $UPTIME -gt 7200 ]; then
        HOURS=$((UPTIME / 3600))
        log_warning "Servidor lleva $HOURS horas corriendo, reiniciando por mantenimiento..."
        return 0
    fi
    
    return 1
}

# Main monitoring loop
log "========================================="
log "Monitor OmniERP iniciado"
log "Configuración:"
log "  - Puerto: $PORT"
log "  - Directorio: $SERVER_DIR"
log "  - Intervalo de chequeo: 2 minutos"
log "  - Reinicio automático: cada 2 horas"
log "========================================="

# Start server initially
start_server

# Monitoring loop
CHECK_COUNTER=0
while true; do
    sleep 120  # Check every 2 minutes
    
    CHECK_COUNTER=$((CHECK_COUNTER + 1))
    log "Chequeo #$CHECK_COUNTER..."
    
    # Check if should restart due to uptime
    if should_restart_for_uptime; then
        restart_server
    elif ! check_server; then
        log_error "Servidor no está disponible, reiniciando..."
        start_server
    fi
done
