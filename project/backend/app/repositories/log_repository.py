from app.models import db, LogMonitoramento
from typing import List


class LogMonitoramentoRepository:

    def create(self, data: dict) -> LogMonitoramento:
        log = LogMonitoramento(**data)
        db.session.add(log)
        db.session.commit()
        return log

    def get_last(self, n: int = 5) -> List[LogMonitoramento]:
        return (
            LogMonitoramento.query
            .order_by(LogMonitoramento.executado_em.desc())
            .limit(n)
            .all()
        )
