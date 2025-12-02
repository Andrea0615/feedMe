from flask import Blueprint, request, jsonify
from extensions.db import db
from models.usuario import Usuario
from utils.security import hash_password, verify_password
from utils.token import generate_token

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def registrar():
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


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(correo=data["correo"]).first()

    if not usuario or not verify_password(data["contrasena"], usuario.contrasena):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = generate_token(usuario.id_usuario)

    return jsonify({
        "msg": "Login exitoso",
        "token": token
    }), 200