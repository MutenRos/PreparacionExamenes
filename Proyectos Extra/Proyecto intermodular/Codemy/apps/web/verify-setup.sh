#!/bin/bash

# 🔍 Script de Verificación - CodeAcademy
# Verifica que todo esté configurado correctamente

echo "🔍 Verificando configuración de CodeAcademy..."
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
ERRORS=0
WARNINGS=0
SUCCESS=0

# Función para verificar
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((SUCCESS++))
    else
        echo -e "${RED}✗${NC} $1"
        ((ERRORS++))
    fi
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# 1. Verificar Node.js
echo "📦 Verificando dependencias..."
node -v > /dev/null 2>&1
check "Node.js instalado"

npm -v > /dev/null 2>&1
check "npm instalado"

# 2. Verificar instalación de paquetes
if [ -d "node_modules" ]; then
    check "node_modules existe"
else
    echo -e "${RED}✗${NC} node_modules no encontrado - ejecuta: npm install"
    ((ERRORS++))
fi

# 3. Verificar variables de entorno
echo ""
echo "⚙️ Verificando variables de entorno..."

if [ -f ".env.local" ]; then
    check ".env.local existe"
    
    # Verificar variables críticas
    if grep -q "NEXT_PUBLIC_SUPABASE_URL" .env.local; then
        SUPABASE_URL=$(grep "NEXT_PUBLIC_SUPABASE_URL" .env.local | cut -d '=' -f2)
        if [[ $SUPABASE_URL == *"example"* ]]; then
            warn "NEXT_PUBLIC_SUPABASE_URL usa valor de ejemplo - actualiza con tus credenciales reales"
        else
            check "NEXT_PUBLIC_SUPABASE_URL configurado"
        fi
    else
        echo -e "${RED}✗${NC} NEXT_PUBLIC_SUPABASE_URL no encontrado en .env.local"
        ((ERRORS++))
    fi
    
    if grep -q "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY" .env.local; then
        STRIPE_KEY=$(grep "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY" .env.local | cut -d '=' -f2)
        if [[ $STRIPE_KEY == *"example"* ]]; then
            warn "STRIPE_PUBLISHABLE_KEY usa valor de ejemplo - actualiza con tus credenciales reales"
        else
            check "STRIPE_PUBLISHABLE_KEY configurado"
        fi
    else
        echo -e "${RED}✗${NC} STRIPE_PUBLISHABLE_KEY no encontrado en .env.local"
        ((ERRORS++))
    fi
else
    echo -e "${RED}✗${NC} .env.local no encontrado - copia .env.example"
    ((ERRORS++))
fi

# 4. Verificar build
echo ""
echo "🏗️ Verificando build..."

if [ -d ".next" ]; then
    check "Build existe (.next)"
else
    warn "Build no encontrado - ejecuta: npm run build"
fi

# 5. Verificar puerto 3000
echo ""
echo "🌐 Verificando puerto 3000..."

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    check "Servidor corriendo en puerto 3000"
else
    warn "Puerto 3000 libre - ejecuta: npm run dev o npm start"
fi

# 6. Health check (si el servidor está corriendo)
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo ""
    echo "🏥 Health Check..."
    
    HEALTH_RESPONSE=$(curl -s http://localhost:3000/api/health 2>/dev/null)
    
    if [ -n "$HEALTH_RESPONSE" ]; then
        if echo "$HEALTH_RESPONSE" | grep -q '"status":"ok"'; then
            check "Health endpoint responde OK"
        else
            warn "Health endpoint responde pero con errores: $HEALTH_RESPONSE"
        fi
    else
        warn "No se pudo conectar al health endpoint"
    fi
fi

# 7. Verificar archivos críticos
echo ""
echo "📁 Verificando archivos críticos..."

critical_files=(
    "package.json"
    "next.config.ts"
    "src/app/layout.tsx"
    "src/app/page.tsx"
)

for file in "${critical_files[@]}"; do
    if [ -f "$file" ]; then
        check "$file existe"
    else
        echo -e "${RED}✗${NC} $file no encontrado"
        ((ERRORS++))
    fi
done

# 8. Verificar PM2 (si está instalado)
echo ""
echo "🔄 Verificando PM2..."

if command -v pm2 &> /dev/null; then
    check "PM2 instalado"
    
    if pm2 list | grep -q "codeacademy"; then
        check "App codeacademy registrada en PM2"
    else
        warn "App no encontrada en PM2 - ejecuta: pm2 start npm --name codeacademy -- start"
    fi
else
    warn "PM2 no instalado - instala con: npm install -g pm2"
fi

# 9. Verificar Nginx (si está instalado)
echo ""
echo "🌐 Verificando Nginx..."

if command -v nginx &> /dev/null; then
    check "Nginx instalado"
    
    if [ -f "/etc/nginx/sites-available/codeacademy" ]; then
        check "Configuración Nginx existe"
    else
        warn "Configuración Nginx no encontrada"
    fi
    
    if systemctl is-active --quiet nginx; then
        check "Nginx corriendo"
    else
        warn "Nginx no está corriendo"
    fi
else
    warn "Nginx no instalado (opcional)"
fi

# Resumen
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 RESUMEN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}Exitoso:${NC} $SUCCESS"
echo -e "${YELLOW}Advertencias:${NC} $WARNINGS"
echo -e "${RED}Errores:${NC} $ERRORS"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}🎉 ¡Todo está perfecto! Tu aplicación está lista.${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️ Hay algunas advertencias, pero la app debería funcionar.${NC}"
    exit 0
else
    echo -e "${RED}❌ Hay errores que deben corregirse antes de continuar.${NC}"
    echo ""
    echo "📚 Consulta SETUP_GUIDE.md para más información."
    exit 1
fi
