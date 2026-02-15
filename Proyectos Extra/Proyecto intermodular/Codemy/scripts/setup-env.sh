#!/bin/bash

# Script para configurar variables de entorno de Supabase
# Ejecutar: bash scripts/setup-env.sh

echo "🚀 Configuración de Variables de Entorno - CodeAcademy"
echo "======================================================"
echo ""
echo "Este script te ayudará a configurar tu archivo .env.local"
echo ""

ENV_FILE="apps/web/.env.local"

# Verificar si ya existe el archivo
if [ -f "$ENV_FILE" ]; then
    echo "⚠️  El archivo .env.local ya existe."
    read -p "¿Quieres sobrescribirlo? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "❌ Operación cancelada"
        exit 1
    fi
    echo ""
fi

echo "📝 Necesitamos los datos de tu proyecto de Supabase"
echo ""
echo "Para obtener estos valores:"
echo "1. Ve a https://supabase.com/dashboard"
echo "2. Selecciona tu proyecto"
echo "3. Ve a Settings > API"
echo ""

# Solicitar URL de Supabase
read -p "🔗 URL del proyecto Supabase: " SUPABASE_URL
while [ -z "$SUPABASE_URL" ]; do
    echo "❌ La URL no puede estar vacía"
    read -p "🔗 URL del proyecto Supabase: " SUPABASE_URL
done

# Solicitar Anon Key
echo ""
read -p "🔑 Anon Key (pública): " SUPABASE_ANON_KEY
while [ -z "$SUPABASE_ANON_KEY" ]; do
    echo "❌ La Anon Key no puede estar vacía"
    read -p "🔑 Anon Key (pública): " SUPABASE_ANON_KEY
done

# Solicitar Service Role Key
echo ""
read -p "🔐 Service Role Key (secreta): " SUPABASE_SERVICE_ROLE_KEY
while [ -z "$SUPABASE_SERVICE_ROLE_KEY" ]; do
    echo "❌ La Service Role Key no puede estar vacía"
    read -p "🔐 Service Role Key (secreta): " SUPABASE_SERVICE_ROLE_KEY
done

# Crear el archivo .env.local
echo ""
echo "📄 Creando archivo .env.local..."

cat > "$ENV_FILE" << EOF
# =============================================
# CodeAcademy - Variables de Entorno
# Configuración automática generada el $(date +"%Y-%m-%d %H:%M:%S")
# =============================================

# ===== SUPABASE =====
NEXT_PUBLIC_SUPABASE_URL=$SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY=$SUPABASE_SERVICE_ROLE_KEY

# ===== STRIPE (Opcional - para pagos) =====
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_example
STRIPE_SECRET_KEY=sk_test_example
STRIPE_WEBHOOK_SECRET=whsec_example

# Price IDs (valores de ejemplo)
NEXT_PUBLIC_PRICE_STARTER_MONTHLY=price_example1
NEXT_PUBLIC_PRICE_STARTER_YEARLY=price_example2
NEXT_PUBLIC_PRICE_PRO_MONTHLY=price_example3
NEXT_PUBLIC_PRICE_PRO_YEARLY=price_example4
NEXT_PUBLIC_PRICE_FAMILIA_MONTHLY=price_example5
NEXT_PUBLIC_PRICE_FAMILIA_YEARLY=price_example6

# ===== APP =====
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXTAUTH_SECRET=$(openssl rand -base64 32)
NODE_ENV=development
EOF

echo ""
echo "✅ Archivo .env.local creado exitosamente!"
echo ""
echo "📋 Resumen de configuración:"
echo "  - Supabase URL: $SUPABASE_URL"
echo "  - Anon Key: ${SUPABASE_ANON_KEY:0:20}..."
echo "  - Service Role Key: ${SUPABASE_SERVICE_ROLE_KEY:0:20}..."
echo ""
echo "🔄 Reinicia el servidor de desarrollo para aplicar los cambios:"
echo "   cd apps/web && npm run dev"
echo ""
echo "🎉 ¡Listo! Ya puedes usar tu aplicación con Supabase"
