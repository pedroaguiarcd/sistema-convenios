from backend.database import db
from backend.models.notifications import Notification

def criarNotificacaoVencimento(convenio, diasRestantes):

    notificacaoExistente = Notification.query.filter_by(
        convenio_id=convenio.id,
        tipo="vencimento",
        lida=False
    ).first()

    if notificacaoExistente:

        return notificacaoExistente


    notificacao = Notification(
        convenio_id=convenio.id,
        titulo="Convênio próximo do vencimento",
        mensagem=f"O convênio '{convenio.id}' está com vencimento em {diasRestantes} dias.",
        tipo="vencimento"
    )

    db.session.add(notificacao)

    return notificacao