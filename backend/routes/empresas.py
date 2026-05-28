from flask import Blueprint, request, jsonify
from backend.models.empresa import Empresa
from backend.database import db
from backend.utils.helpers import require_auth, require_perfil, get_current_user

empresas_bp = Blueprint("empresas", __name__, url_prefix="/empresas")


def _empresa_to_dict(e):
    return {
        "id": e.id,
        "nome": e.nome,
        "cnpj": e.cnpj,
        "email": e.email,
        "telefone": e.telefone,
        "endereco": e.endereco,
    }


@empresas_bp.get("/")
@require_perfil("gestor", "admin")
def listar():
    empresas = Empresa.query.order_by(Empresa.nome).all()
    return jsonify([_empresa_to_dict(e) for e in empresas])


@empresas_bp.get("/<int:empresa_id>")
@require_auth
def obter(empresa_id):
    user_id, perfil = get_current_user()
    empresa = Empresa.query.get_or_404(empresa_id)

    # empresa-role users can only see their own empresa
    if perfil == "empresa":
        from backend.models.usuario import Usuario
        usuario = Usuario.query.get(user_id)
        if not usuario or usuario.empresa_id != empresa_id:
            return jsonify({"erro": "Acesso negado"}), 403

    return jsonify(_empresa_to_dict(empresa))


@empresas_bp.patch("/<int:empresa_id>")
@require_auth
def atualizar(empresa_id):
    user_id, perfil = get_current_user()
    empresa = Empresa.query.get_or_404(empresa_id)

    if perfil == "empresa":
        from backend.models.usuario import Usuario
        usuario = Usuario.query.get(user_id)
        if not usuario or usuario.empresa_id != empresa_id:
            return jsonify({"erro": "Acesso negado"}), 403

    data = request.get_json()
    campos = ("nome", "cnpj", "email", "telefone", "endereco")
    for campo in campos:
        if campo in data:
            setattr(empresa, campo, data[campo])

    db.session.commit()
    return jsonify(_empresa_to_dict(empresa))
