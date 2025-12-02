from extensions.db import db

class Mascota(db.Model):
    __tablename__ = "mascota"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer)
    peso_kg = db.Column(db.Float)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)

    def __repr__(self):
        return f"<Mascota {self.nombre}>"
