# ⚡ InfraGuard — Autonomous AIOps Self-Healing Platform

[

![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

](#)
[

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

](#)
[

![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)

](#)
[

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)

](#)
[

![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white)

](#)
[

![LangChain](https://img.shields.io/badge/LangChain-AI_Agent-1C3C3C?style=for-the-badge)

](#)
[

![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)

](#)
[

![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)

](#)
[

![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

](#)

> AI-powered infrastructure monitoring platform that detects anomalies,
> heals servers automatically, and explains every decision in plain English.
> Built for high-availability production environments.

---

## 🎯 What Is InfraGuard?

InfraGuard is an autonomous AIOps platform that:

- 🧠 **Learns** normal server behavior using Machine Learning
- 🔍 **Detects** anomalies before they become outages
- 🔧 **Heals** infrastructure automatically without human intervention
- 💬 **Explains** every decision in plain English via AI Agent
- 📊 **Tracks** SLO/SLI metrics following Google SRE principles
- 📄 **Reports** PDF incident reports with MTTR calculations
- 🚨 **Alerts** via Telegram in real time

---

## 🏗️ Architecture
Browser
↓
Nginx (Reverse Proxy + Security Headers)
↓
Flask App (Gunicorn + Eventlet)
↓
┌──────────────────────────────────────┐
│  collector.py  → metrics every 10s   │
│  detector.py   → ML anomaly detect   │
│  agent.py      → AI decision engine  │
│  healer.py     → auto-healing logic  │
│  slo.py        → SLO/SLI tracking    │
│  alerter.py    → Telegram alerts     │
│  reporter.py   → PDF reports         │
└──────────────────────────────────────┘
↓              ↓              ↓
SQLite DB      Redis Queue    ChromaDB
(AI Memory)
---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Framework | Flask 3.1 + Gunicorn + Eventlet |
| AI Agent | LangChain + GPT-4o-mini |
| ML Model | scikit-learn Isolation Forest |
| Vector Memory | ChromaDB |
| Monitoring | Prometheus + Grafana + Node-Exporter |
| Containers | Docker + Docker Compose |
| Proxy | Nginx |
| Cache | Redis |
| Database | SQLite |
| IaC | Terraform |
| Orchestration | Kubernetes manifests |
| CI/CD | GitHub Actions + Trivy security scan |
| Alerting | Telegram Bot API |
| Reporting | ReportLab PDF |
| Cloud | AWS EC2 |
| SRE | SLO/SLI/Error Budget tracking |

---

## 🚀 Quick Start

### Local Development
```bash
git clone https://github.com/Aslam-space/infraguard.git
cd infraguard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your keys
gunicorn app.routes:app --bind 0.0.0.0:8080 \
  --worker-class eventlet --workers 1
Docker Compose (Full Stack)
docker compose up -d --build
Terraform (Provision EC2)
cd terraform
terraform init
terraform plan
terraform apply
🤖 AI Agent
InfraGuard uses a LangChain AI agent with 5 tools:
Tool
What It Does
get_current_metrics
Reads live CPU/RAM/Disk
get_incident_history
Checks past incidents
check_anomaly
Runs ML detection
execute_healing
Runs bash heal script
get_avg_recovery_time
Calculates MTTR
Agent uses ChromaDB vector memory to remember past incidents and make smarter decisions over time.
🔧 Auto-Healing Scenarios
Anomaly
Detection
Action
Target MTTR
CPU > 90%
Isolation Forest
Kill top process
< 30s
RAM > 85%
Pattern detection
Drop cache + kill hog
< 30s
Disk > 85%
Threshold breach
Clean logs + Docker
< 60s
Service crash
Health check fail
Restart service
< 45s
📊 SLO/SLI Dashboard
Following Google SRE principles:
SLO Target:    99.9% uptime
Error Budget:  43.8 minutes/month
MTTR Target:   < 30 seconds
Heal Rate:     > 95%
🔒 DevSecOps Pipeline
git push → GitHub Actions triggered
         → Python import tests
         → Trivy security scan (Docker image)
         → Build verified
         → SSH deploy to EC2
         → Health check passes
         → Telegram notification sent
📁 Project Structure
infraguard/
├── app/
│   ├── routes.py       Flask API + startup
│   ├── agent.py        LangChain AI agent
│   ├── collector.py    Metrics collection
│   ├── detector.py     ML anomaly detection
│   ├── healer.py       Auto-healing logic
│   ├── alerter.py      Telegram alerts
│   ├── reporter.py     PDF reports
│   ├── slo.py          SLO/SLI tracking
│   ├── database.py     SQLite operations
│   └── config.py       Environment config
├── scripts/            Bash heal scripts
├── terraform/          AWS EC2 provisioning
├── k8s/                Kubernetes manifests
├── nginx/              Reverse proxy config
├── prometheus/         Metrics scraping
└── .github/workflows/  CI/CD pipeline
📡 API Endpoints
Method
Endpoint
Description
GET
/
Live dashboard
GET
/api/metrics
Current metrics
GET
/api/metrics/history
Last 60 readings
GET
/api/incidents
Recent incidents
GET
/api/status
System status
GET
/api/slo
SLO/SLI data
POST
/api/agent
Ask AI agent
POST
/api/heal
Trigger manual heal
GET
/api/report
Download PDF report
GET
/health
Health check
GET
/metrics
Prometheus metrics
👤 Author
Aslam A — Cloud & DevOps Engineer
[
�
Load image
](https://www.linkedin.com/in/aslama77)
[
�
Load image
](https://github.com/Aslam-space)
Open to DevOps, Cloud Engineering and Technical Support opportunities in Bangalore.
📄 License
MIT License — free to use and modify.
