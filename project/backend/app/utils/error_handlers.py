from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Recurso não encontrado", "status": 404}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Método não permitido", "status": 405}), 405

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({"error": "Dados inválidos", "status": 422}), 422

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Erro interno: {e}")
        return jsonify({"error": "Erro interno do servidor", "status": 500}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Exceção não tratada: {e}", exc_info=True)
        return jsonify({"error": "Erro inesperado", "detail": str(e), "status": 500}), 500
