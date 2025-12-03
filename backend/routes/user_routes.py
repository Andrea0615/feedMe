from flask import Blueprint, jsonify, request
from extensions.db import db
from models.usuario import Usuario
from utils.token import login_required
from utils.security import hash_password

user_bp = Blueprint("user_bp", __name__)

# --- GET /api/user/info ---
@user_bp.route("/info", methods=["GET"])
@login_required
def get_info():
    usuario = Usuario.query.get(request.user_id)

    return jsonify({
        "id": usuario.id_usuario,
        "nombre": usuario.nombre,
        "correo": usuario.correo
    }), 200


# --- PUT /api/user/update ---
@user_bp.route("/edit", methods=["PUT"])
@login_required
def update_info():
    data = request.get_json()
    usuario = Usuario.query.get(request.user_id)

    if "nombre" in data:
        usuario.nombre = data["nombre"]

    if "correo" in data:
        usuario.correo = data["correo"]

    if "contrasena" in data and data["contrasena"].strip() != "":
        usuario.contrasena = hash_password(data["contrasena"])

    db.session.commit()

    return jsonify({"msg": "Perfil actualizado"}), 200
