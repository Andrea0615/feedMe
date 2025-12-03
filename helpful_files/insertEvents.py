from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# Import your event detection logic from Script A
from eventos import detect_and_get_events  


def insertEvent(event_type, priority, timestamp):
    engine = create_engine("mariadb+pymysql://ras4:ras4@localhost/mqttesting")
    metadata = MetaData()
    metadata.reflect(bind=engine)

    SessionLocal = sessionmaker(bind=engine)
    mdb = SessionLocal()

    events_table = metadata.tables["eventos"]

    insert_stmt = events_table.insert().values(
        tipo=event_type,
        prioridad=priority,
        fecha=timestamp
    )

    mdb.execute(insert_stmt)
    mdb.commit()


def processIncomingData(json_data):
    events = detect_and_get_events(json_data)

    for event_type, priority, timestamp in events:
        if event_type != "" and priority > 0:
            insertEvent(event_type, priority, timestamp)

    return events
