#!/bin/bash

# Script simplificado para iniciar el servidor en modo inmortal
# Puede ejecutarse directamente o usarse como respaldo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 Iniciando Codeacademy en modo INMORTAL..."
echo "📁 Directorio: $PROJECT_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Verificar si ya está corriendo
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  El servidor ya está corriendo en puerto 3000"
    echo ""
    read -p "¿Deseas reiniciarlo? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "❌ Cancelado"
        exit 0
    fi
    
    echo "🛑 Deteniendo servidor actual..."
    pkill -9 -f "next dev"
    pkill -9 -f "keep-alive"
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    sleep 3
fi

# Limpiar logs antiguos si son muy grandes
if [ -f "$PROJECT_DIR/keep-alive.log" ]; then
    LOG_SIZE=$(du -k "$PROJECT_DIR/keep-alive.log" | cut -f1)
    if [ "$LOG_SIZE" -gt 10240 ]; then # Si > 10MB
        echo "🧹 Limpiando log antiguo (>10MB)..."
        mv "$PROJECT_DIR/keep-alive.log" "$PROJECT_DIR/keep-alive.log.old"
    fi
fi

# Iniciar en background con nohup
echo "⚡ Iniciando keep-alive daemon..."
cd "$PROJECT_DIR"
nohup bash "$SCRIPT_DIR/keep-alive.sh" > /dev/null 2>&1 &
DAEMON_PID=$!

sleep 3

# Verificar que arrancó
if ps -p $DAEMON_PID > /dev/null 2>&1; then
    echo "✅ Daemon iniciado (PID: $DAEMON_PID)"
    echo ""
    echo "El servidor está corriendo en modo inmortal:"
    echo "  🌐 http://localhost:3000"
    echo "  📊 Logs: tail -f $PROJECT_DIR/keep-alive.log"
    echo "  🛑 Detener: pkill -f keep-alive"
    echo ""
else
    echo "❌ ERROR: No se pudo iniciar el daemon"
    exit 1
fi
