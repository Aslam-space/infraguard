#!/bin/bash
echo "[heal_cpu] Starting CPU healing..."
TOP_PID=$(ps aux --sort=-%cpu | grep -v -E "PID|systemd|sshd|bash|ps|grep" | head -1 | awk '{print $2}')
if [ -n "$TOP_PID" ]; then
    PROC=$(ps -p $TOP_PID -o comm= 2>/dev/null)
    kill -15 $TOP_PID 2>/dev/null
    echo "[heal_cpu] Killed PID $TOP_PID ($PROC)"
else
    echo "[heal_cpu] No killable process found"
fi
echo "[heal_cpu] Done"
