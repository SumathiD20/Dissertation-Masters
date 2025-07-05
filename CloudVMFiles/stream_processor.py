import json
import numpy as np
import joblib
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt

# Load the model & key
model = joblib.load('iforest.joblib')
with open('secret.key','rb') as f:
    key = f.read()
cipher = Fernet(key)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    temp = data['temperature_C']
    t = data['timestamp']
    is_anomaly = (model.predict([[temp]]) == -1)
    # Mask: big noise for anomalies, small noise otherwise
    out_temp = (25.0 + np.random.normal(0,0.1)) if is_anomaly else (temp + np.random.normal(0,0.02))
    line = f"{t},{out_temp:.2f}".encode()
    encrypted = cipher.encrypt(line)
    client.publish('dc/temperature/masked', encrypted)

client = mqtt.Client()
client.connect('localhost',1883)
client.subscribe('dc/temperature/raw')
client.on_message = on_message
client.loop_forever()
