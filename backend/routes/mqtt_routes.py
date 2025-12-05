from flask import Blueprint, request, jsonify
from utils.token import login_required
from services.event_service import detect_and_get_events
from utils.event_saver import save_detected_events

mqtt_bp = Blueprint("mqtt_bp", __name__)

@mqtt_bp.route("/mqtt-data", methods=["POST"])
@login_required
def procesar_mqtt():
    data = request.get_json()

    # 1. Detectar eventos según tu script
    eventos = detect_and_get_events(data, request.user_id)

    # 2. Guardarlos en MariaDB
    save_detected_events(eventos, request.user_id)

    return jsonify({
        "msg": "Datos procesados",
        "eventos": eventos
    }), 200
