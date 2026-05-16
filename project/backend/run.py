import os
import sys

# Garante que o backend/ está no path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.config.settings import get_config

app = create_app()

if __name__ == "__main__":
    cfg = get_config()

    # Inicia o scheduler se habilitado
    if cfg.SCHEDULER_ENABLED:
        from app.scheduler import iniciar_scheduler
        iniciar_scheduler(app)

    app.run(
        host=cfg.HOST,
        port=cfg.PORT,
        debug=cfg.DEBUG,
        use_reloader=False,  # Evita duplo scheduler em debug
    )
