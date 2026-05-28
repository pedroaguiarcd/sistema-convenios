from backend.database import criar_app_flask

from backend.routes.notifications import notificacoes_bp
from backend.routes.auth import auth_bp
from backend.routes.empresas import empresas_bp
from backend.routes.convenios import convenios_bp
from backend.routes.dashboard import dashboard_bp


def create_app():
    app = criar_app_flask()

    app.register_blueprint(notificacoes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(empresas_bp)
    app.register_blueprint(convenios_bp)
    app.register_blueprint(dashboard_bp)

    return app
