#!/bin/bash
echo "[heal_memory] Starting memory healing..."
sync
echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true
TOP_PID=$(ps aux --sort=-%mem | grep -v -E "PID|systemd|sshd|bash|ps|grep" | head -1 | awk '{print $2}')
if [ -n "$TOP_PID" ]; then
    PROC=$(ps -p $TOP_PID -o comm= 2>/dev/null)
    kill -15 $TOP_PID 2>/dev/null
    echo "[heal_memory] Killed PID $TOP_PID ($PROC)"
fi
echo "[heal_memory] Done"
