
from flask import Blueprint, jsonify
from backend.models.notifications import Notification
from backend.services.vencimento_service import verificar_vencimentos
from backend.database import db

notificacoes_bp = Blueprint("notificacoes", __name__, url_prefix="/notificacoes")


@notificacoes_bp.get("/")
def listar_notificacoes():
    notificacoes = Notification.query.order_by(
        Notification.criado_em.desc()
    ).all()

    return jsonify([
        {
            "id": n.id,
            "convenio_id": n.convenio_id,
            "titulo": n.titulo,
            "mensagem": n.mensagem,
            "tipo": n.tipo,
            "lida": n.lida,
            "criado_em": n.criada_em.isoformat() if n.criada_em else None
        }
        for n in notificacoes
    ])


@notificacoes_bp.post("/verificar-vencimentos")
def executar_verificacao():
    resultado = verificar_vencimentos()
    return jsonify(resultado)


@notificacoes_bp.patch("/<int:notificacao_id>/lida")
def marcar_como_lida(notificacao_id):
    notificacao = Notification.query.get_or_404(notificacao_id)
    notificacao.lida = True

    db.session.commit()

    return jsonify({"mensagem": "Notificação marcada como lida"})