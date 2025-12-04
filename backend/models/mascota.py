from extensions.db import db

class Mascota(db.Model):
    __tablename__ = "mascota"

    id_mascota = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    raza = db.Column(db.String(100))
    peso_kg = db.Column(db.Numeric(5, 2), nullable=False)

    id_cuenta = db.Column(db.Integer, db.ForeignKey("cuenta.id_cuenta"), nullable=False)

    # relación con plan alimenticio
    planes = db.relationship("PlanAlimenticio", backref="mascota", lazy=True)
