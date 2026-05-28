from backend.database import db
from backend.models.notifications import Notification

def criarNotificacaoVencimento(convenio, diasRestantes):

    notificacaoExistente = Notification.query.filter_by(
        convenio_id=convenio.id,
        tipo="vencimento",
        lida=False
    ).first()

    nova_mensagem = f"O convênio '{convenio.descricao}' vence em {diasRestantes} dias."

    if notificacaoExistente:

        if notificacaoExistente.mensagem != nova_mensagem:
            notificacaoExistente.mensagem = nova_mensagem
            db.session.commit()

        return notificacaoExistente


    notificacao = Notification(
        convenio_id=convenio.id,
        titulo="Convênio próximo do vencimento",
        mensagem=f"O convênio '{convenio.descricao}' vence em {diasRestantes} dias.",
        tipo="vencimento"
    )

    db.session.add(notificacao)
    db.session.commit()

    return notificacao