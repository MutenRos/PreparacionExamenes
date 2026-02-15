#!/bin/bash

# Script para reemplazar colores hardcodeados con variables CSS en templates

TEMPLATES_DIR="/home/dario/src/dario_app/templates"

echo "🎨 Reemplazando colores hardcodeados con variables CSS..."
echo ""

# Función para reemplazar en un archivo
replace_colors() {
    local file="$1"
    local temp_file="${file}.tmp"
    
    # Crear backup
    cp "$file" "${file}.bak"
    
    # Reemplazos de colores comunes
    sed -i 's/#667eea/var(--brand-primary)/g' "$file"
    sed -i 's/#764ba2/var(--brand-secondary)/g' "$file"
    sed -i 's/#5568d3/var(--brand-primary-dark)/g' "$file"
    sed -i 's/#8b9eff/var(--brand-primary-light)/g' "$file"
    sed -i 's/#10b981/var(--color-success)/g' "$file"
    sed -i 's/#059669/var(--color-success-dark)/g' "$file"
    sed -i 's/#d1fae5/var(--color-success-light)/g' "$file"
    sed -i 's/#ef4444/var(--color-danger)/g' "$file"
    sed -i 's/#dc2626/var(--color-danger)/g' "$file"
    sed -i 's/#fee2e2/var(--color-danger-light)/g' "$file"
    sed -i 's/#f59e0b/var(--color-warning)/g' "$file"
    sed -i 's/#d97706/var(--color-warning-dark)/g' "$file"
    sed -i 's/#fef3c7/var(--color-warning-light)/g' "$file"
    sed -i 's/#3b82f6/var(--color-info)/g' "$file"
    sed -i 's/#2563eb/var(--color-info-dark)/g' "$file"
    sed -i 's/#dbeafe/var(--color-info-light)/g' "$file"
    
    # Grises
    sed -i 's/#fafafa/var(--gray-50)/g' "$file"
    sed -i 's/#f3f4f6/var(--gray-100)/g' "$file"
    sed -i 's/#f9fafb/var(--gray-100)/g' "$file"
    sed -i 's/#f8f9fa/var(--gray-100)/g' "$file"
    sed -i 's/#e5e7eb/var(--gray-200)/g' "$file"
    sed -i 's/#d1d5db/var(--gray-300)/g' "$file"
    sed -i 's/#ddd/var(--gray-300)/g' "$file"
    sed -i 's/#9ca3af/var(--gray-400)/g' "$file"
    sed -i 's/#6b7280/var(--gray-500)/g' "$file"
    sed -i 's/#666/var(--gray-600)/g' "$file"
    sed -i 's/#555/var(--gray-600)/g' "$file"
    sed -i 's/#4b5563/var(--gray-600)/g' "$file"
    sed -i 's/#374151/var(--gray-700)/g' "$file"
    sed -i 's/#333/var(--gray-800)/g' "$file"
    sed -i 's/#1f2937/var(--gray-800)/g' "$file"
    sed -i 's/#111827/var(--gray-900)/g' "$file"
    sed -i 's/#111/var(--gray-900)/g' "$file"
    
    # Colores específicos
    sed -i 's/#ffffff/var(--color-white)/g' "$file"
    sed -i 's/#fff\b/var(--color-white)/g' "$file"
    
    echo "✅ $file actualizado"
}

# Procesar templates principales
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
        echo "📝 Procesando $file..."
        replace_colors "$filepath"
    else
        echo "⚠️  No encontrado: $file"
    fi
done

echo ""
echo "🎉 Completado! Los archivos .bak contienen las copias de seguridad"
