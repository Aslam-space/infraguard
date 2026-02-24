import psutil
import threading
import time
from app.database import insert_metric
from app.config import COLLECT_INTERVAL

# Shared latest metrics
latest = {
    "cpu": 0, "ram": 0, "disk": 0,
    "net_in": 0, "net_out": 0, "processes": 0
}

def collect():
    global latest
    old_net = psutil.net_io_counters()
    while True:
        try:
            cpu     = psutil.cpu_percent(interval=1)
            ram     = psutil.virtual_memory().percent
            disk    = psutil.disk_usage('/').percent
            procs   = len(psutil.pids())
            new_net = psutil.net_io_counters()
            net_in  = round((new_net.bytes_recv - old_net.bytes_recv) / 1024, 2)
            net_out = round((new_net.bytes_sent - old_net.bytes_sent) / 1024, 2)
            old_net = new_net
            latest  = {
                "cpu": cpu, "ram": ram, "disk": disk,
                "net_in": net_in, "net_out": net_out,
                "processes": procs
            }
            insert_metric(cpu, ram, disk, net_in, net_out, procs)
        except Exception as e:
            print(f"[Collector Error] {e}")
        time.sleep(COLLECT_INTERVAL)

def start_collector():
    t = threading.Thread(target=collect, daemon=True)
    t.start()
    print("[Collector] Started — every 10s")

def get_latest():
    return latest
