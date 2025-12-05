from flask import Blueprint, jsonify, request
from utils.token import login_required
from models.evento import Evento

events_bp = Blueprint("events_bp", __name__)

@events_bp.route("/events/history", methods=["GET"])
@login_required
def history():
    eventos = Evento.query.filter_by(id_cuenta=request.user_id).order_by(Evento.fecha.desc()).all()

    data = [
        {
            "tipo_evento": e.tipo_evento,
            "prioridad": e.prioridad,
            "fecha": e.fecha.strftime("%Y-%m-%d %H:%M:%S")
        }
        for e in eventos
    ]

    return jsonify(data), 200
