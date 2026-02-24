#!/bin/bash
SERVICE=${1:-"infraguard"}
echo "[heal_service] Restarting $SERVICE..."
sudo systemctl restart $SERVICE 2>/dev/null || \
docker restart $SERVICE 2>/dev/null || \
echo "[heal_service] Could not restart $SERVICE"
echo "[heal_service] Done"
