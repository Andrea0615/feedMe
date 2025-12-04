import json
import sys
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError

import paho.mqtt.publish as publish


def get_db_engine():
    try:
        engine = create_engine("mariadb+pymysql://ras4:ras4@localhost/mqttesting")
        return engine
    except SQLAlchemyError as e:
        print(f"SQLAlchemy connection error: {e}")
        sys.exit(1)


def publish_json(broker, topic, data):
    json_payload = json.dumps(data)
    publish.single(topic, json_payload, hostname=broker, port=1883)
    print(f"Published to '{topic}': {json_payload}")


def get_schedule_payload(engine, id_plan):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    horarios_table = metadata.tables["horarios"]

    with engine.connect() as conn:
        rows = conn.execute(
            horarios_table.select().where(horarios_table.c.id_plan == id_plan)
        ).fetchall()

    horarios_list = []
    for row in rows:
        horarios_list.append({
            "hora": row.hora.strftime("%H:%M:%S"),
            "porcion": row.porcion
        })

    return {"horarios": horarios_list}


def send_schedule(id_plan):
    engine = get_db_engine()

    BROKER = "broker.hivemq.com"
    SEND_TOPIC = "IoT/testESP32/sub"

    # Get schedule from DB
    schedule_payload = get_schedule_payload(engine, id_plan)

    print(f"Sending schedule for id_plan={id_plan}")
    publish_json(BROKER, SEND_TOPIC, schedule_payload)


if __name__ == "__main__":
    send_schedule(id_plan=1)
