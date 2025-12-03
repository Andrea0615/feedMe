from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# Import your event detection logic from Script A
from eventos import detect_and_get_events  


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
    
if __name__ == "__main__":
    json_data_sample = {
        "hora": "14:07:00",
        "horario": "14:07:00",
        "sensores": [
            {"id": 1, "valor": 2, "unidad": "cm"},
            {"id": 2, "valor": 150, "unidad": "g"}
        ]
    }
    user_id = 1

    events = processIncomingData(json_data_sample, user_id)
    print("Eventos detectados:")
    print(events)

