from typing import Dict, Any, List
from datetime import date
import logging

from app.repositories import ConvenioRepository, LogMonitoramentoRepository

logger = logging.getLogger(__name__)


class DashboardService:
    def __init__(self):
        self.repo = ConvenioRepository()
        self.log_repo = LogMonitoramentoRepository()

    def get_metrics(self) -> Dict[str, Any]:
        counts = self.repo.count_by_status()
        total = sum(counts.values())

        vigentes = counts.get("Vigente", 0)
        proximos = counts.get("Próximo do vencimento", 0)
        vencidos = counts.get("Vencido", 0)

        ultimo_log = self.log_repo.get_last(1)

        return {
            "total": total,
            "vigentes": vigentes,
            "proximos_vencimento": proximos,
            "vencidos": vencidos,
            "percentual_vigentes": round((vigentes / total * 100) if total > 0 else 0, 1),
            "percentual_criticos": round(((proximos + vencidos) / total * 100) if total > 0 else 0, 1),
            "ultima_atualizacao": ultimo_log[0].executado_em.isoformat() if ultimo_log else None,
        }

    def get_critical(self, limite: int = 15) -> List[Dict[str, Any]]:
        criticos = self.repo.get_criticos(limite)
        return [c.to_dict() for c in criticos]
