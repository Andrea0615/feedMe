from flask import Blueprint, request, jsonify
from extensions.db import db
from models.mascota import Mascota
from models.PlanAlimenticio import PlanAlimenticio
from models.Horarios import Horario
from utils.token import login_required
import datetime 

mascotas_bp = Blueprint("mascotas_bp", __name__)

@mascotas_bp.route("/registro", methods=["POST"])
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
