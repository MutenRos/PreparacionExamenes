#!/bin/bash

# Script para arrancar el servidor solo si no está corriendo

PORT=3000

# Verificar si el puerto está en uso
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "✓ El servidor ya está corriendo en el puerto $PORT"
    echo "→ http://localhost:$PORT"
else
    echo "⚡ Arrancando servidor en puerto $PORT..."
    npm run dev
fi
