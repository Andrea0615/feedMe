from models.evento import Evento
from extensions.db import db

def save_event(tipo, prioridad, fecha, user_id):
    nuevo = Evento(
        tipo_evento=tipo,
        prioridad=prioridad,
        fecha=fecha,
        id_cuenta=user_id
    )

    db.session.add(nuevo)
    db.session.commit()

    print("Evento guardado:", tipo, prioridad, fecha)
