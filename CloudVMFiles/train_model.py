import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

df = pd.read_csv('temp_reading.csv', parse_dates=['timestamp'])
quiet = df[df['timestamp'] < df['timestamp'].iloc[0] + pd.Timedelta(seconds=10)]

model = IsolationForest(contamination=0.01, random_state=42)
model.fit(quiet[['temperature_C']])
joblib.dump(model, 'iforest.joblib')
print("Model saved as iforest.joblib")
