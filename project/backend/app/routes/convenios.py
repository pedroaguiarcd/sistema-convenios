from flask import Blueprint, request, jsonify
from app.services import ConvenioService

convenios_bp = Blueprint("convenios", __name__, url_prefix="/convenios")
service = ConvenioService()


@convenios_bp.route("", methods=["GET"])
def listar():
    filters = {
        "status": request.args.get("status"),
        "nome_empresa": request.args.get("empresa"),
        "tipo_convenio": request.args.get("tipo"),
    }
    filters = {k: v for k, v in filters.items() if v}
    convenios = service.listar(filters)
    return jsonify({"data": convenios, "total": len(convenios)}), 200


@convenios_bp.route("/<int:convenio_id>", methods=["GET"])
def buscar(convenio_id):
    convenio = service.buscar_por_id(convenio_id)
    if not convenio:
        return jsonify({"error": "Convênio não encontrado"}), 404
    return jsonify({"data": convenio}), 200


@convenios_bp.route("", methods=["POST"])
def criar():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Payload JSON inválido"}), 400
    try:
        convenio = service.criar(data)
        return jsonify({"data": convenio, "message": "Convênio criado com sucesso"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 422


@convenios_bp.route("/<int:convenio_id>", methods=["PUT"])
def atualizar(convenio_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Payload JSON inválido"}), 400
    try:
        convenio = service.atualizar(convenio_id, data)
        if not convenio:
            return jsonify({"error": "Convênio não encontrado"}), 404
        return jsonify({"data": convenio, "message": "Convênio atualizado com sucesso"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 422


@convenios_bp.route("/<int:convenio_id>", methods=["DELETE"])
def deletar(convenio_id):
    result = service.deletar(convenio_id)
    if not result:
        return jsonify({"error": "Convênio não encontrado"}), 404
    return jsonify({"message": "Convênio removido com sucesso"}), 200
