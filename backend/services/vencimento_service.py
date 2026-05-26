from datetime import date

from backend.database import db
from backend.models.convenio import Convenio
from backend.models.notifications import Notification
from backend.services.notificacao_service import criarNotificacaoVencimento


def verificar_vencimentos():
    hoje = date.today()

    convenios = Convenio.query.filter_by(
        deletado=False
    ).all()

    resultado = {
        "vigentes": 0,
        "proximos": 0,
        "vencidos": 0
    }

    for convenio in convenios:
        dias_restantes = (convenio.data_fim - hoje).days

        if convenio.status in ["pendente", "cancelado"]:
            continue

        if dias_restantes < 0:
            resultado["vencidos"] += 1

            Notification.query.filter_by(
                convenio_id=convenio.id,
                tipo="vencimento",
                lida=False
            ).delete()

        elif 1 <= dias_restantes <= 30:
            resultado["proximos"] += 1
            criarNotificacaoVencimento(convenio, dias_restantes)

        else:
            resultado["vigentes"] += 1

            Notification.query.filter_by(
                convenio_id=convenio.id,
                tipo="vencimento",
                lida=False
            ).delete()

    db.session.commit()

    return resultado