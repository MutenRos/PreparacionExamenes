#!/bin/bash
# Install OmniERP Monitor as systemd service

SERVICE_FILE="/home/dario/omnierp-monitor.service"
SERVICE_DEST="/etc/systemd/system/omnierp-monitor.service"

echo "📦 Instalando OmniERP Monitor Service..."

# Copy service file
sudo cp "$SERVICE_FILE" "$SERVICE_DEST"
sudo chmod 644 "$SERVICE_DEST"

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable omnierp-monitor.service

# Start the service
sudo systemctl start omnierp-monitor.service

echo ""
echo "✅ Servicio instalado correctamente"
echo ""
echo "Comandos útiles:"
echo "  Ver estado:       sudo systemctl status omnierp-monitor.service"
echo "  Ver logs:         sudo journalctl -u omnierp-monitor.service -f"
echo "  Parar monitor:    sudo systemctl stop omnierp-monitor.service"
echo "  Reiniciar:        sudo systemctl restart omnierp-monitor.service"
echo ""
