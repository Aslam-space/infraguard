import os
import threading
import time
from flask import Flask, render_template, jsonify, send_file, Response
from flask_socketio import SocketIO
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.database import init_db, get_recent_metrics, get_recent_incidents, get_avg_mttr
from app.collector import start_collector, get_latest
from app.detector import start_detector, detect, train_model, get_anomaly_type
from app.healer import heal
from app.alerter import alert_anomaly, alert_healed
from app.reporter import generate_report
from app.slo import get_slo_summary
from app.agent import run_agent

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'infraguard-2026'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# ==============================================================
# Background monitor loop
# ==============================================================
def monitor_loop():
    time.sleep(30)  # wait for data to accumulate
    while True:
        try:
            m = get_latest()
            is_anomaly, score = detect(
                m['cpu'], m['ram'], m['disk'],
                m['net_in'], m['net_out']
            )
            if is_anomaly:
                atype, severity, value = get_anomaly_type(
                    m['cpu'], m['ram'], m['disk']
                )
                alert_anomaly(atype, value, score)
                success, mttr, _ = heal(atype, value)
                if success:
                    alert_healed(atype, mttr)

            # Retrain model every 100 cycles
            monitor_loop.counter = getattr(monitor_loop, 'counter', 0) + 1
            if monitor_loop.counter % 100 == 0:
                threading.Thread(target=train_model, daemon=True).start()

            # Push live metrics to dashboard
            socketio.emit('metrics_update', m)

        except Exception as e:
            print(f"[Monitor] {e}")
        time.sleep(10)

# ==============================================================
# Routes
# ==============================================================
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/metrics')
def api_metrics():
    return jsonify(get_latest())

@app.route('/api/metrics/history')
def api_history():
    return jsonify(get_recent_metrics(60))

@app.route('/api/incidents')
def api_incidents():
    return jsonify(get_recent_incidents(10))

@app.route('/api/status')
def api_status():
    m = get_latest()
    if m['cpu'] > 90 or m['ram'] > 85 or m['disk'] > 85:
        status = 'CRITICAL'
    elif m['cpu'] > 75 or m['ram'] > 75 or m['disk'] > 75:
        status = 'WARNING'
    else:
        status = 'NOMINAL'
    return jsonify({
        'status':   status,
        'metrics':  m,
        'avg_mttr': get_avg_mttr()
    })

@app.route('/api/slo')
def api_slo():
    return jsonify(get_slo_summary())

@app.route('/api/agent', methods=['POST'])
def api_agent():
    from flask import request
    prompt = request.json.get('prompt', 'Check server health and fix any issues')
    result = run_agent(prompt)
    return jsonify({'response': result})

@app.route('/api/report')
def api_report():
    path = generate_report()
    return send_file(path, as_attachment=True,
                     download_name='infraguard_report.pdf')

@app.route('/api/heal', methods=['POST'])
def api_heal():
    m = get_latest()
    atype, _, value = get_anomaly_type(m['cpu'], m['ram'], m['disk'])
    success, mttr, output = heal(atype, value)
    return jsonify({'success': success, 'mttr': mttr, 'output': output})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/metrics')
def prometheus_metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# ==============================================================
# Startup — runs once when app starts
# ==============================================================
def startup():
    init_db()
    start_collector()
    start_detector()
    threading.Thread(target=monitor_loop, daemon=True).start()
    print("[InfraGuard] All systems started ✅")

startup()
