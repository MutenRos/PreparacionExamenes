#!/bin/bash
# Monitor status checker para OmniERP

echo "========================================="
echo "🔍 Estado del Monitor OmniERP"
echo "========================================="
echo ""

# Check if monitor is running
if pgrep -f "monitor_server.sh" > /dev/null; then
    MONITOR_PID=$(pgrep -f "monitor_server.sh" | head -1)
    echo "✅ Monitor corriendo (PID: $MONITOR_PID)"
else
    echo "❌ Monitor no está corriendo"
fi

echo ""

# Check if server is running
if pgrep -f "uvicorn dario_app" > /dev/null; then
    SERVER_PID=$(pgrep -f "uvicorn dario_app" | head -1)
    echo "✅ Servidor OmniERP corriendo (PID: $SERVER_PID)"
else
    echo "❌ Servidor OmniERP no está corriendo"
fi

echo ""

# Check port
if ss -tuln 2>/dev/null | grep -q ":8001 " || netstat -tuln 2>/dev/null | grep -q ":8001 "; then
    echo "✅ Puerto 8001 escuchando"
else
    echo "❌ Puerto 8001 no está escuchando"
fi

echo ""

# Check HTTP response
if curl -s http://localhost:8001/app/dashboard > /dev/null 2>&1; then
    echo "✅ Servidor respondiendo a HTTP"
else
    echo "❌ Servidor no respondiendo a HTTP"
fi

echo ""

# Show startup time if exists
if [ -f /tmp/omnierp_startup_time ]; then
    STARTUP_TIME=$(cat /tmp/omnierp_startup_time)
    CURRENT_TIME=$(date +%s)
    UPTIME=$((CURRENT_TIME - STARTUP_TIME))
    HOURS=$((UPTIME / 3600))
    MINUTES=$(( (UPTIME % 3600) / 60 ))
    
    echo "⏱️  Tiempo de ejecución: ${HOURS}h ${MINUTES}m"
fi

echo ""

# Show recent logs
echo "📋 Últimos eventos (últimos 10):"
echo "---"
if [ -f /tmp/omnierp_monitor.log ]; then
    tail -10 /tmp/omnierp_monitor.log | sed 's/^/  /'
fi

echo ""
echo "========================================="
echo "Comandos útiles:"
echo "  Ver logs:         tail -f /tmp/omnierp_monitor.log"
echo "  Ver server logs:  tail -f /tmp/omnierp_server.log"
echo "  Acceso web:       http://localhost:8001"
echo "========================================="
