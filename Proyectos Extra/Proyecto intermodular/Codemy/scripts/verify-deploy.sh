#!/bin/bash

# ========================================
# Code Dungeon - Pre-Deploy Verification
# ========================================

echo "🚀 Iniciando verificación pre-deploy..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

errors=0
warnings=0

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        ((errors++))
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((warnings++))
}

echo "📋 Verificando estructura del proyecto..."
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ No se encontró package.json. Ejecuta desde la raíz del proyecto.${NC}"
    exit 1
fi

# Check Node version
echo "🔍 Verificando Node.js..."
NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
if [ "$NODE_VERSION" -ge 18 ]; then
    print_status 0 "Node.js version: $(node -v)"
else
    print_status 1 "Node.js version $(node -v) - Se requiere >= 18.0.0"
fi

# Check npm version
NPM_VERSION=$(npm -v | cut -d '.' -f 1)
if [ "$NPM_VERSION" -ge 9 ]; then
    print_status 0 "npm version: $(npm -v)"
else
    print_status 1 "npm version $(npm -v) - Se requiere >= 9.0.0"
fi

echo ""
echo "📦 Verificando dependencias..."

# Check if node_modules exists
if [ -d "node_modules" ]; then
    print_status 0 "node_modules instalado"
else
    print_status 1 "node_modules no encontrado - ejecuta: npm install"
fi

# Check critical packages
if [ -d "node_modules/next" ]; then
    print_status 0 "Next.js instalado"
else
    print_status 1 "Next.js no encontrado"
fi

if [ -d "node_modules/react" ]; then
    print_status 0 "React instalado"
else
    print_status 1 "React no encontrado"
fi

if [ -d "node_modules/typescript" ]; then
    print_status 0 "TypeScript instalado"
else
    print_status 1 "TypeScript no encontrado"
fi

echo ""
echo "🔧 Verificando configuración..."

# Check environment file
if [ -f ".env.local" ] || [ -f ".env" ]; then
    print_status 0 "Variables de entorno configuradas"
else
    print_warning "No se encontró .env.local - copia desde .env.example"
fi

# Check Next.js config
if [ -f "apps/web/next.config.ts" ]; then
    print_status 0 "next.config.ts encontrado"
else
    print_status 1 "next.config.ts no encontrado"
fi

# Check TypeScript config
if [ -f "apps/web/tsconfig.json" ]; then
    print_status 0 "tsconfig.json encontrado"
else
    print_status 1 "tsconfig.json no encontrado"
fi

echo ""
echo "🎨 Verificando archivos críticos..."

# Check critical app files
critical_files=(
    "apps/web/src/app/page.tsx"
    "apps/web/src/app/layout.tsx"
    "apps/web/src/app/dashboard/page.tsx"
    "apps/web/src/app/challenges/page.tsx"
    "apps/web/src/app/social/page.tsx"
    "apps/web/src/components/Navigation.tsx"
    "apps/web/src/components/Footer.tsx"
)

for file in "${critical_files[@]}"; do
    if [ -f "$file" ]; then
        print_status 0 "$(basename $file)"
    else
        print_status 1 "$file no encontrado"
    fi
done

echo ""
echo "🧪 Ejecutando verificaciones de código..."

# Type check
cd apps/web
if npm run type-check > /dev/null 2>&1; then
    print_status 0 "TypeScript type check passed"
else
    print_status 1 "TypeScript type check failed - ejecuta: npm run type-check"
fi

# Lint check
if npm run lint > /dev/null 2>&1; then
    print_status 0 "ESLint check passed"
else
    print_warning "ESLint warnings encontrados - ejecuta: npm run lint"
fi

cd ../..

echo ""
echo "🏗️  Verificando build..."

# Try to build (optional - can be slow)
read -p "¿Ejecutar build de prueba? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd apps/web
    if npm run build > /dev/null 2>&1; then
        print_status 0 "Build exitoso"
        rm -rf .next
    else
        print_status 1 "Build failed - ejecuta: npm run build para ver errores"
    fi
    cd ../..
fi

echo ""
echo "================================================"
echo "📊 Resumen de Verificación"
echo "================================================"
echo ""

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo -e "${GREEN}🎉 ¡TODO PERFECTO! El proyecto está listo para deploy.${NC}"
    echo ""
    echo "Próximos pasos:"
    echo "1. Configura variables de entorno en producción"
    echo "2. Configura Supabase project"
    echo "3. Configura Stripe webhooks"
    echo "4. Deploy a Vercel: vercel --prod"
    echo "5. O deploy a tu servidor: npm run build && npm start"
    exit 0
elif [ $errors -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Verificación completada con $warnings advertencias${NC}"
    echo "El proyecto puede desplegarse, pero revisa las advertencias."
    exit 0
else
    echo -e "${RED}❌ Verificación fallida con $errors errores y $warnings advertencias${NC}"
    echo "Corrige los errores antes de deployar."
    exit 1
fi
