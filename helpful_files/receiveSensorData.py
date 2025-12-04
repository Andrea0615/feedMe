import json
import sys
from datetime import datetime

import paho.mqtt.subscribe as subscribe

from sqlalchemy import create_engine, MetaData, insert
from sqlalchemy.exc import SQLAlchemyError


def get_db_engine():
    try:
        engine = create_engine("mariadb+pymysql://ras4:ras4@localhost/mqttesting")
        return engine
    except SQLAlchemyError as e:
        print(f"SQLAlchemy connection error: {e}")
        sys.exit(1)


def load_tables(engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return {
        "normalized_readings": metadata.tables["normalized_readings"]
    }


def extract_timestamp(data):
    hora_str = data["hora"]
    ts = datetime.strptime(hora_str, "%H:%M:%S")
    return datetime.combine(datetime.today(), ts.time())


def insert_normalized_readings(engine, table, data):
    ts_utc = extract_timestamp(data)

    with engine.begin() as conn:
        for sensor in data["sensores"]:
            stmt = insert(table).values(
                ts_utc=ts_utc,
                valor_limpio=sensor["valor"],
                unidades_convertidas=sensor["unidad"],
                id_sensor=sensor["id"]
            )
            conn.execute(stmt)

    print("Data inserted into 'normalized_readings'")


def listen_and_store(json_data):
    engine = get_db_engine()
    tables = load_tables(engine)
    normalized_readings = tables["normalized_readings"]

    insert_normalized_readings(engine, normalized_readings, json_data)

