import json
import paho.mqtt.publish as publish

def publish_schedule_to_device(horarios):
    BROKER = "broker.hivemq.com"
    TOPIC = "IoT/testESP32/sub"

    payload = {"horarios": horarios}

    publish.single(
        TOPIC,
        json.dumps(payload),
        hostname=BROKER,
        port=1883
    )

    print(f"[MQTT] Enviado a ESP32 → {payload}")
