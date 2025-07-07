import json
import numpy as np
import joblib
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt

# — Load the trained Isolation Forest model and the secret key —
model = joblib.load('iforest.joblib')
with open('secret.key', 'rb') as f:
    key = f.read()
cipher = Fernet(key)

# — Thresholds —
OVERHEAT_THRESHOLD = 30.0

def on_message(client, userdata, msg):
    # 1. Parse the incoming temperature data
    data = json.loads(msg.payload)
    temp = data['temperature_C']
    t = data['timestamp']

    # 2. Detect anomaly
    is_anomaly = (model.predict([[temp]]) == -1)

    # 3. Decide whether to apply masking
    if temp >= OVERHEAT_THRESHOLD:
        # 🔥 Do NOT mask overheating – pass the real value through
        out_temp = temp
        is_anomaly = False  # not treated as privacy-sensitive
        print(f"🚨 Overheating! Passing through real value: {temp:.2f}°C at {t}")
    elif is_anomaly:
        # 🛡️ Apply stronger noise to hide door-opening patterns
        out_temp = 25.0 + np.random.normal(0, 0.1)
        print(f"[ANOMALY] {t} raw={temp:.2f}°C → masked as {out_temp:.2f}°C")
    else:
        # ✅ Normal reading with minimal noise
        out_temp = temp + np.random.normal(0, 0.02)

    # 4. Build the output payload with anomaly flag
    payload = {
        "timestamp": t,
        "temperature": round(out_temp, 2),
        "anomaly": bool(is_anomaly)
    }

    # 5. Encrypt and publish
    encrypted = cipher.encrypt(json.dumps(payload).encode())
    client.publish('dc/temperature/masked', encrypted)

# — MQTT setup —
client = mqtt.Client()
client.connect('localhost', 1883)
client.subscribe('dc/temperature/raw')
client.on_message = on_message

print("🔐 Stream Processor Running... Listening for temperature data.")
client.loop_forever()
