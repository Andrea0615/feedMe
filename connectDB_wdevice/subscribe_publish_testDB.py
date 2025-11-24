import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import mysql.connector
import json
import sys

# ------------------- MariaDB / MySQL Connection -------------------
try:
    conn = mysql.connector.connect(
        user="ras4",
        password="ras4",
        host="localhost",
        database="mqttesting"
    )
    cursor = conn.cursor()
except mysql.connector.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

# ------------------- MQTT Settings -------------------
MQTT_BROKER = "broker.hivemq.com"
SEND_TOPIC = "IoT/ras4/equipo3/comedero/schedule"
RECEIVE_TOPICS = ["IoT/testESP32/sub"]  # subscribe to all topics
MSG_COUNT = 1  # number of messages to receive before exiting'''

# ------------------- Publish a message -------------------
data = {
	"hora":"12:00:00",
	"porcion": 300
}
json_payload = json.dumps(data)
#payload_to_send = "informacion desde la raspberry"
publish.single(SEND_TOPIC, json_payload, hostname=MQTT_BROKER, port = 1883)
print(f"Published '{json_payload}' to topic '{SEND_TOPIC}'")
message=subscribe.simple(RECEIVE_TOPICS, hostname=MQTT_BROKER, retained=False, msg_count=MSG_COUNT)
payload = message.payload.decode()  # convert bytes to string
print(f"Received message '{payload}' on topic '{RECEIVE_TOPICS}'")
'''
# ------------------- Subscribe and store messages -------------------
messages = subscribe.simple(
    RECEIVE_TOPICS,
    hostname=MQTT_BROKER,
    retained=False,
    msg_count=MSG_COUNT
)

for msg in messages:
    topic = msg.topic
    payload = msg.payload.decode()  # convert bytes to string
    print(f"Received message '{payload}' on topic '{topic}'")

    # Insert into MariaDB
    try:
        cursor.execute(
            "INSERT INTO mqtt_data (topic, message) VALUES (%s, %s)",
            (topic, payload)
        )
        conn.commit()
        print("Inserted into MariaDB successfully")
    except mysql.connector.Error as e:
        print(f"Error inserting into MariaDB: {e}")

# ------------------- Close MariaDB connection -------------------
'''
conn.close()
