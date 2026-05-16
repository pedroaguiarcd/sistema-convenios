from flask import Blueprint, jsonify, request
from app.services import MonitoramentoService

monitoramento_bp = Blueprint("monitoramento", __name__, url_prefix="/monitoramento")
service = MonitoramentoService()


@monitoramento_bp.route("/run", methods=["POST"])
def run():
    resultado = service.executar()
    return jsonify({"data": resultado, "message": "Monitoramento executado com sucesso"}), 200


@monitoramento_bp.route("/logs", methods=["GET"])
def logs():
    n = int(request.args.get("n", 10))
    historico = service.get_historico_logs(n)
    return jsonify({"data": historico, "total": len(historico)}), 200


@monitoramento_bp.route("/logs/ultimo", methods=["GET"])
def ultimo_log():
    log = service.get_ultimo_log()
    if not log:
        return jsonify({"data": None, "message": "Nenhum log encontrado"}), 200
    return jsonify({"data": log}), 200
