from flask import Flask
app = Flask(__name__)

# Members API Route 


#Ruta para probar la conexion de flask con react
@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3" ]}

#Para correr la app 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True) 
    
    #ponemos el debug porq estamos en development

