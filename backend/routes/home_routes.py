from flask import Blueprint, jsonify, request
from utils.token import login_required
from models.usuario import Usuario
from models.mascota import Mascota
from models.PlanAlimenticio import PlanAlimenticio
from models.Horarios import Horario

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/home", methods=["GET"])
@login_required
def home_info():
    usuario = Usuario.query.get(request.user_id)
    mascota = Mascota.query.filter_by(id_cuenta=usuario.id_cuenta).first()

    if not mascota:
        return jsonify({
            "nombre_usuario": usuario.nombre,
            "tiene_mascota": False
        })

    # Obtener su plan
    plan = PlanAlimenticio.query.filter_by(id_mascota=mascota.id_mascota).first()
    horarios = Horario.query.filter_by(id_plan=plan.id_plan).order_by(Horario.hora).all()

    # Tomar siguiente horario
    proxima = horarios[0].hora.isoformat() if horarios else None

    return jsonify({
        "nombre_usuario": usuario.nombre,
        "tiene_mascota": True,
        "mascota_nombre": mascota.nombre,
        "proxima_comida": proxima
    })
