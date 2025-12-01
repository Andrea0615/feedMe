from extensions.db import db

class Mascota(db.Model):
    __tablename__ = "mascota"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer)
    raza = db.Column(db.String(50))
    peso_kg = db.Column(db.Float)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    def __repr__(self):
        return f"<Mascota {self.nombre}>"
