import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

_scheduler = None


def iniciar_scheduler(app):
    global _scheduler

    with app.app_context():
        from app.services import MonitoramentoService

        def job_monitoramento():
            with app.app_context():
                try:
                    svc = MonitoramentoService()
                    resultado = svc.executar()
                    logger.info(
                        f"[Scheduler] Monitoramento automático concluído: "
                        f"{resultado['total_verificados']} verificados."
                    )
                except Exception as e:
                    logger.error(f"[Scheduler] Erro no monitoramento automático: {e}")

        intervalo_horas = app.config.get("SCHEDULER_INTERVAL_HOURS", 24)

        _scheduler = BackgroundScheduler(daemon=True)
        _scheduler.add_job(
            func=job_monitoramento,
            trigger=IntervalTrigger(hours=intervalo_horas),
            id="monitoramento_automatico",
            name="Monitoramento Automático de Convênios",
            replace_existing=True,
        )
        _scheduler.start()
        logger.info(f"[Scheduler] Agendado para executar a cada {intervalo_horas}h.")

        # Executa uma vez ao iniciar
        job_monitoramento()


def parar_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("[Scheduler] Parado.")
