import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet

with open('secret.key','rb') as f:
    key = f.read()
cipher = Fernet(key)

def on_message(client, userdata, msg):
    print("Clean data:", cipher.decrypt(msg.payload).decode())

client = mqtt.Client()
client.connect('52.54.148.118', 1883)
client.subscribe('dc/temperature/masked')
client.on_message = on_message
client.loop_forever()
