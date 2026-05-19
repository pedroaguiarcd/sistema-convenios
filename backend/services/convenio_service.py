from backend.models.convenio import Convenio


def listar_convenios(status=None):
    convenios = (
        Convenio.query
        .order_by(Convenio.data_fim.asc())
        .all()
    )

    if status and status != "todos":
        convenios = [
            convenio
            for convenio in convenios
            if convenio.status_real == status
        ]

    return convenios