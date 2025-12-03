from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

def getPlanAData(user_id):
    engine = create_engine("mariadb+pymysql://ras4:ras4@localhost/mqttesting")
    metadata = MetaData()
    metadata.reflect(bind=engine)

    SessionLocal = sessionmaker(bind=engine)
    mdb = SessionLocal()

    user = metadata.tables["cuenta"]
    feeding_plan = metadata.tables["plan_alimenticio"]
    pet = metadata.tables["mascota"]
    schedule = metadata.tables["horarios"]

    #accessing the user's pet feeding schedule, only the hour and portion established
    statement = (
    select(schedule.c.hora, schedule.c.porcion)
    .select_from(
        user
        .join(pet, user.c.id_cuenta == pet.c.id_cuenta)
        .join(feeding_plan, pet.c.id_mascota == feeding_plan.c.id_mascota)
        .join(schedule, feeding_plan.c.id_plan == schedule.c.id_plan)
        )   
        .where(user.c.id_cuenta == user_id)
    )

    result = mdb.execute(statement).fetchall()
    horarios = [{"hora": r.hora.strftime("%H:%M:%S"), "porcion": r.porcion} for r in result]

    return horarios

def getNowTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getClosestSchedule(schedule, actual_hour_str):
    actual_time = datetime.strptime(actual_hour_str, "%H:%M:%S").time()
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

def isWithinTolerance(actual_hour_str, scheduled_hour_str, minutes):
    actual = datetime.strptime(actual_hour_str, "%H:%M:%S").time()
    sched = datetime.strptime(scheduled_hour_str, "%H:%M:%S").time()

    actual_dt = datetime.combine(datetime.today(), actual)
    sched_dt = datetime.combine(datetime.today(), sched)

    diff_min = abs((actual_dt - sched_dt).total_seconds() / 60)
    return diff_min <= minutes


def getEventType(sensor_id, value, scheduled, actual_hour):
    eventTypes = ["Se sirvió la comida", "Tu mascota no ha comido", "Te estás quedando sin comida"]
    eventType = ""
    eventPriority = 0 

    if sensor_id == 2:
        closest = getClosestSchedule(scheduled, actual_hour)
        if closest is None:
            return ["", 0, getNowTime()]

        sched_hour = closest["hora"]
        sched_portion = closest["porcion"]

        # Event when food is served and within the range
        if isWithinTolerance(actual_hour, sched_hour, 2) and abs(value - sched_portion) <= 10:
            eventType = eventTypes[0]
            eventPriority = 3

        # Event when the food is still the same after 5 minutes, means pet didnt eat
        actual_dt = datetime.combine(datetime.today(), datetime.strptime(actual_hour, "%H:%M:%S").time())
        sched_dt = datetime.combine(datetime.today(), datetime.strptime(sched_hour, "%H:%M:%S").time())

        if actual_dt > sched_dt + timedelta(minutes=5) and abs(value - sched_portion) <= 10:
            eventType = eventTypes[1]
            eventPriority = 2   

    #To check if its missing food
    if sensor_id == 1 and value <= 5:
        eventType = eventTypes[2]
        eventPriority = 3

    return [eventType, eventPriority, getNowTime()] #return array with the event data

def eventDetection(data, user_id):
    event_reg = [] 

    scheduled = getPlanAData(user_id)
    str_hour = data["hora"]
    # ts_utc = datetime.strptime(hora_str, "%H:%M:%S")
    # ts_utc = datetime.combine(datetime.today(), ts_utc.time())
    for sensor in data["sensores"]:
        sensor_id = sensor["id"]
        value = sensor["valor"]
        #unidad = sensor["unidad"]
        temp = getEventType(sensor_id=sensor_id, value=value, scheduled=scheduled, actual_hour=str_hour)
        event_reg.append(temp)

    return event_reg

def detect_and_get_events(json_data, user_id):
    return eventDetection(json_data, user_id)

# if __name__ == "__main__":
#     print(getPlanAData(1))
#     #este se saca directo de la esp32
#     json_data_sample=  {  
#         "hora": "12:00:00",        
#         "horario": "12:00:00",     
#         "sensores": [
#         {"id":1,"valor":10,"unidad":"cm"},
#         {"id":2,"valor":150,"unidad":"g"}
#         ]
#     }
#     eventDetection(json_data_sample)

