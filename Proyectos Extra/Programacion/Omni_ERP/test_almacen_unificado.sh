#!/bin/bash
# Test: Verificar que almacén.html está correctamente formado

echo "🧪 Test de Almacén Unificado"
echo "=============================="

# 1. Verificar que el archivo existe
if [ -f "/home/dario/src/dario_app/templates/almacen.html" ]; then
    echo "✅ Archivo almacén.html existe"
else
    echo "❌ Archivo almacén.html no encontrado"
    exit 1
fi

# 2. Verificar que contiene los tabs correctamente
TABS=("Configurar Pasillos" "Gestionar Parcelas" "Ver Ubicaciones" "Productos")
for tab in "${TABS[@]}"; do
    if grep -q "$tab" "/home/dario/src/dario_app/templates/almacen.html"; then
        echo "✅ Tab '$tab' encontrado"
    else
        echo "❌ Tab '$tab' no encontrado"
        exit 1
    fi
done

# 3. Verificar que las funciones JS principales existen
FUNCTIONS=("switchTab" "guardarPasillo" "cargarParcelasLlenas" "guardarParcelasLlenas" "actualizarEstadisticas")
for func in "${FUNCTIONS[@]}"; do
    if grep -q "function $func" "/home/dario/src/dario_app/templates/almacen.html"; then
        echo "✅ Función '$func' encontrada"
    else
        echo "❌ Función '$func' no encontrada"
        exit 1
    fi
done

# 4. Verificar que no contiene las secciones antiguas
OLD_SECTIONS=("Configuración del almacén" "Edición por bloques" "linear-gradient(135deg, #f8f9ff")
for section in "${OLD_SECTIONS[@]}"; do
    if grep -q "$section" "/home/dario/src/dario_app/templates/almacen.html"; then
        echo "⚠️  Encontrada sección antigua: '$section'"
    else
        echo "✅ Sección antigua '$section' eliminada correctamente"
    fi
done

# 5. Verificar localStorage
if grep -q "localStorage.setItem('configAlmacenIndividual'" "/home/dario/src/dario_app/templates/almacen.html"; then
    echo "✅ localStorage configAlmacenIndividual implementado"
else
    echo "❌ localStorage no correctamente implementado"
    exit 1
fi

# 6. Verificar que el servidor está activo
if curl -s http://localhost:8000/app/almacen | grep -q "🏭 Almacén"; then
    echo "✅ Servidor está sirviendo almacén.html correctamente"
else
    echo "❌ Servidor no está sirviendo almacén.html"
    exit 1
fi

echo ""
echo "✅ Todos los tests pasaron!"
echo ""
echo "📊 Estadísticas del archivo:"
wc -l "/home/dario/src/dario_app/templates/almacen.html"
echo ""
echo "Tamaño:"
du -h "/home/dario/src/dario_app/templates/almacen.html"
