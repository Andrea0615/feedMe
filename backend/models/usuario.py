from extensions.db import db

class Usuario(db.Model):
    __tablename__ = "usuario"   

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.correo}>"
