import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import mysql.connector
from datetime import datetime 
import json
import sys

# ------------------- MariaDB / MySQL Connection -------------------
#NOTA IMPORTANTE: LA BASE DE DATOS "mqttesting" es una database para PRUEBAS
#para el código final usaremos "appDB"
def connectToMariaDB():
	try:
		conn = mysql.connector.connect(
			user="ras4",
			password="ras4",
			host="localhost",
			database="mqttesting"
		)
		cursor = conn.cursor()
	except mysql.connector.Error as e:
		print(f"Error connecting to MariaDB: {e}")
		sys.exit(1)
		
	return conn, cursor

#Insert account data in the table 
def insertAccountData(acc_email, acc_password, acc_name, acc_country):
	conn, cursor = connectToMariaDB()
	cursor.execute("""
		INSERT INTO cuenta (correo, password, nombre, pais)
		VALUES (%s, %s, %s, %s)
	""", (acc_email, acc_password, acc_name, acc_country))
		
		
	conn.commit()
	print("Datos insertados en la tabla 'cuenta'")

	conn.close()

def insertPetData(name, age, breed, weight, acc_id):
	conn, cursor = connectToMariaDB()
	cursor.execute("""
		INSERT INTO mascota (nombre, edad, raza, peso_kg, id_cuenta)
		VALUES (%s, %s, %s, %s)
	""", (name, age, breed, weight, acc_id))
		
		
	conn.commit()
	print("Datos insertados en la tabla 'mascota'")

	conn.close()
	
def insertFeedingPlan(objective, pet_id, schedule_portion):
	conn, cursor = connectToMariaDB()
	#insertar plan alimenticio en la tabla
	cursor.execute("""
		INSERT INTO plan_alimenticio (objetivo, id_mascota)
		VALUES (%s, %s)
	""", (objective, pet_id))
	#agregar el sacar el id del plan creado para meterlo en la tabla de horarios
	plan_id = cursor.lastrowid
	
	data = [(hora, porcion, plan_id) for hora, porcion in schedule_portion]
	
	#se cancela el for, encontre como hacerlo con un solo .execute()
	cursor.executemany("""
		INSERT INTO horarios (hora, porcion, id_plan)
		VALUES (%s, %s, %s)
	""", data))
		
	conn.commit()
	print("Datos insertados en las tabla 'plan_alimenticio' y 'horarios'")
	conn.close()

#datos prueba, los reemplazan por un codigo de donde saquen los datos
acc_email = 'usauario1@gmail.com'
acc_password = "hola5678"
acc_name = "Usuario1"
acc_country = "Canada"
insertAccountData(acc_email, acc_password, acc_name, acc_country)



# ------------------- Close MariaDB connection -------------------

#conn.close()
