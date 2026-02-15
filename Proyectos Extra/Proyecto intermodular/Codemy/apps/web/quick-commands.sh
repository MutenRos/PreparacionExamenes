#!/bin/bash

# 🚀 Quick Start - CodeAcademy
# Comandos rápidos para tareas comunes

show_menu() {
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎓 CodeAcademy - Quick Commands"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1) 🔍 Verificar configuración"
    echo "2) 🟢 Iniciar en desarrollo"
    echo "3) 🏗️  Build para producción"
    echo "4) 🚀 Iniciar en producción"
    echo "5) 📊 Ver estado (PM2)"
    echo "6) 📝 Ver logs"
    echo "7) 🔄 Reiniciar aplicación"
    echo "8) 🏥 Health check"
    echo "9) 🧹 Limpiar y rebuild"
    echo "10) 📚 Ver documentación"
    echo "0) ❌ Salir"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

verify_setup() {
    echo "🔍 Verificando configuración..."
    ./verify-setup.sh
    read -p "Presiona Enter para continuar..."
}

start_dev() {
    echo "🟢 Iniciando servidor de desarrollo..."
    echo "📍 URL: http://localhost:3000"
    echo ""
    npm run dev
}

build_prod() {
    echo "🏗️ Compilando para producción..."
    npm run build
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Build exitoso!"
        echo "Para iniciar: npm start"
    else
        echo ""
        echo "❌ Build falló. Revisa los errores arriba."
    fi
    read -p "Presiona Enter para continuar..."
}

start_prod() {
    echo "🚀 Iniciando en producción..."
    echo ""
    echo "Selecciona método:"
    echo "1) Directo (npm start)"
    echo "2) Con PM2 (recomendado)"
    read -p "Opción: " option
    
    case $option in
        1)
            echo "Iniciando con npm start..."
            npm start
            ;;
        2)
            if command -v pm2 &> /dev/null; then
                pm2 start npm --name "codeacademy" -- start
                pm2 save
                echo "✅ Aplicación iniciada con PM2"
            else
                echo "❌ PM2 no instalado. Instalando..."
                npm install -g pm2
                pm2 start npm --name "codeacademy" -- start
                pm2 save
            fi
            ;;
        *)
            echo "Opción inválida"
            ;;
    esac
    read -p "Presiona Enter para continuar..."
}

show_status() {
    echo "📊 Estado de la aplicación..."
    echo ""
    
    if command -v pm2 &> /dev/null; then
        pm2 status
    else
        echo "⚠️ PM2 no instalado"
        echo ""
        echo "Verificando puerto 3000..."
        if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo "✅ Servidor corriendo en puerto 3000"
        else
            echo "❌ No hay servidor en puerto 3000"
        fi
    fi
    
    read -p "Presiona Enter para continuar..."
}

show_logs() {
    echo "📝 Mostrando logs..."
    echo ""
    
    if command -v pm2 &> /dev/null; then
        pm2 logs codeacademy --lines 50
    else
        echo "⚠️ PM2 no instalado. No hay logs disponibles."
    fi
    
    read -p "Presiona Enter para continuar..."
}

restart_app() {
    echo "🔄 Reiniciando aplicación..."
    
    if command -v pm2 &> /dev/null; then
        pm2 restart codeacademy
        echo "✅ Aplicación reiniciada"
    else
        echo "⚠️ PM2 no instalado"
        echo "Deteniendo proceso en puerto 3000..."
        lsof -ti:3000 | xargs kill -9 2>/dev/null
        echo "Inicia nuevamente con la opción 2 o 4"
    fi
    
    read -p "Presiona Enter para continuar..."
}

health_check() {
    echo "🏥 Ejecutando health check..."
    echo ""
    
    response=$(curl -s http://localhost:3000/api/health 2>/dev/null)
    
    if [ -n "$response" ]; then
        echo "$response" | jq . 2>/dev/null || echo "$response"
        echo ""
        
        if echo "$response" | grep -q '"status":"ok"'; then
            echo "✅ Health check OK"
        else
            echo "⚠️ Health check con advertencias"
        fi
    else
        echo "❌ No se pudo conectar al servidor"
        echo "¿Está la aplicación corriendo?"
    fi
    
    read -p "Presiona Enter para continuar..."
}

clean_rebuild() {
    echo "🧹 Limpiando y rebuilding..."
    echo ""
    
    read -p "¿Eliminar node_modules? (s/N): " delete_nm
    
    if [[ $delete_nm =~ ^[Ss]$ ]]; then
        echo "Eliminando node_modules..."
        rm -rf node_modules
    fi
    
    echo "Eliminando .next..."
    rm -rf .next
    
    echo "Limpiando cache..."
    npm cache clean --force
    
    if [[ $delete_nm =~ ^[Ss]$ ]]; then
        echo "Instalando dependencias..."
        npm install --legacy-peer-deps
    fi
    
    echo "Building..."
    npm run build
    
    echo ""
    echo "✅ Limpieza y rebuild completado"
    read -p "Presiona Enter para continuar..."
}

show_docs() {
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📚 Documentación Disponible"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. PROJECT_COMPLETE.md  - Resumen completo del proyecto"
    echo "2. SETUP_GUIDE.md       - Configuración de Supabase y Stripe"
    echo "3. DEPLOY_SERVER.md     - Deploy en tu servidor"
    echo "4. DEPLOY_READY.md      - Guía rápida de deploy"
    echo "5. docs/DEPLOYMENT.md   - Guía detallada (2,800 líneas)"
    echo "6. README.md            - Documentación general"
    echo ""
    echo "Para leer un archivo:"
    echo "  cat ARCHIVO.md | less"
    echo ""
    read -p "Presiona Enter para continuar..."
}

# Main loop
while true; do
    show_menu
    read -p "Selecciona una opción: " choice
    
    case $choice in
        1) verify_setup ;;
        2) start_dev ;;
        3) build_prod ;;
        4) start_prod ;;
        5) show_status ;;
        6) show_logs ;;
        7) restart_app ;;
        8) health_check ;;
        9) clean_rebuild ;;
        10) show_docs ;;
        0) 
            clear
            echo "👋 ¡Hasta luego!"
            exit 0
            ;;
        *)
            echo "Opción inválida"
            sleep 1
            ;;
    esac
done
