from flask import Blueprint, request, jsonify
from extensions.db import db
from models.mascota import Mascota
from models.PlanAlimenticio import PlanAlimenticio
from models.Horarios import Horario
from utils.token import login_required
from utils.mqtt_sender import publish_schedule_to_device
import datetime

mascotas_bp = Blueprint("mascotas_bp", __name__)

# =========================================================
#  UTILIDAD: PARSEAR HORAS CON O SIN SEGUNDOS
# =========================================================
def parse_time_flexible(hora_str):
    """
    Acepta formatos:
    - 'HH:MM'
    - 'HH:MM:SS'
    """
    partes = hora_str.split(":")
    if len(partes) == 3:
        return datetime.datetime.strptime(hora_str, "%H:%M:%S").time()
    return datetime.datetime.strptime(hora_str, "%H:%M").time()


# =========================================================
#  REGISTRAR MASCOTA + PLAN + HORARIOS + MQTT
# =========================================================
@mascotas_bp.route("/register", methods=["POST"])
@login_required
def registrar_mascota():
    data = request.get_json()

    # --- Mascota ---
    m = data["mascota"]
    mascota = Mascota(
        nombre=m["nombre"],
        edad=m.get("edad"),
        peso_kg=m.get("peso"),
        id_cuenta=request.user_id
    )
    db.session.add(mascota)
    db.session.flush()

    # --- Plan ---
    a = data["alimentacion"]
    plan = PlanAlimenticio(
        objetivo="Plan generado automáticamente",
        mascota_id=mascota.id_mascota
    )
    db.session.add(plan)
    db.session.flush()

    # --- Horarios ---
    horarios_payload = []  # Para MQTT

    for h in a["horarios"]:
        hora_obj = parse_time_flexible(h["hora"])

        horario = Horario(
            hora=hora_obj,
            porcion=h["porcion"],
            plan_id=plan.id_plan
        )
        db.session.add(horario)

        # Enviar siempre HH:MM:SS
        horarios_payload.append({
            "hora": hora_obj.strftime("%H:%M:%S"),
            "porcion": h["porcion"]
        })

    db.session.commit()

    # Enviar a ESP32
    publish_schedule_to_device(horarios_payload)

    return jsonify({
        "msg": "Mascota registrada correctamente",
        "mascota_id": mascota.id_mascota
    }), 201


# =========================================================
#  OBTENER INFORMACIÓN DE LA MASCOTA
# =========================================================
@mascotas_bp.route("/info", methods=["GET"])
@login_required
def obtener_mascota():
    mascota = Mascota.query.filter_by(usuario_id=request.user_id).first()

    if not mascota:
        return jsonify({"error": "No hay mascota registrada"}), 404

    plan = PlanAlimenticio.query.filter_by(mascota_id=mascota.id_mascota).first()

    if not plan:
        return jsonify({"error": "No hay plan alimenticio registrado"}), 404

    horarios = Horario.query.filter_by(plan_id=plan.id_plan).order_by(Horario.hora).all()

    horarios_data = [
        {
            "hora": h.hora.strftime("%H:%M:%S"),  # SIEMPRE enviamos segundos
            "porcion": h.porcion
        }
        for h in horarios
    ]

    return jsonify({
        "mascota": {
            "id": mascota.id_mascota,
            "nombre": mascota.nombre,
            "edad": mascota.edad,
            "peso_kg": mascota.peso_kg
        },
        "horarios": horarios_data
    }), 200


# =========================================================
#  EDITAR DATOS DE LA MASCOTA
# =========================================================
@mascotas_bp.route("/edit", methods=["PUT"])
@login_required
def editar_mascota():
    data = request.get_json()

    mascota = Mascota.query.filter_by(usuario_id=request.user_id).first()

    if not mascota:
        return jsonify({"error": "No hay mascota registrada"}), 404

    mascota.nombre = data.get("nombre", mascota.nombre)
    mascota.edad = data.get("edad", mascota.edad)
    mascota.peso_kg = data.get("peso_kg", mascota.peso_kg)

    db.session.commit()

    return jsonify({"msg": "Mascota actualizada correctamente"}), 200


# =========================================================
#  EDITAR HORARIOS + MQTT
# =========================================================
@mascotas_bp.route("/horarios", methods=["PUT"])
@login_required
def editar_horarios():
    data = request.get_json()
    horarios_nuevos = data.get("horarios")

    if not horarios_nuevos:
        return jsonify({"error": "Debes enviar al menos un horario"}), 400

    mascota = Mascota.query.filter_by(usuario_id=request.user_id).first()
    if not mascota:
        return jsonify({"error": "Mascota no encontrada"}), 404

    plan = PlanAlimenticio.query.filter_by(mascota_id=mascota.id_mascota).first()
    if not plan:
        return jsonify({"error": "Plan alimenticio no encontrado"}), 404

    # Borrar horarios actuales
    Horario.query.filter_by(plan_id=plan.id_plan).delete()

    horarios_payload = []  # MQTT

    # Guardar nuevos
    for h in horarios_nuevos:
        hora_obj = parse_time_flexible(h["hora"])
        porcion = float(h["porcion"])

        nuevo_horario = Horario(
            hora=hora_obj,
            porcion=porcion,
            plan_id=plan.id
        )
        db.session.add(nuevo_horario)

        horarios_payload.append({
            "hora": hora_obj.strftime("%H:%M:%S"),
            "porcion": porcion
        })

    db.session.commit()

    # Enviar actualización a ESP32
    publish_schedule_to_device(horarios_payload)

    return jsonify({"msg": "Horarios actualizados correctamente"}), 200
