from flask import Flask
from extensions.db import db
from config import Config
from flask_cors import CORS
# Importar blueprints
from routes.auth_routes import auth_bp
from routes.pet_routes import mascotas_bp
from routes.home_routes import home_bp
from routes.user_routes import user_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

 

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(mascotas_bp, url_prefix="/api/mascota")
    app.register_blueprint(home_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api/user")


    return app

if __name__ == "__main__": #esto lo añadi para probarlo con sqlite, no se si si vaya con maria db
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)

