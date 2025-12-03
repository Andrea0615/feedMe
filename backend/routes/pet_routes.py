from flask import Blueprint, request, jsonify
from extensions.db import db
from models.mascota import Mascota
from models.PlanAlimenticio import PlanAlimenticio
from models.Horarios import Horario
from utils.token import login_required
import datetime 

mascotas_bp = Blueprint("mascotas_bp", __name__)

@mascotas_bp.route("/register", methods=["POST"])
@login_required
def registrar_mascota():
    data = request.get_json()

    m = data["mascota"]

    mascota = Mascota(
        nombre=m["nombre"],
        edad=m.get("edad"),
        peso_kg=m.get("peso"),
        usuario_id=request.user_id
    )

    db.session.add(mascota)
    db.session.flush()



    a = data["alimentacion"]

    plan = PlanAlimenticio(
        objetivo="Plan generado automáticamente",
        mascota_id=mascota.id
    )

    db.session.add(plan)
    db.session.flush()

    for h in a["horarios"]:

        # Convert time string → datetime.time
        # "08:30" → hour=8, minute=30
        hora_str = h["hora"]
        hora_obj = datetime.datetime.strptime(hora_str, "%H:%M").time()

        horario = Horario(
            hora=hora_obj,
            porcion=h["porcion"],
            plan_id=plan.id
        )

        db.session.add(horario)

    db.session.commit()

    return jsonify({
        "msg": "Mascota registrada correctamente",
        "mascota_id": mascota.id
    }), 201

@mascotas_bp.route("/info", methods=["GET"])
@login_required
def obtener_mascota():
    # 1. Obtener mascota del usuario loggeado
    mascota = Mascota.query.filter_by(usuario_id=request.user_id).first()

    if not mascota:
        return jsonify({"error": "No hay mascota registrada"}), 404

    # 2. Obtener plan alimenticio
    plan = PlanAlimenticio.query.filter_by(mascota_id=mascota.id).first()

    if not plan:
        return jsonify({"error": "No hay plan alimenticio registrado"}), 404

    # 3. Obtener horarios
    horarios = Horario.query.filter_by(plan_id=plan.id).order_by(Horario.hora).all()

    horarios_data = [
        {
            "hora": h.hora.strftime("%H:%M"),
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

    return jsonify({
        "msg": "Mascota actualizada correctamente"
    }), 200

@mascotas_bp.route("/horarios", methods=["PUT"])
@login_required
def editar_horarios():
    data = request.get_json()

    horarios_nuevos = data.get("horarios")

    if not horarios_nuevos or len(horarios_nuevos) == 0:
        return jsonify({"error": "Debes enviar al menos un horario"}), 400

    #obtener mascota del usuario
    mascota = Mascota.query.filter_by(usuario_id=request.user_id).first()
    if not mascota:
        return jsonify({"error": "Mascota no encontrada"}), 404

    #obtener plan alimenticio
    plan = PlanAlimenticio.query.filter_by(mascota_id=mascota.id).first()
    if not plan:
        return jsonify({"error": "Plan alimenticio no encontrado"}), 404

    #eliminar horarios actuales
    Horario.query.filter_by(plan_id=plan.id).delete()

    #insertar nuevos horarios
    for h in horarios_nuevos:
        try:
            hora_obj = datetime.datetime.strptime(h["hora"], "%H:%M").time()
            porcion = float(h["porcion"])
        except Exception:
            return jsonify({"error": "Formato de horario inválido"}), 400

        nuevo_horario = Horario(
            hora=hora_obj,
            porcion=porcion,
            plan_id=plan.id
        )

        db.session.add(nuevo_horario)

    #guardar cambios
    db.session.commit()

    return jsonify({
        "msg": "Horarios actualizados correctamente"
    }), 200
