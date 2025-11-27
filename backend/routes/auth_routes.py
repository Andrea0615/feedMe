from flask import Blueprint, request, jsonify
from extensions.db import db
from models.usuario import Usuario
from utils.security import hash_password, verify_password

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    hashed = hash_password(data["contrasena"])

    nuevo = Usuario(
        nombre=data["nombre"],
        correo=data["correo"],
        contrasena=hashed
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"msg": "Usuario creado"}), 201
