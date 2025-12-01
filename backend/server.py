from flask import Flask
from extensions.db import db
from extensions.cors import cors
from config import Config
# Importar blueprints
from routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cors.init_app(app)
 

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
