from datetime import date
from typing import Dict, Any
import logging
import json

from app.repositories import ConvenioRepository, LogMonitoramentoRepository

logger = logging.getLogger(__name__)

DIAS_ALERTA = 30
STATUS_VIGENTE = "Vigente"
STATUS_PROXIMO = "Próximo do vencimento"
STATUS_VENCIDO = "Vencido"


class MonitoramentoService:
    """
    Agente automatizado de monitoramento preventivo.
    Responsável por verificar e atualizar o status de todos os convênios.
    """

    def __init__(self):
        self.repo = ConvenioRepository()
        self.log_repo = LogMonitoramentoRepository()

    def executar(self) -> Dict[str, Any]:
        logger.info("Iniciando rotina de monitoramento de convênios...")
        hoje = date.today()

        convenios = self.repo.get_all_ativos_para_monitoramento()
        total = len(convenios)

        updates = []
        vigentes = proximos = vencidos = 0
        detalhes = []

        for c in convenios:
            novo_status = self._calcular_status(c.data_vencimento, hoje)
            updates.append({"id": c.id, "status": novo_status})

            if novo_status == STATUS_VIGENTE:
                vigentes += 1
            elif novo_status == STATUS_PROXIMO:
                proximos += 1
                detalhes.append({
                    "id": c.id,
                    "empresa": c.nome_empresa,
                    "vencimento": c.data_vencimento.isoformat(),
                    "dias_restantes": (c.data_vencimento - hoje).days,
                    "status": novo_status
                })
            elif novo_status == STATUS_VENCIDO:
                vencidos += 1
                detalhes.append({
                    "id": c.id,
                    "empresa": c.nome_empresa,
                    "vencimento": c.data_vencimento.isoformat(),
                    "dias_restantes": (c.data_vencimento - hoje).days,
                    "status": novo_status
                })

        atualizados = self.repo.bulk_update_status(updates)

        log = self.log_repo.create({
            "total_verificados": total,
            "total_atualizados": atualizados,
            "vigentes": vigentes,
            "proximos_vencimento": proximos,
            "vencidos": vencidos,
            "detalhes": json.dumps(detalhes, ensure_ascii=False),
        })

        resultado = {
            "executado_em": log.executado_em.isoformat(),
            "total_verificados": total,
            "total_atualizados": atualizados,
            "vigentes": vigentes,
            "proximos_vencimento": proximos,
            "vencidos": vencidos,
            "criticos": detalhes,
        }

        logger.info(
            f"Monitoramento concluído: {total} verificados, "
            f"{atualizados} atualizados, {vencidos} vencidos, {proximos} próximos."
        )
        return resultado

    def _calcular_status(self, data_vencimento: date, hoje: date) -> str:
        delta = (data_vencimento - hoje).days
        if delta < 0:
            return STATUS_VENCIDO
        elif delta <= DIAS_ALERTA:
            return STATUS_PROXIMO
        else:
            return STATUS_VIGENTE

    def get_ultimo_log(self):
        logs = self.log_repo.get_last(1)
        return logs[0].to_dict() if logs else None

    def get_historico_logs(self, n: int = 10):
        logs = self.log_repo.get_last(n)
        return [l.to_dict() for l in logs]
