from extensions.db import db

class Horario(db.Model):
    __tablename__ = "horarios"

    id = db.Column(db.Integer, primary_key=True)
    hora = db.Column(db.Time, nullable=False)
    porcion = db.Column(db.Float, nullable=False)

    plan_id = db.Column(db.Integer, db.ForeignKey("plan_alimenticio.id"), nullable=False)
