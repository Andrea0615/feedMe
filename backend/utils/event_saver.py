from models.evento import Evento
from extensions.db import db
from datetime import datetime

def save_detected_events(events, user_id):
    for tipo, prioridad, timestamp in events:
        if not tipo or prioridad <= 0:
            continue

        fecha = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

        nuevo = Evento(
            tipo_evento=tipo,
            prioridad=prioridad,
            fecha=fecha,
            id_cuenta=user_id
        )

        db.session.add(nuevo)

    db.session.commit()
