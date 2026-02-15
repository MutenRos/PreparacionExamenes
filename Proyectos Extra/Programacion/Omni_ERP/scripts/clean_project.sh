#!/bin/bash
# Script de limpieza automática del proyecto

echo "🧹 Limpiando proyecto OmniERP..."

# Limpiar cache de Python
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null
echo "✓ Cache de Python limpiado"

# Limpiar archivos temporales
find . -type f -name "*~" -delete 2>/dev/null
find . -type f -name "*.swp" -delete 2>/dev/null
find . -type f -name "*.swo" -delete 2>/dev/null
echo "✓ Archivos temporales eliminados"

# Limpiar logs antiguos (mantener solo los últimos 5)
if [ -d "archive" ]; then
    find archive -name "*.log" -mtime +7 -delete 2>/dev/null
    echo "✓ Logs antiguos limpiados"
fi

# Mostrar estadísticas
echo ""
echo "📊 Estadísticas del proyecto:"
echo "- Módulos: $(find src/dario_app/modules -mindepth 1 -maxdepth 1 -type d | wc -l)"
echo "- Archivos Python: $(find src -name "*.py" | wc -l)"
echo "- Documentación: $(ls -1 *.md 2>/dev/null | wc -l) archivos MD"
echo "- Scripts en raíz: $(ls -1 *.py 2>/dev/null | wc -l)"

echo ""
echo "✅ Limpieza completada"
