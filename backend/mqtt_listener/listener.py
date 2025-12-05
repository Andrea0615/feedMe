import json
import paho.mqtt.client as mqtt

from utils.readings_saver import save_raw_data
from utils.event_detector import detect_and_get_events
from services.event_service import save_event

BROKER = "broker.hivemq.com"
TOPIC = "IoT/testESP32/pub"
USER_ID = 1  # ya lo dinamizaremos


def on_connect(client, userdata, flags, rc):
    print("MQTT conectado:", rc)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("\n📥 Recibido MQTT:", data)

        # 1️⃣ Guardar en sensoresDB
        save_raw_data(data)

        # 2️⃣ Detectar eventos
        events = detect_and_get_events(data, USER_ID)
        print("EVENTOS DETECTADOS:", events)


        # 3️⃣ Guardarlos en appDB
        for e_type, priority, timestamp in events:
            if e_type and priority > 0:
                save_event(e_type, priority, timestamp, USER_ID)

        print("✔ Procesado correctamente\n")

    except Exception as e:
        print("❌ Error procesando MQTT:", e)


def start_mqtt_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, 1883, 60)
    client.loop_forever()
