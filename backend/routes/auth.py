from flask import Blueprint, request, jsonify
from backend.services.auth_service import autenticar_usuario, cadastrar_usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/login")
def login():
    data = request.get_json()
    email = data.get("email", "").strip()
    senha = data.get("senha", "")

    if not email or not senha:
        return jsonify({"erro": "E-mail e senha são obrigatórios"}), 400

    usuario = autenticar_usuario(email, senha)

    if not usuario:
        return jsonify({"erro": "E-mail ou senha inválidos"}), 401

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil,
        "empresa_id": usuario.empresa_id,
    })


@auth_bp.post("/cadastro")
def cadastro():
    data = request.get_json()
    nome = data.get("nome", "").strip()
    email = data.get("email", "").strip()
    senha = data.get("senha", "")
    perfil = data.get("perfil", "")

    if not nome or not email or not senha:
        return jsonify({"erro": "Nome, e-mail e senha são obrigatórios"}), 400

    if perfil not in ("empresa", "gestor", "admin"):
        return jsonify({"erro": "Perfil inválido"}), 400

    usuario = cadastrar_usuario(nome, email, senha, perfil)

    if not usuario:
        return jsonify({"erro": "E-mail já cadastrado"}), 409

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil,
    }), 201
