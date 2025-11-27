from flask import Flask
from extensions.db import db
from extensions.cors import cors
from extensions.jwt import jwt

# Importar blueprints
from routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)

    # REGISTRAR RUTAS
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
