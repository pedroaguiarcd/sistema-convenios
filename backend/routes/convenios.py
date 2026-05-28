from flask import Blueprint, request, jsonify
from datetime import datetime

from backend.services.convenio_service import (
    listar_convenios,
    criar_convenio,
    aprovar_convenio,
    cancelar_convenio,
    excluir_convenio,
)
from backend.models.convenio import Convenio
from backend.database import db
from backend.utils.helpers import require_auth, require_perfil, get_current_user

convenios_bp = Blueprint("convenios", __name__, url_prefix="/convenios")

CAMPOS_EDITAVEIS = ("descricao", "tipo_convenio", "telefone", "endereco", "responsavel_legal")


def _convenio_to_dict(c):
    return {
        "id": c.id,
        "empresa_id": c.empresa_id,
        "empresa_nome": c.empresa.nome if c.empresa else None,
        "descricao": c.descricao,
        "tipo_convenio": c.tipo_convenio,
        "tipo_convenio_formatado": c.tipo_convenio_formatado,
        "status": c.status,
        "status_real": c.status_real,
        "data_inicio": c.data_inicio.isoformat() if c.data_inicio else None,
        "data_fim": c.data_fim.isoformat() if c.data_fim else None,
        "dias_para_vencer": c.dias_para_vencer,
        "telefone": c.telefone,
        "cnpj": c.cnpj,
        "endereco": c.endereco,
        "responsavel_legal": c.responsavel_legal,
        "documento_anexo": c.documento_anexo,
        "arquivo_documento": c.arquivo_documento,
        "aprovado_por": c.aprovado_por,
        "data_aprovacao": c.data_aprovacao.isoformat() if c.data_aprovacao else None,
        "motivo_cancelamento": c.motivo_cancelamento,
        "motivo_alteracao": c.motivo_alteracao,
        "campos_alterados": c.campos_alterados,
        "alterado_em": c.alterado_em.isoformat() if c.alterado_em else None,
        "deletado": c.deletado,
    }


@convenios_bp.get("/")
@require_auth
def listar():
    user_id, perfil = get_current_user()
    status = request.args.get("status")  # ativo | vencido | cancelado | historico | alterado

    if perfil == "empresa":
        from backend.models.usuario import Usuario
        usuario = Usuario.query.get(user_id)
        convenios = (
            Convenio.query
            .filter_by(empresa_id=usuario.empresa_id, deletado=False)
            .filter(Convenio.status != "cancelado")
            .order_by(Convenio.id.desc())
            .all()
        )
    else:
        convenios = listar_convenios(status)

    return jsonify([_convenio_to_dict(c) for c in convenios])


@convenios_bp.get("/<int:convenio_id>")
@require_auth
def obter(convenio_id):
    convenio = Convenio.query.get_or_404(convenio_id)
    return jsonify(_convenio_to_dict(convenio))


@convenios_bp.post("/")
@require_perfil("empresa")
def criar():
    data = request.get_json()

    required = ("empresa_id", "descricao", "tipo_convenio", "data_fim", "cnpj")
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"erro": f"Campos obrigatórios ausentes: {', '.join(missing)}"}), 400

    convenio = criar_convenio(
        empresa_id=data["empresa_id"],
        nome=data.get("nome", ""),
        descricao=data["descricao"],
        tipo_convenio=data["tipo_convenio"],
        data_fim=data["data_fim"],
        telefone=data.get("telefone", ""),
        cnpj=data["cnpj"],
        endereco=data.get("endereco", ""),
        responsavel_legal=data.get("responsavel_legal", ""),
        documento_anexo=data.get("documento_anexo", ""),
        arquivo_documento=data.get("arquivo_documento"),
    )

    return jsonify(_convenio_to_dict(convenio)), 201


