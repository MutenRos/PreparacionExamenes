#!/bin/bash
# Create dynamic timestamp
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Define base and destination
DEST_DIR="/var/backups/josevicente/$TIMESTAMP"

# Create directories
sudo mkdir -p "$DEST_DIR"

# Copy files
sudo cp -r /home/josevicente/* "$DEST_DIR/"

# Optional: show confirmation
echo "Backup completed: $DEST_DIR"
