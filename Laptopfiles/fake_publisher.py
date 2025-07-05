import time, json
import pandas as pd
import paho.mqtt.publish as publish

df = pd.read_csv('temp_reading.csv', parse_dates=['timestamp'])

for _, row in df.iterrows():
    msg = json.dumps({
        'timestamp': row['timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ'),
        'temperature_C': row['temperature_C']
    })
    publish.single('dc/temperature/raw', msg, hostname='52.54.148.118')
    time.sleep(1)
