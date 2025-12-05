from extensions.db import db
from datetime import datetime

class Evento(db.Model):
    __tablename__ = "eventos"

    id_evento = db.Column(db.Integer, primary_key=True)
    tipo_evento = db.Column(db.String(50), nullable=False)
    prioridad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    id_cuenta = db.Column(db.Integer, db.ForeignKey("cuenta.id_cuenta"), nullable=False)
