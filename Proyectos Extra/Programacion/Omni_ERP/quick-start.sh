#!/bin/bash
# Quick Start Guide - ERP Dario

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          ERP DARIO - GUÍA DE INICIO RÁPIDO                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

#!/bin/bash
# Detect server status and base URL (5000 or 8001)

# Check if server is running
if pgrep -f "uvicorn dario_app.api:app" > /dev/null || pgrep -f dario-server > /dev/null; then
    echo "✅ Servidor: EJECUTÁNDOSE"
    echo "   PID: $(pgrep -f "uvicorn dario_app.api:app" | head -n1)"
else
    echo "⚠️  Servidor: DETENIDO"
    echo "   Iniciar con: dario-server"
fi

echo ""
echo "📍 URLs DEL SISTEMA:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
BASE_URL="http://localhost:5000"
curl -s "$BASE_URL/health" >/dev/null || BASE_URL="http://localhost:8001"
echo "Landing Page:        $BASE_URL/"
echo "Login:               $BASE_URL/app/login"
echo "Dashboard:           $BASE_URL/app/dashboard"
echo "Punto de Venta:      $BASE_URL/app/pos"
echo "Configuración:       $BASE_URL/app/settings"
echo "API Docs (Swagger):  $BASE_URL/api/docs"
echo ""

echo "🔐 CREDENCIALES DE ADMINISTRADOR:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Email:     admin@erpdario.com"
echo "Password:  admin123"
echo ""

echo "🔧 COMANDOS DISPONIBLES:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Iniciar servidor:         dario-server"
echo "Detener servidor:         pkill -f dario-server"
echo "Ejecutar tests:           pytest"
echo "Ver coverage:             pytest --cov=dario_app"
echo "Crear admin:              python scripts/create_admin.py"
echo "Lint código:              ruff check src tests"
echo "Formatear código:         black src tests"
echo ""

echo "📦 MÓDULOS IMPLEMENTADOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ Multi-Tenancy (Organizations)"
echo "✓ Autenticación (JWT + bcrypt)"
echo "✓ Usuarios (CRUD + roles)"
echo "✓ Inventario (Productos + stock)"
echo "✓ Ventas (Órdenes + detalles)"
echo "✓ Compras (Proveedores)"
echo "✓ Clientes (CRM + lealtad)"
echo "✓ POS (Punto de Venta)"
echo "✓ Reportes (Analytics)"
echo ""

echo "📊 ESTADÍSTICAS DEL PROYECTO:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Archivos Python:     $(find src/dario_app -name "*.py" | wc -l)"
echo "Templates HTML:      $(find src/dario_app/templates -name "*.html" | wc -l)"
echo "Tests:               $(find tests -name "test_*.py" | wc -l) archivos"
echo ""

echo "💡 PRÓXIMOS PASOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Acceder a http://localhost:5000"
echo "2. Explorar la landing page"
echo "3. Hacer login con las credenciales de admin"
echo "4. Probar los módulos desde el dashboard"
echo "5. Revisar la API en http://localhost:5000/docs"
echo ""

echo "📖 DOCUMENTACIÓN:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "README.md              - Documentación completa"
echo "SISTEMA_COMPLETO.md    - Resumen de características"
echo "/docs                  - API interactiva (Swagger)"
echo "/redoc                 - API docs alternativo (ReDoc)"
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "   🎉 SISTEMA LISTO PARA USAR 🎉"
echo "═══════════════════════════════════════════════════════════════"
