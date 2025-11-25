import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import mysql.connector
from datetime import datetime 
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
SEND_TOPIC = "IoT/testESP32/sub"
RECEIVE_TOPICS = ["IoT/testESP32/pub"]  # subscribe to all topics
MSG_COUNT = 1  # number of messages to receive before exiting'''

# ------------------- Publish a message -------------------
data = {
	"horarios":[
		{"hora": "13:33:00", "porcion": 250},
		{"hora": "13:35:00", "porcion": 200},
	]
}

json_payload = json.dumps(data)
#payload_to_send = "informacion desde la raspberry"
publish.single(SEND_TOPIC, json_payload, hostname=MQTT_BROKER, port = 1883)
print(f"Published '{json_payload}' to topic '{SEND_TOPIC}'")

# ------------------- Receive message -------------------
msg = subscribe.simple(
    RECEIVE_TOPICS,
    hostname=MQTT_BROKER,
    retained=False,
    msg_count=1
)

payload = msg.payload.decode()
print(f"Received message '{payload}' on topic '{msg.topic}'")

data = json.loads(payload)


# ---------------------------------------------------------
#   INSERTAR EN LA TABLA normalized_readings
# ---------------------------------------------------------

# Convertimos solo la hora a un datetime completo (fecha hoy)
hora_str = data["hora"]
ts_utc = datetime.strptime(hora_str, "%H:%M:%S")
ts_utc = datetime.combine(datetime.today(), ts_utc.time())  # añade fecha de hoy


for sensor in data["sensores"]:
    sensor_id = sensor["id"]
    valor = sensor["valor"]
    unidad = sensor["unidad"]

    cursor.execute("""
        INSERT INTO normalized_readings (ts_utc, valor_limpio, unidades_convertidas, id_sensor)
        VALUES (%s, %s, %s, %s)
    """, (ts_utc, valor, unidad, sensor_id))

conn.commit()
print("Datos insertados en la tabla 'normalized_readings'")

conn.close()



# ------------------- Close MariaDB connection -------------------

conn.close()
