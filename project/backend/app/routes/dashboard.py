from flask import Blueprint, request, jsonify
from app.services import DashboardService

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
service = DashboardService()


@dashboard_bp.route("/metrics", methods=["GET"])
def metrics():
    data = service.get_metrics()
    return jsonify({"data": data}), 200


@dashboard_bp.route("/critical", methods=["GET"])
def critical():
    limite = int(request.args.get("limite", 15))
    data = service.get_critical(limite)
    return jsonify({"data": data, "total": len(data)}), 200
