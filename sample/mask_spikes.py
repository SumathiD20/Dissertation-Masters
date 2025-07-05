import pandas as pd
import numpy as np

# 1. Load the original data and the detected spikes
df = pd.read_csv('temp_reading.csv', comment='#')
df['timestamp'] = pd.to_datetime(df['timestamp'])
spikes = pd.read_csv('detected_spikes.csv', parse_dates=['timestamp'])

# 2. Define a window around each spike (e.g. 2 seconds before & after)
WINDOW = pd.Timedelta(seconds=2)

# 3. Mark points to mask
df['to_mask'] = False
for t in spikes['timestamp']:
    start = t - WINDOW
    end   = t + WINDOW
    df.loc[(df['timestamp'] >= start) & (df['timestamp'] <= end), 'to_mask'] = True

# 4. Apply smoothing interpolation
#    - Save original so you can compare later
df['orig_temp'] = df['temperature_C']

#    - Interpolate across masked regions
df.loc[df['to_mask'], 'temperature_C'] = np.nan
df['temperature_C'] = df['temperature_C'].interpolate(method='linear')

# 5. (Optional) Or inject noise instead of smoothing:
#noise_sigma = 0.1
#mask_idxs = df['to_mask']
#df.loc[mask_idxs, 'temperature_C'] = df.loc[mask_idxs, 'orig_temp'] + np.random.normal(0, noise_sigma, mask_idxs.sum())

# 6. Clean up and save
df.drop(columns=['to_mask','orig_temp'], inplace=True)
df['temperature_C'] = df['temperature_C'].round(2)
df.to_csv('masked_temperature.csv', index=False)

print("Done—all dips have been masked and written to masked_temperature.csv")
