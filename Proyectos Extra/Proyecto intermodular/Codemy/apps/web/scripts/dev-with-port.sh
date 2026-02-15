#!/bin/bash
# Script para iniciar Next.js en el puerto especificado por la variable PORT o 3000 por defecto
PORT=${PORT:-3000}
next dev -p $PORT
