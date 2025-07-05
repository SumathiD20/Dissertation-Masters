import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet
from datetime import datetime, time

# — Load the shared secret key —
with open('secret.key','rb') as f:
    cipher = Fernet(f.read())

# Configuration
OVERHEAT_THRESHOLD = 30.0        # °C, example for overheating
STRANGE_WINDOW = (22, 5)         # 22:00 → 05:00
STRANGE_EVENT_LIMIT = 3          # e.g. 3 openings in one night → VERY STRANGE

# State
night_openings = 0

def is_night(dt: datetime):
    """Return True if dt falls between 22:00 and 05:00."""
    if dt.hour >= 22 or dt.hour < 5:
        return True
    return False

def on_message(client, userdata, msg):
    global night_openings

    # 1. Decrypt and parse
    line = cipher.decrypt(msg.payload).decode()  
    # format is "2025-07-05T12:00:42Z,25.01"
    ts_str, temp_str = line.split(',')
    dt = datetime.fromisoformat(ts_str.replace('Z','+00:00'))
    temp = float(temp_str)

    # 2. Pass to cooling system (simulate)
    print(f"[COOLING] {dt.time()} → temperature = {temp:.2f}°C")

    # 3. Overheat detection
    if temp >= OVERHEAT_THRESHOLD:
        print(f"⚠️  OVERHEAT ALARM! {dt} reached {temp:.2f}°C")

    # 4. Door-opening detection window
    #    Any time we see a *masked* anomaly come through,
    #    that implies a door event. We detect it by the fact
    #    the masked temperature was drawn from the “anomaly” branch.
    #    Here we simply check for temperatures that _differ significantly_
    #    from the running mean as a proxy, or better: your stream processor
    #    could include a flag you republish. For simplicity:
    #
    delta = abs(temp - 25.0)  # ~0.1° for normal, ~0.1+ for masked anomalies
    if delta > 0.09:
        # We assume this reading was an anomaly mask
        if is_night(dt):
            night_openings += 1
            print(f"🔒 Night opening #{night_openings} detected at {dt.time()}")
            if night_openings >= STRANGE_EVENT_LIMIT:
                print("🚨 VERY STRANGE: multiple off-hours accesses detected!")
        else:
            print(f"🚪 Door event at {dt.time()}")

client = mqtt.Client()
client.connect('54.227.29.83', 1883)      # or localhost if local
client.subscribe('dc/temperature/masked')
client.on_message = on_message
print("Monitoring subscriber started...")
client.loop_forever()
