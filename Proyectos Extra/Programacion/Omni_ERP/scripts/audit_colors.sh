#!/bin/bash

# Script para auditar colores hardcodeados en CSS y HTML
# Encuentra todos los colores hexadecimales que no son definiciones de variables

echo "🎨 === AUDITORÍA DE COLORES HARDCODEADOS ==="
echo ""

# Colores a buscar (excluir definiciones de variables)
echo "📊 Buscando colores en archivos CSS..."
echo ""

cd /home/dario/src/dario_app

# Buscar en archivos CSS
find static -name "*.css" -type f | while read file; do
    # Buscar colores hexadecimales que NO sean definiciones de variables
    matches=$(grep -n "color:\s*#\|background.*#" "$file" | grep -v "^\s*--" | grep -v "^[[:space:]]*--")
    
    if [ ! -z "$matches" ]; then
        echo "📁 $file"
        echo "$matches"
        echo ""
    fi
done

echo ""
echo "📊 Buscando colores inline en archivos HTML..."
echo ""

# Buscar en archivos HTML (estilos inline)
find templates -name "*.html" -type f | while read file; do
    matches=$(grep -n 'style="[^"]*#[0-9a-fA-F]\{3,6\}' "$file" | head -10)
    
    if [ ! -z "$matches" ]; then
        echo "📁 $file"
        echo "$matches"
        echo ""
    fi
done

echo ""
echo "✅ Auditoría completada"
