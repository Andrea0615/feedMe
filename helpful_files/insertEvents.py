from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import paho.mqtt.client as mqtt
import json

# Import your event detection logic from Script A
from eventos import detect_and_get_events  
from receiveSensorData import listen_and_store


def insertEvent(event_type, priority, timestamp, user_id):
    engine = create_engine("mariadb+pymysql://ras4:ras4@localhost/mqttesting")
    metadata = MetaData()
    metadata.reflect(bind=engine)

    SessionLocal = sessionmaker(bind=engine)
    mdb = SessionLocal()

    events_table = metadata.tables["eventos"]

    insert_stmt = events_table.insert().values(
        tipo_evento=event_type,
        prioridad=priority,
        fecha=timestamp,
        id_cuenta = user_id
    )

    mdb.execute(insert_stmt)
    mdb.commit()


def processIncomingData(json_data, user_id):
    events = detect_and_get_events(json_data, user_id)

    for event_type, priority, timestamp in events:
        if event_type != "" and priority > 0:
            insertEvent(event_type, priority, timestamp, user_id)

    return events
    
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with code:", rc)
    topic = userdata["topic"]
    client.subscribe(topic)
    print(f"Suscribed to topic: {topic}")
    

def on_message(client, userdata, msg):
    print(f"\nReceived message on {msg.topic}:")
    
    try:
        payload = json.loads(msg.payload.decode())
        print("JSON received:", payload)

        user_id = userdata["user_id"]

        # Store in normalized_readings
        listen_and_store(payload)

        # Detect events
        events = processIncomingData(payload, user_id)

        print("Detected events:", events)

    except json.JSONDecodeError:
        print("Error: MQTT JSON not valid.")

        
def start_mqtt_listener(user_id):
    BROKER = "broker.hivemq.com"
    PORT = 1883
    TOPIC = "IoT/testESP32/pub"

    client = mqtt.Client(userdata={"topic": TOPIC, "user_id": user_id})

    client.on_connect = on_connect
    client.on_message = on_message

    print("Conecting to MQTT...")
    client.connect(BROKER, PORT, 60)
    client.loop_forever()



if __name__ == "__main__":
    user_id = 1
    start_mqtt_listener(user_id)

