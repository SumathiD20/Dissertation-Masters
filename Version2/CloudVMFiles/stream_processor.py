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

def on_message(client, userdata, msg):
    # 1. Parse incoming JSON
    data = json.loads(msg.payload)
    temp = data['temperature_C']
    t = data['timestamp']

    # 2. Detect anomaly (door‐opening dip)
    is_anomaly = (model.predict([[temp]]) == -1)
    if is_anomaly:
        # Print to console whenever an anomaly is found
        print(f"[ANOMALY] {t} raw={temp:.2f}°C")

    # 3. Mask: big noise for anomalies, small noise otherwise
    if is_anomaly:
        out_temp = 25.0 + np.random.normal(0, 0.1)
    else:
        out_temp = temp + np.random.normal(0, 0.02)

    # 4. Encrypt the “timestamp,masked_temp” line
    line = f"{t},{out_temp:.2f}".encode()
    encrypted = cipher.encrypt(line)

    # 5. Publish the masked & encrypted payload
    client.publish('dc/temperature/masked', encrypted)

# — MQTT setup —
client = mqtt.Client()
client.connect('localhost', 1883)
client.subscribe('dc/temperature/raw')
client.on_message = on_message

# — Start processing loop —
print("Stream processor started, listening for raw data...")
client.loop_forever()
