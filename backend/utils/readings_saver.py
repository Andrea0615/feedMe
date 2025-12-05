import json
from datetime import datetime
from sqlalchemy import create_engine, MetaData, insert
from sqlalchemy.exc import SQLAlchemyError

# ❗❗ Aquí va la base de datos de sensores
DB_URL = "mariadb+pymysql://ras4:ras4@localhost/sensoresDB"


def get_db_engine():
    try:
        engine = create_engine(DB_URL)
        return engine
    except SQLAlchemyError as e:
        print(f"SQLAlchemy connection error: {e}")
        return None


def load_tables(engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return {
        "normalized_readings": metadata.tables["normalized_readings"]
    }


def extract_timestamp(data):
    hora_str = data["hora"]  # “14:07:00”
    ts = datetime.strptime(hora_str, "%H:%M:%S")
    return datetime.combine(datetime.today(), ts.time())


def insert_normalized_readings(engine, table, data):
    ts_utc = extract_timestamp(data)

    with engine.begin() as conn:
        for sensor in data["sensores"]:
            raw_value = sensor.get("valor")

            # 🔍 Validar el valor del sensor
            try:
                if raw_value is None:
                    clean_value = -1
                else:
                    clean_value = float(raw_value)
            except:
                clean_value = -1

            # Insertar
            stmt = insert(table).values(
                ts_utc=ts_utc,
                valor_limpio=clean_value,
                unidades_convertidas=sensor.get("unidad", ""),
                id_sensor=sensor.get("id", -1)
            )

            conn.execute(stmt)

    print("✔ Lecturas guardadas en sensoresDB.normalized_readings")



def save_raw_data(json_data):
    engine = get_db_engine()
    if not engine:
        return

    tables = load_tables(engine)
    normalized_readings = tables["normalized_readings"]

    insert_normalized_readings(engine, normalized_readings, json_data)
