import os
from flask import Flask
from flask_cors import CORS

from app.config.settings import get_config
from app.models import db
from app.routes import convenios_bp, dashboard_bp, monitoramento_bp
from app.utils import register_error_handlers, setup_logging


def create_app(config=None):
    app = Flask(__name__)

    # Config
    cfg = config or get_config()
    app.config.from_object(cfg)

    # SQLAlchemy - resolve path relativo
    db_path = os.path.join(
        os.path.dirname(__file__), "../database/convenios.db"
    )
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath(db_path)}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Extensions
    db.init_app(app)
    CORS(app, origins=app.config.get("CORS_ORIGINS", "*"))

    # Logging
    setup_logging(app)

    # Error handlers
    register_error_handlers(app)

    # Blueprints
    app.register_blueprint(convenios_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(monitoramento_bp)

    # Health check
    @app.route("/health")
    def health():
        return {"status": "ok", "service": "ConvenioManager API"}, 200

    # Criar tabelas
    with app.app_context():
        db.create_all()
        _seed_data_if_empty(app)

    return app


def _seed_data_if_empty(app):
    """Popula banco com dados de exemplo se estiver vazio."""
    from app.models import Convenio
    from datetime import date, timedelta
    import random

    if Convenio.query.count() > 0:
        return

    app.logger.info("Populando banco com dados de exemplo...")

    empresas = [
        ("Tech Solutions Ltda", "12.345.678/0001-99", "techsolutions@email.com"),
        ("Inovação Digital S.A.", "98.765.432/0001-11", "inovacao@digital.com"),
        ("Grupo Educacional XYZ", "11.222.333/0001-44", "grupo@educacional.com"),
        ("StartUp Futuro Ltda", "55.666.777/0001-88", "contato@startupfuturo.com"),
        ("Indústria Conectada S.A.", "33.444.555/0001-66", "industria@conectada.com"),
        ("Consultoria Prime Ltda", "77.888.999/0001-22", "prime@consultoria.com"),
        ("DataFlow Sistemas", "22.333.444/0001-55", "dataflow@sistemas.com"),
        ("HealthTech Brasil", "44.555.666/0001-77", "healthtech@brasil.com"),
    ]

    tipos = ["Estágio", "Técnico", "Graduação", "Pesquisa"]
    responsaveis = ["Ana Lima", "Carlos Mendes", "Beatriz Costa", "Rafael Souza"]

    hoje = date.today()

    convenios_sample = [
        # Vigentes
        (empresas[0], tipos[0], -180, 180),
        (empresas[1], tipos[1], -90, 90),
        (empresas[2], tipos[2], -365, 200),
        (empresas[3], tipos[3], -60, 120),
        # Próximos do vencimento
        (empresas[4], tipos[0], -300, 20),
        (empresas[5], tipos[1], -200, 15),
        (empresas[6], tipos[2], -400, 5),
        # Vencidos
        (empresas[7], tipos[3], -400, -10),
    ]

    for empresa, tipo, inicio_delta, fim_delta in convenios_sample:
        c = Convenio(
            nome_empresa=empresa[0],
            cnpj=empresa[1],
            email_empresa=empresa[2],
            tipo_convenio=tipo,
            data_inicio=hoje + timedelta(days=inicio_delta),
            data_vencimento=hoje + timedelta(days=fim_delta),
            responsavel=random.choice(responsaveis),
            observacoes="Convênio cadastrado automaticamente como exemplo.",
        )
        db.session.add(c)

    db.session.commit()
    app.logger.info("Dados de exemplo inseridos.")
