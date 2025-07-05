import time
import json
import pandas as pd
import paho.mqtt.publish as publish

# Load your CSV of pre-recorded readings
df = pd.read_csv('temp_reading.csv', parse_dates=['timestamp'])

# For each row, publish once per second
for _, row in df.iterrows():
    msg = json.dumps({
        'timestamp': row['timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ'),
        'temperature_C': row['temperature_C']
    })
    publish.single('dc/temperature/raw', msg, hostname='13.218.12.234')  # replace VM_IP if needed
    time.sleep(1)
