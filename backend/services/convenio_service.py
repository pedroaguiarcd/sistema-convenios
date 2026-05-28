from datetime import date, datetime

from backend.services.pdf_service import gerar_termo_convenio

from backend.models.convenio import Convenio
from backend.database import db


def excluir_convenio(
    convenio_id,
    motivo=""
):

    convenio = Convenio.query.get(
        convenio_id
    )

    if not convenio:
        return None

    convenio.deletado = True
    convenio.excluido_em = datetime.now()
    convenio.motivo_exclusao = motivo

    db.session.commit()

    return convenio

def aprovar_convenio(
    convenio_id,
    gestor="Gestor UESPI"
):

    convenio = Convenio.query.get(
        convenio_id
    )

    if not convenio:
        return None

    convenio.status = "ativo"
    convenio.data_inicio = date.today()
    convenio.data_aprovacao = date.today()
    convenio.aprovado_por = gestor

    db.session.commit()

    gerar_termo_convenio(
        convenio
    )

    return convenio


def cancelar_convenio(
    convenio_id,
    motivo=""
):

    convenio = Convenio.query.get(
        convenio_id
    )

    if not convenio:
        return None

    convenio.status = "cancelado"
    convenio.data_cancelamento = date.today()
    convenio.motivo_cancelamento = motivo

    db.session.commit()

    return convenio


def listar_convenios(status=None):

    convenios = Convenio.query.all()

    if status == "ativo":

        convenios = [
            c
            for c in convenios
            if c.status_real == "ativo"
            and not c.deletado
        ]

    elif status == "vencido":

        convenios = [
            c
            for c in convenios
            if c.status_real == "vencido"
        ]
    elif status == "cancelado":

        convenios = [
            c
            for c in convenios
            if c.status_real == "cancelado"
            and not c.deletado
        ]

    elif status == "alterado":

        convenios = [
            c
            for c in convenios
            if c.alterado_em
            and not c.deletado
        ]

    elif status == "historico":

        convenios = [
            c
            for c in convenios
            if (
                c.status_real == "vencido"
                or c.status_real == "cancelado"
                or c.alterado_em
                or c.excluido_em
                or c.deletado
            )
        ]

    else:

        convenios = [
            c
            for c in convenios
            if c.status_real == "ativo"
            and not c.deletado
        ]

    convenios = sorted(
        convenios,
        key=lambda c: (
            c.status_real == "vencido",
            c.dias_para_vencer
            if c.dias_para_vencer is not None
            else 9999
        )
    )

    return convenios


def criar_convenio(
    empresa_id,
    nome,
    descricao,
    tipo_convenio,
    data_fim=None,
    telefone="",
    cnpj="",
    endereco="",
    responsavel_legal="",
    documento_anexo="",
    arquivo_documento=None
):

    convenio = Convenio(
        empresa_id=empresa_id,
        nome=nome,
        descricao=descricao,
        tipo_convenio=tipo_convenio,
        data_inicio=None,
        data_fim=data_fim,
        telefone=telefone,
        cnpj=cnpj,
        endereco=endereco,
        responsavel_legal=responsavel_legal,
        documento_anexo=documento_anexo,
        status="pendente",
        arquivo_documento=arquivo_documento,
    )

    db.session.add(convenio)
    db.session.commit()

    return convenio