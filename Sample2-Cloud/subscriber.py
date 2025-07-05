import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet

with open('secret.key','rb') as f: key = f.read()
cipher = Fernet(key)

def on_message(client, userdata, msg):
    decrypted = cipher.decrypt(msg.payload).decode()
    print("Clean data:", decrypted)

client = mqtt.Client()
client.connect('13.218.12.234',1883)
client.subscribe('dc/temperature/masked')
client.on_message = on_message
client.loop_forever()
