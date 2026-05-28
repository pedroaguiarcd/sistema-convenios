"""
Auth helpers for Flask routes.

Strategy: stateless header-based identity.
The Flet frontend sets two headers on every request:
    X-User-Id    : usuario.id   (int as string)
    X-User-Perfil: usuario.perfil  ("gestor" | "empresa" | "admin")

No JWT/session needed — the app runs locally and login already
authenticates against the DB directly in login.py.
"""

from functools import wraps
from flask import request, jsonify, g


def get_current_user():
    """Return (user_id: int, perfil: str) from request headers."""
    user_id = request.headers.get("X-User-Id")
    perfil = request.headers.get("X-User-Perfil", "")
    if user_id:
        try:
            return int(user_id), perfil
        except ValueError:
            pass
    return None, None


def require_auth(f):
    """Decorator: reject requests with no identity headers."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id, perfil = get_current_user()
        if not user_id:
            return jsonify({"erro": "Não autenticado"}), 401
        return f(*args, **kwargs)
    return decorated


def require_perfil(*perfis_permitidos):
    """Decorator factory: reject requests whose perfil is not in the allowed list."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_id, perfil = get_current_user()
            if not user_id:
                return jsonify({"erro": "Não autenticado"}), 401
            if perfil not in perfis_permitidos:
                return jsonify({"erro": "Acesso negado"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator
