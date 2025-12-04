from extensions.db import db
from sqlalchemy import DateTime
from datetime import datetime

class PlanAlimenticio(db.Model):
    __tablename__ = "plan_alimenticio"

    id_plan = db.Column(db.Integer, primary_key=True)

    objetivo = db.Column(db.String(100))
    fecha_creacion = db.Column(DateTime, default=datetime.utcnow)

    id_mascota = db.Column(db.Integer, db.ForeignKey("mascota.id_mascota"), nullable=False)

    horarios = db.relationship("Horario", backref="plan", lazy=True)
