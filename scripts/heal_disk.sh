#!/bin/bash
echo "[heal_disk] Starting disk healing..."
find /var/log -name "*.log" -size +50M -delete 2>/dev/null
find /tmp -mtime +3 -delete 2>/dev/null
docker system prune -f 2>/dev/null || true
journalctl --vacuum-size=50M 2>/dev/null || true
echo "[heal_disk] Done"
