from datetime import datetime, timedelta

def getPlanAData(user_id):
    from sqlalchemy import create_engine, MetaData
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("mariadb+pymysql://ras4:ras4@localhost/appDB")
    metadata = MetaData()
    metadata.reflect(bind=engine)
    mdb = sessionmaker(bind=engine)()

    schedule = metadata.tables["horarios"]
    pet = metadata.tables["mascota"]
    plan = metadata.tables["plan_alimenticio"]
    user = metadata.tables["cuenta"]

    query = (
        schedule.select()
        .select_from(
            user.join(pet, user.c.id_cuenta == pet.c.id_cuenta)
                .join(plan, pet.c.id_mascota == plan.c.id_mascota)
                .join(schedule, plan.c.id_plan == schedule.c.id_plan)
        )
        .where(user.c.id_cuenta == user_id)
    )

    result = mdb.execute(query).fetchall()

    horarios = [
        {"hora": r.hora.strftime("%H:%M:%S"), "porcion": r.porcion}
        for r in result
    ]

    return horarios


def isWithinTolerance(actual, scheduled, minutes):
    a = datetime.strptime(actual, "%H:%M:%S").time()
    s = datetime.strptime(scheduled, "%H:%M:%S").time()

    ad = datetime.combine(datetime.today(), a)
    sd = datetime.combine(datetime.today(), s)

    return abs((ad - sd).total_seconds()) / 60 <= minutes


def getClosestSchedule(schedule, actual):
    actual_time = datetime.strptime(actual, "%H:%M:%S").time()
    actual_dt = datetime.combine(datetime.today(), actual_time)

    closest = None
    min_diff = float("inf")

    for h in schedule:
        sched_time = datetime.strptime(h["hora"], "%H:%M:%S").time()
        sched_dt = datetime.combine(datetime.today(), sched_time)

        diff = abs((sched_dt - actual_dt).total_seconds())
        if diff < min_diff:
            min_diff = diff
            closest = h

    return closest


def detect_and_get_events(json_data, user_id):
    schedule = getPlanAData(user_id)
    hour = json_data["hora"]
    events = []

    for sensor in json_data["sensores"]:
        sid = sensor["id"]
        val = sensor["valor"]

        # EVENTO: SIN COMIDA
        if sid == 1 and val <= 5:
            events.append(["Te estás quedando sin comida", 1, datetime.now()])
            continue

        # EVENTO: COMIDA SERVIDA / NO COMIÓ
        if sid == 2:
            closest = getClosestSchedule(schedule, hour)
            if closest is None:
                continue

            sched_time = closest["hora"]
            sched_portion = closest["porcion"]

            # COMIDA SERVIDA
            if isWithinTolerance(hour, sched_time, 2) and abs(val - sched_portion) <= 10:
                events.append(["Se sirvió la comida", 3, datetime.now()])
                continue

            # NO HA COMIDO
            h_now = datetime.strptime(hour, "%H:%M:%S")
            h_sched = datetime.strptime(sched_time, "%H:%M:%S")

            if h_now > (h_sched + timedelta(minutes=5)) and abs(val - sched_portion) <= 10:
                events.append(["Tu mascota no ha comido", 2, datetime.now()])

    return events
