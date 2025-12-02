import jwt
import datetime
from flask import request, jsonify, current_app
from functools import wraps

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

    # Asegurar STRING
    return token.decode() if isinstance(token, bytes) else token


def decode_token(token):
    try:
        return jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            resp = jsonify({"error": "Token requerido"})
            resp.headers.add("Access-Control-Allow-Origin", "*")
            return resp, 401

        try:
            token = auth_header.split(" ")[1]
        except:
            resp = jsonify({"error": "Formato de token inválido"})
            resp.headers.add("Access-Control-Allow-Origin", "*")
            return resp, 401

        payload = decode_token(token)

        if not payload:
            resp = jsonify({"error": "Token inválido o expirado"})
            resp.headers.add("Access-Control-Allow-Origin", "*")
            return resp, 401

        request.user_id = payload["user_id"]

        return f(*args, **kwargs)

    return decorated