@convenios_bp.patch("/<int:convenio_id>")
@require_auth
def editar(convenio_id):

    data = request.get_json()
    motivo = (data.get("motivo") or "").strip()

    if not motivo:
        return jsonify({"erro": "Informe o motivo da alteração"}), 400

    convenio = Convenio.query.get_or_404(convenio_id)

    campos_alterados = []
    for campo in CAMPOS_EDITAVEIS:
        if campo not in data:
            continue
        valor_antigo = getattr(convenio, campo)
        valor_novo = data[campo]
        if valor_novo != valor_antigo:
            campos_alterados.append(
                f"{campo}: '{valor_antigo}' → '{valor_novo}'"
            )
            setattr(convenio, campo, valor_novo)

    if not campos_alterados:
        return jsonify({"erro": "Nenhum campo foi alterado"}), 422

    convenio.alterado_em = datetime.now()
    convenio.motivo_alteracao = motivo
    convenio.campos_alterados = "\n".join(campos_alterados)

    db.session.commit()
    return jsonify(_convenio_to_dict(convenio))


@convenios_bp.post("/<int:convenio_id>/aprovar")
@require_perfil("gestor", "admin")
def aprovar(convenio_id):
    data = request.get_json() or {}
    gestor = data.get("gestor", "Gestor UESPI")

    convenio = aprovar_convenio(convenio_id, gestor)
    if not convenio:
        return jsonify({"erro": "Convênio não encontrado"}), 404

    return jsonify(_convenio_to_dict(convenio))


@convenios_bp.post("/<int:convenio_id>/cancelar")
@require_perfil("gestor", "admin")
def cancelar(convenio_id):
    data = request.get_json() or {}
    motivo = data.get("motivo", "")

    convenio = cancelar_convenio(convenio_id, motivo)
    if not convenio:
        return jsonify({"erro": "Convênio não encontrado"}), 404

    return jsonify(_convenio_to_dict(convenio))


@convenios_bp.delete("/<int:convenio_id>")
@require_perfil("gestor", "admin")
def excluir(convenio_id):
    data = request.get_json() or {}
    motivo = data.get("motivo", "")

    convenio = excluir_convenio(convenio_id, motivo)
    if not convenio:
        return jsonify({"erro": "Convênio não encontrado"}), 404

    return jsonify({"mensagem": "Convênio excluído", "id": convenio_id})


@convenios_bp.post("/com-documento")
@require_perfil("empresa")
def criar_com_documento():

    import os
    from werkzeug.utils import secure_filename

    empresa_id = request.form.get("empresa_id")
    descricao = request.form.get("descricao")
    tipo_convenio = request.form.get("tipo_convenio")
    data_fim = request.form.get("data_fim")
    cnpj = request.form.get("cnpj")

    required = {"empresa_id": empresa_id, "descricao": descricao,
                 "tipo_convenio": tipo_convenio, "data_fim": data_fim, "cnpj": cnpj}
    missing = [k for k, v in required.items() if not v]
    if missing:
        return jsonify({"erro": f"Campos obrigatórios ausentes: {', '.join(missing)}"}), 400

    arquivo = request.files.get("documento")
    arquivo_salvo = None
    nome_documento = ""

    if arquivo and arquivo.filename:
        os.makedirs("uploads/documentos", exist_ok=True)
        nome_documento = secure_filename(arquivo.filename)
        destino = os.path.join("uploads", "documentos", nome_documento)
        arquivo.save(destino)
        arquivo_salvo = destino

    convenio = criar_convenio(
        empresa_id=int(empresa_id),
        nome=request.form.get("nome", ""),
        descricao=descricao,
        tipo_convenio=tipo_convenio,
        data_fim=data_fim,
        telefone=request.form.get("telefone", ""),
        cnpj=cnpj,
        endereco=request.form.get("endereco", ""),
        responsavel_legal=request.form.get("responsavel_legal", ""),
        documento_anexo=nome_documento,
        arquivo_documento=arquivo_salvo,
    )

    return jsonify(_convenio_to_dict(convenio)), 201
