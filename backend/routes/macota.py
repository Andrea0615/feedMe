from flask import Blueprint, request, jsonify
from extensions.db import db
from models.mascota import Mascota
from models.PlanAlimenticio import PlanAlimenticio
from models.Horarios import Horario
from utils.token import login_required

mascotas_bp = Blueprint("mascotas_bp", __name__)

@mascotas_bp.route("/mascotas/registro", methods=["POST"])
@login_required
def registrar_mascota():
    data = request.get_json()

    #Crear mascota
    m = data["mascota"]

    mascota = Mascota(
        nombre=m["nombre"],
        edad=m.get("edad"),
        peso_kg=m.get("peso"),
        especie=m.get("especie"),
        usuario_id=request.user_id
    )

    db.session.add(mascota)
    db.session.flush()  # obtener mascota.id

    #Crear plan alimenticio
    a = data["alimentacion"]

    plan = PlanAlimenticio(
        comidas_por_dia=a["comidas_por_dia"],
        mascota_id=mascota.id
    )

    db.session.add(plan)
    db.session.flush()

    #Crear horarios
    for h in a["horarios"]:
        horario = Horario(
            hora=h["hora"],
            porcion=h["porcion"],
            plan_id=plan.id
        )
        db.session.add(horario)

    #Guardar todo junto
    db.session.commit()

    return jsonify({
        "msg": "Mascota y plan alimenticio registrados correctamente",
        "mascota_id": mascota.id
    }), 201

