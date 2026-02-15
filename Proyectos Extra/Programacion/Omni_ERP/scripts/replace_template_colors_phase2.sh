#!/bin/bash

# Script avanzado para reemplazar colores hardcodeados con variables CSS

TEMPLATES_DIR="/home/dario/src/dario_app/templates"

echo "🎨 Fase 2: Reemplazando colores adicionales..."
echo ""

replace_advanced_colors() {
    local file="$1"
    
    # Colores de borde y fondos comunes
    sed -i 's/#f0f4ff/var(--brand-primary-light)/g' "$file"
    sed -i 's/#e5ecff/var(--brand-primary-light)/g' "$file"
    sed -i 's/#dde4f0/var(--gray-200)/g' "$file"
    sed -i 's/#eef2ff/var(--brand-primary-light)/g' "$file"
    
    # Colores específicos de estados
    sed -i 's/#0e7490/var(--color-info-dark)/g' "$file"
    sed -i 's/#06b6d4/var(--color-info)/g' "$file"
    sed -i 's/#14b8a6/var(--color-success)/g' "$file"
    sed -i 's/#f97316/var(--color-warning)/g' "$file"
    
    # Más variaciones de grises
    sed -i 's/#e0e7ff/var(--brand-primary-light)/g' "$file"
    sed -i 's/#f1f5f9/var(--gray-100)/g' "$file"
    sed -i 's/#e2e8f0/var(--gray-200)/g' "$file"
    sed -i 's/#cbd5e1/var(--gray-300)/g' "$file"
    sed -i 's/#94a3b8/var(--gray-400)/g' "$file"
    sed -i 's/#64748b/var(--gray-500)/g' "$file"
    sed -i 's/#475569/var(--gray-600)/g' "$file"
    sed -i 's/#334155/var(--gray-700)/g' "$file"
    sed -i 's/#1e293b/var(--gray-800)/g' "$file"
    sed -i 's/#0f172a/var(--gray-900)/g' "$file"
    
    # Colores RGBA comunes -> variables con transparencia
    sed -i 's/rgba(102, 126, 234, 0\.\([0-9]\+\))/rgba(var(--brand-primary-rgb), 0.\1)/g' "$file"
    sed -i 's/rgba(0, 0, 0, 0\.\([0-9]\+\))/rgba(0, 0, 0, 0.\1)/g' "$file"
    
    # Box shadows con colores específicos
    sed -i 's/rgba(102, 126, 234,/rgba(var(--brand-primary-rgb),/g' "$file"
    
    echo "✅ $file actualizado (fase 2)"
}

FILES=(
    "produccion.html"
    "produccion_ordenes.html"
    "configuracion.html"
    "usuarios_roles.html"
    "reportes.html"
    "pos_widgets.html"
    "puertas_entrada.html"
    "settings.html"
    "contabilidad.html"
    "oficina_tecnica.html"
)

for file in "${FILES[@]}"; do
    filepath="${TEMPLATES_DIR}/${file}"
    if [ -f "$filepath" ]; then
        echo "📝 Procesando $file (fase 2)..."
        replace_advanced_colors "$filepath"
    fi
done

echo ""
echo "🎉 Fase 2 completada!"
