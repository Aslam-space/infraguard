import time
from app.database import get_recent_metrics, get_recent_incidents

# SLO targets (industry standard)
UPTIME_TARGET    = 99.9   # 99.9% uptime per month
ERROR_RATE_MAX   = 0.1    # max 0.1% error rate
LATENCY_TARGET   = 200    # 200ms response time target

# Track start time for uptime calculation
START_TIME = time.time()

def get_uptime_percent():
    """Calculate uptime % based on incidents"""
    incidents  = get_recent_incidents(limit=100)
    total_time = time.time() - START_TIME

    if total_time == 0:
        return 100.0

    # Sum all downtime from unresolved incidents (estimate 60s each)
    downtime = sum(
        i['mttr_seconds'] if i['mttr_seconds'] else 60
        for i in incidents
    )

    uptime = ((total_time - downtime) / total_time) * 100
    return round(min(uptime, 100.0), 3)

def get_error_budget():
    """
    Error budget = how much downtime you are allowed this month
    At 99.9% SLO: allowed 43.8 minutes downtime per month
    """
    allowed_downtime_mins = 43.8   # 99.9% SLO = 43.8 min/month
    incidents = get_recent_incidents(limit=100)

    used_mins = sum(
        (i['mttr_seconds'] or 60) / 60
        for i in incidents
        if i['resolved'] == 0
    )

    remaining       = max(allowed_downtime_mins - used_mins, 0)
    percent_used    = round((used_mins / allowed_downtime_mins) * 100, 1)
    percent_left    = round(100 - percent_used, 1)

    return {
        "allowed_minutes":   allowed_downtime_mins,
        "used_minutes":      round(used_mins, 2),
        "remaining_minutes": round(remaining, 2),
        "percent_used":      percent_used,
        "percent_left":      percent_left,
        "status": "CRITICAL" if percent_used > 90
                  else "WARNING" if percent_used > 50
                  else "HEALTHY"
    }

def get_slo_summary():
    """Full SLO dashboard data"""
    uptime   = get_uptime_percent()
    budget   = get_error_budget()
    metrics  = get_recent_metrics(limit=10)

    avg_cpu  = round(sum(m['cpu']  for m in metrics) / len(metrics), 1) if metrics else 0
    avg_ram  = round(sum(m['ram']  for m in metrics) / len(metrics), 1) if metrics else 0

    return {
        "uptime_percent":    uptime,
        "uptime_target":     UPTIME_TARGET,
        "slo_met":           uptime >= UPTIME_TARGET,
        "error_budget":      budget,
        "avg_cpu":           avg_cpu,
        "avg_ram":           avg_ram,
        "latency_target_ms": LATENCY_TARGET,
    }
