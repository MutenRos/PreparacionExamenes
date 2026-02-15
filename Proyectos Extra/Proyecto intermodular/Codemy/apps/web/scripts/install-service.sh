#!/bin/bash

# Script para instalar Codeacademy como servicio systemd
# Esto garantiza que el servidor se inicie automáticamente al arrancar el sistema

SERVICE_NAME="codeacademy"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
USER=$(whoami)
WORK_DIR="/home/dario/codeacademy/apps/web"

echo "🔧 Instalando Codeacademy como servicio systemd..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Crear archivo de servicio
sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Codeacademy Next.js Server (Immortal Mode)
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$WORK_DIR
Environment="NODE_ENV=production"
Environment="PORT=3000"
ExecStart=/bin/bash $WORK_DIR/scripts/keep-alive.sh
Restart=always
RestartSec=10
StandardOutput=append:$WORK_DIR/service.log
StandardError=append:$WORK_DIR/service-error.log

# Límites de recursos
LimitNOFILE=65536
TimeoutStartSec=0

# Reinicio agresivo
StartLimitInterval=0
StartLimitBurst=0

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Archivo de servicio creado en: $SERVICE_FILE"

# Recargar systemd
echo "🔄 Recargando systemd..."
sudo systemctl daemon-reload

# Habilitar servicio para inicio automático
echo "⚡ Habilitando inicio automático..."
sudo systemctl enable $SERVICE_NAME

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ¡Instalación completada!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Comandos disponibles:"
echo "  sudo systemctl start $SERVICE_NAME    - Iniciar servidor"
echo "  sudo systemctl stop $SERVICE_NAME     - Detener servidor"
echo "  sudo systemctl restart $SERVICE_NAME  - Reiniciar servidor"
echo "  sudo systemctl status $SERVICE_NAME   - Ver estado"
echo "  sudo journalctl -u $SERVICE_NAME -f   - Ver logs en tiempo real"
echo ""
echo "El servidor ahora se iniciará automáticamente:"
echo "  ✓ Al arrancar el sistema"
echo "  ✓ Si se cae por cualquier motivo"
echo "  ✓ Incluso después de múltiples fallos"
echo ""
