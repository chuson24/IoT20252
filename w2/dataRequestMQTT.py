import paho.mqtt.client as mqtt
import ssl
import json
import time

# ===== CONFIG =====
BROKER = "50daabe16f99471ba3a35695492d4d2a.s1.eu.hivemq.cloud"
PORT = 8883
TOPIC = "/mqtt_demo"
QOS = 0

USERNAME = "iot20251"
PASSWORD = "Iot20251"

# ===== CALLBACK =====
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to broker")
        client.subscribe(TOPIC, qos=QOS)
    else:
        print("❌ Failed to connect, code:", rc)

def on_message(client, userdata, msg):
    print(f"\n📩 Received from {msg.topic}")
    payload = msg.payload.decode()
    print("Raw:", payload)

    try:
        data = json.loads(payload)
        print("Parsed:")
        print(" - devID:", data.get("devID"))
        print(" - packetno:", data.get("packetno"))
        print(" - temperature:", data.get("temperature"))
        print(" - humidity:", data.get("humidity"))
    except:
        print("⚠️ Not JSON format")

# ===== CLIENT =====
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)

# TLS (bắt buộc cho HiveMQ Cloud)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.tls_insecure_set(False)

client.on_connect = on_connect
client.on_message = on_message

print("Connecting...")
client.connect(BROKER, PORT, 60)

client.loop_start()

# ===== PUBLISH TEST =====
while True:
    data = {
        "devID": "mqttbox01",
        "packetno": int(time.time()),
        "temperature": 30,
        "humidity": 60
    }

    payload = json.dumps(data)

    print("\n📤 Publishing:", payload)
    client.publish(TOPIC, payload, qos=QOS)

    time.sleep(5)