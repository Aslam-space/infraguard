import os
import pickle
import numpy as np
import threading
from sklearn.ensemble import IsolationForest
from app.database import get_recent_metrics
from app.config import MODEL_PATH

model = None
model_lock = threading.Lock()

def get_features(metrics_list):
    return np.array([
        [m['cpu'], m['ram'], m['disk'], m['net_in'], m['net_out']]
        for m in metrics_list
    ])

def train_model():
    global model
    metrics = get_recent_metrics(limit=500)
    if len(metrics) < 50:
        print(f"[Detector] Need 50+ samples, have {len(metrics)}")
        return False
    X = get_features(metrics)
    clf = IsolationForest(
        contamination=0.1,
        random_state=42,
        n_estimators=100
    )
    clf.fit(X)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(clf, f)
    with model_lock:
        model = clf
    print(f"[Detector] Model trained on {len(metrics)} samples")
    return True

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            with model_lock:
                model = pickle.load(f)
        print("[Detector] Model loaded from disk")
        return True
    return False

def detect(cpu, ram, disk, net_in, net_out):
    with model_lock:
        m = model
    if m is None:
        return False, 0.0
    X          = np.array([[cpu, ram, disk, net_in, net_out]])
    prediction = m.predict(X)[0]
    score      = m.decision_function(X)[0]
    return prediction == -1, round(float(score), 4)

def get_anomaly_type(cpu, ram, disk):
    if cpu  > 90: return "CPU",    "CRITICAL", cpu
    if ram  > 85: return "MEMORY", "HIGH",     ram
    if disk > 85: return "DISK",   "HIGH",     disk
    return "GENERAL", "MEDIUM", max(cpu, ram, disk)

def start_detector():
    if not load_model():
        print("[Detector] No model yet — trains after 50 samples")
    print("[Detector] Started")
