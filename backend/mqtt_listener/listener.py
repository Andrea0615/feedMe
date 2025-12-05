import json
import paho.mqtt.client as mqtt

from utils.event_detector import detect_and_get_events
from services.event_service import save_event

BROKER = "broker.hivemq.com"
TOPIC = "IoT/testESP32/pub"

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("📩 MQTT recibido:", data)

        user_id = data.get("user_id")  # debe venir desde ESP32

        eventos = detect_and_get_events(data, user_id)

        for tipo, prioridad, fecha in eventos:
            if tipo != "" and prioridad > 0:
                save_event(tipo, prioridad, fecha, user_id)

    except Exception as e:
        print("❌ Error procesando MQTT:", e)

def start_listener():
    client = mqtt.Client()
    client.connect(BROKER, 1883)
    client.subscribe(TOPIC)
    client.on_message = on_message

    print("📡 MQTT Listener activo en", TOPIC)
    client.loop_forever()


if __name__ == "__main__":
    start_listener()
