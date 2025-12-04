from extensions.db import db
from sqlalchemy import Time

class Horario(db.Model):
    __tablename__ = "horarios"

    id_horario = db.Column(db.Integer, primary_key=True)

    hora = db.Column(Time, nullable=False)
    porcion = db.Column(db.Integer, nullable=False)

    id_plan = db.Column(db.Integer, db.ForeignKey("plan_alimenticio.id_plan"), nullable=False)
