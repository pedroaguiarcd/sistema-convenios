from flask import Blueprint, jsonify
from backend.models.convenio import Convenio
from backend.utils.helpers import require_perfil

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.get("/resumo")
@require_perfil("gestor", "admin")
def resumo():
    todos = Convenio.query.filter_by(deletado=False).all()

    ativos = sum(1 for c in todos if c.status_real == "ativo")
    pendentes = sum(1 for c in todos if c.status_real == "pendente")
    vencidos = sum(1 for c in todos if c.status_real == "vencido")
    cancelados = sum(1 for c in todos if c.status_real == "cancelado")
    proximos_30d = sum(
        1 for c in todos
        if c.status_real == "ativo"
        and c.dias_para_vencer is not None
        and 0 <= c.dias_para_vencer <= 30
    )

    return jsonify({
        "total": len(todos),
        "ativos": ativos,
        "pendentes": pendentes,
        "vencidos": vencidos,
        "cancelados": cancelados,
        "proximos_vencimento_30d": proximos_30d,
    })
