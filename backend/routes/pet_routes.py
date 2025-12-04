from flask import Blueprint, request, jsonify
from extensions.db import db
from models.mascota import Mascota
from models.PlanAlimenticio import PlanAlimenticio
from models.Horarios import Horario
from utils.token import login_required
from utils.mqtt_sender import publish_schedule_to_device   # ← MQTT
import datetime 

mascotas_bp = Blueprint("mascotas_bp", __name__)

# ---------------------------------------------------------
#  REGISTRAR MASCOTA + PLAN + HORARIOS + MQTT
# ---------------------------------------------------------
@mascotas_bp.route("/register", methods=["POST"])
@login_required
def registrar_mascota():
    data = request.get_json()

    # ----- Crear mascota -----
    m = data["mascota"]
    mascota = Mascota(
        nombre=m["nombre"],
        edad=m.get("edad"),
        peso_kg=m.get("peso"),
        usuario_id=request.user_id
    )
    db.session.add(mascota)
    db.session.flush()

    # ----- Crear plan alimenticio -----
    a = data["alimentacion"]
    plan = PlanAlimenticio(
        objetivo="Plan generado automáticamente",
        mascota_id=mascota.id
    )
    db.session.add(plan)
    db.session.flush()

    # ----- Crear horarios -----
    horarios_payload = []  # ← lista para MQTT

    for h in a["horarios"]:
        hora_str = h["hora"]
        hora_obj = datetime.datetime.strptime(hora_str, "%H:%M:%S").time()

        horario = Horario(
            hora=hora_obj,
            porcion=h["porcion"],
            plan_id=plan.id
        )

        db.session.add(horario)

        horarios_payload.append({
            "hora": hora_str,
            "porcion": h["porcion"]
        })

    db.session.commit()

    # ----- Enviar horarios al ESP32 -----
    publish_schedule_to_device(horarios_payload)

    return jsonify({
        "msg": "Mascota registrada correctamente",
        "mascota_id": mascota.id
    }), 201


# ---------------------------------------------------------
#  OBTENER INFORMACIÓN DE LA MASCOTA
# ---------------------------------------------------------
@mascotas_bp.route("/info", methods=["GET"])
@login_required
def obtener_mascota():
    mascota = Mascota.query.filter_by(usuario_id=request.user_id).first()

    if not mascota:
        return jsonify({"error": "No hay mascota registrada"}), 404

    plan = PlanAlimenticio.query.filter_by(mascota_id=mascota.id).first()

    if not plan:
        return jsonify({"error": "No hay plan alimenticio registrado"}), 404

    horarios = Horario.query.filter_by(plan_id=plan.id).order_by(Horario.hora).all()

    horarios_data = [
        {
            "hora": h.hora.strftime("%H:%M:%S"),
            "porcion": h.porcion
        }
        for h in horarios
    ]

    return jsonify({
        "mascota": {
            "id": mascota.id,
            "nombre": mascota.nombre,
            "edad": mascota.edad,
            "peso_kg": mascota.peso_kg
        },
        "horarios": horarios_data
    }), 200


# ---------------------------------------------------------
#  EDITAR DATOS DE LA MASCOTA
# ---------------------------------------------------------
@mascotas_bp.route("/edit", methods=["PUT"])
@login_required
def editar_mascota():
    data = request.get_json()

    mascota = Mascota.query.filter_by(usuario_id=request.user_id).first()

    if not mascota:
        return jsonify({"error": "No hay mascota registrada"}), 404

    if "nombre" in data:
        mascota.nombre = data["nombre"]

    if "edad" in data:
        mascota.edad = data["edad"]

    if "peso_kg" in data:
        mascota.peso_kg = data["peso_kg"]

    db.session.commit()

    return jsonify({"msg": "Mascota actualizada correctamente"}), 200


# ---------------------------------------------------------
#  EDITAR HORARIOS + MQTT
# ---------------------------------------------------------
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

    plan = PlanAlimenticio.query.filter_by(mascota_id=mascota.id).first()
    if not plan:
        return jsonify({"error": "Plan alimenticio no encontrado"}), 404

    # ----- Borrar horarios pasados -----
    Horario.query.filter_by(plan_id=plan.id).delete()

    horarios_payload = []  # ← para MQTT

    # ----- Guardar nuevos -----
    for h in horarios_nuevos:
        hora_obj = datetime.datetime.strptime(h["hora"], "%H:%M:%S").time()
        porcion = float(h["porcion"])

        nuevo_horario = Horario(
            hora=hora_obj,
            porcion=porcion,
            plan_id=plan.id
        )

        db.session.add(nuevo_horario)

        horarios_payload.append({
            "hora": h["hora"],
            "porcion": porcion
        })

    db.session.commit()

    # ----- Enviar actualización por MQTT -----
    publish_schedule_to_device(horarios_payload)

    return jsonify({"msg": "Horarios actualizados correctamente"}), 200
