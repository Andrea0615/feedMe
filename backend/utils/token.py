import jwt
import datetime
from flask import request, jsonify,current_app
from functools import wraps

#esto es basicamente pare que una vez que haga login, se recuerde mi sesión

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return token

def decode_token(token):
    try:
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        try:
            token = auth_header.split(" ")[1]
        except:
            return jsonify({"error": "Formato de token inválido"}), 401

        payload = decode_token(token)

        if not payload:
            return jsonify({"error": "Token inválido o expirado"}), 401

        # Guardamos el ID DE USUARIO dentro del request
        request.user_id = payload["user_id"]

        return f(*args, **kwargs)

    return decorated