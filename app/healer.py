import subprocess
import time
import os
from app.database import insert_incident, resolve_incident
from app.config import HEAL_ENABLED

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts')

def run_script(script_name):
    path = os.path.join(SCRIPTS_DIR, script_name)
    os.chmod(path, 0o755)
    result = subprocess.run(
        ['bash', path],
        capture_output=True, text=True, timeout=60
    )
    return result.returncode == 0, result.stdout + result.stderr

def heal(anomaly_type, metric_value):
    if not HEAL_ENABLED:
        return False, 0, "Healing disabled"

    print(f"[Healer] Healing {anomaly_type} = {metric_value}%")

    script_map = {
        "CPU":     "heal_cpu.sh",
        "MEMORY":  "heal_memory.sh",
        "DISK":    "heal_disk.sh",
        "SERVICE": "heal_service.sh",
        "GENERAL": "heal_cpu.sh"
    }

    script      = script_map.get(anomaly_type, "heal_cpu.sh")
    start_time  = time.time()
    incident_id = insert_incident(
        anomaly_type, "HIGH", metric_value, f"Running {script}"
    )

    success, output = run_script(script)
    mttr = round(time.time() - start_time, 1)

    if success:
        resolve_incident(incident_id, mttr)
        print(f"[Healer] Healed in {mttr}s")

    return success, mttr, output
