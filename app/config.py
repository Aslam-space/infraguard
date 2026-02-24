import os
from dotenv import load_dotenv
load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID     = os.getenv("TELEGRAM_CHAT_ID", "")

# OpenAI
OPENAI_API_KEY       = os.getenv("OPENAI_API_KEY", "")
AI_PROVIDER          = os.getenv("AI_PROVIDER", "openai")

# Flask
PORT                 = int(os.getenv("PORT", 8080))
FLASK_DEBUG          = os.getenv("FLASK_DEBUG", "0") == "1"

# Redis
REDIS_URL            = os.getenv("REDIS_URL", "redis://localhost:6379")

# Database
DB_PATH              = os.getenv("DB_PATH",    "data/infraguard.db")
MODEL_PATH           = os.getenv("MODEL_PATH", "data/model/anomaly_model.pkl")

# Thresholds
ALERT_CPU_THRESHOLD  = int(os.getenv("ALERT_CPU_THRESHOLD",  90))
ALERT_RAM_THRESHOLD  = int(os.getenv("ALERT_RAM_THRESHOLD",  85))
ALERT_DISK_THRESHOLD = int(os.getenv("ALERT_DISK_THRESHOLD", 85))

# Features
HEAL_ENABLED        = os.getenv("HEAL_ENABLED", "true").lower() == "true"
COLLECT_INTERVAL    = int(os.getenv("COLLECT_INTERVAL", 10))
MODEL_RETRAIN_HOURS = int(os.getenv("MODEL_RETRAIN_HOURS", 24))
