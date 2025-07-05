import pandas as pd
from sklearn.ensemble import IsolationForest

# 1. Load the CSV without parsing timestamp yet
df = pd.read_csv('temp_reading.csv')

# 2. Filter out rows where 'timestamp' starts with a non-date string (like a comment)
df = df[~df['timestamp'].astype(str).str.startswith('#')]

# 3. Convert 'timestamp' to datetime now that bad rows are removed
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows where timestamp couldn't be converted
df = df.dropna(subset=['timestamp'])

# 4. Train on a “quiet” period (first 10 seconds)
quiet = df[df['timestamp'] < df['timestamp'].iloc[0] + pd.Timedelta(seconds=20)]

model = IsolationForest(contamination=0.01, random_state=42)
model.fit(quiet[['temperature_C']])

# 5. Score the entire dataset
df['anomaly'] = model.predict(df[['temperature_C']]) == -1

# 6. Extract timestamps where anomalies occur
spikes = df[df['anomaly']][['timestamp', 'temperature_C']]
spikes.to_csv('detected_spikes.csv', index=False)

print("Done! Detected spikes saved to detected_spikes.csv:")
print(spikes)
