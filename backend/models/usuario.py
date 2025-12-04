from extensions.db import db
#add to make the login

class Usuario(db.Model):
    __tablename__ = "cuenta"

    id_cuenta = db.Column(db.Integer, primary_key=True)

    correo = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100))

    # relación con mascota
    mascotas = db.relationship("Mascota", backref="cuenta", lazy=True)
