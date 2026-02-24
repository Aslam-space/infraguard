import requests
from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(message):
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_bot_token_here":
        print(f"[Alerter] Telegram not set — {message[:50]}")
        return False
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML"
            },
            timeout=10
        )
        return r.status_code == 200
    except Exception as e:
        print(f"[Alerter] Error: {e}")
        return False

def alert_anomaly(anomaly_type, metric_value, score):
    emoji = {"CPU":"🔴","MEMORY":"🟡","DISK":"🟠"}.get(anomaly_type,"⚠️")
    send_telegram(
        f"{emoji} <b>InfraGuard Alert</b>\n\n"
        f"<b>Type:</b> {anomaly_type}\n"
        f"<b>Value:</b> {metric_value}%\n"
        f"<b>Anomaly Score:</b> {score}\n"
        f"<b>Status:</b> Auto-healing initiated..."
    )

def alert_healed(anomaly_type, mttr):
    send_telegram(
        f"✅ <b>InfraGuard Healed</b>\n\n"
        f"<b>Type:</b> {anomaly_type}\n"
        f"<b>MTTR:</b> {mttr} seconds\n"
        f"<b>Status:</b> System back to normal"
    )

def alert_deploy(status, commit=""):
    emoji = "✅" if status == "success" else "❌"
    send_telegram(
        f"{emoji} <b>Deploy {status.upper()}</b>\n"
        f"<b>Commit:</b> {commit}"
    )
