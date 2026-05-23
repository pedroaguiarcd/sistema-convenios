from datetime import date
from backend.database import db
from backend.models.convenio import Convenio
from backend.services.notificacao_service import criarNotificacaoVencimento


def verificar_vencimentos():
    hoje = date.today()
    convenios = Convenio.query.all()

    resultado = {
        "vigentes": 0,
        "proximos": 0,
        "vencidos": 0
    }

    for convenio in convenios:
        dias_restantes = (convenio.data_fim - hoje).days

        if dias_restantes < 0:
            convenio.status = "VENCIDO"
            resultado["vencidos"] += 1

        elif dias_restantes <= 30:
            convenio.status = "PROXIMO_VENCIMENTO"
            resultado["proximos"] += 1
            criarNotificacaoVencimento(convenio, dias_restantes)

        else:
            convenio.status = "VIGENTE"
            resultado["vigentes"] += 1

    db.session.commit()
    return resultado