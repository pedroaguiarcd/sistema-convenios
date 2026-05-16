from datetime import date, datetime
from typing import List, Optional, Dict, Any
import logging

from app.repositories import ConvenioRepository

logger = logging.getLogger(__name__)

TIPOS_CONVENIO = ["Estágio", "Técnico", "Graduação", "Pós-Graduação", "Pesquisa", "Extensão", "Outro"]

STATUS_VIGENTE = "Vigente"
STATUS_PROXIMO = "Próximo do vencimento"
STATUS_VENCIDO = "Vencido"


class ConvenioService:
    def __init__(self):
        self.repo = ConvenioRepository()

    def listar(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict]:
        convenios = self.repo.get_all(filters)
        return [c.to_dict() for c in convenios]

    def buscar_por_id(self, convenio_id: int) -> Optional[Dict]:
        c = self.repo.get_by_id(convenio_id)
        return c.to_dict() if c else None

    def criar(self, data: Dict[str, Any]) -> Dict:
        validated = self._validate_and_parse(data)
        validated["status"] = self._calcular_status(validated["data_vencimento"])
        convenio = self.repo.create(validated)
        logger.info(f"Convênio criado: ID={convenio.id}, empresa={convenio.nome_empresa}")
        return convenio.to_dict()

    def atualizar(self, convenio_id: int, data: Dict[str, Any]) -> Optional[Dict]:
        existing = self.repo.get_by_id(convenio_id)
        if not existing:
            return None
        validated = self._validate_and_parse(data, partial=True)
        vencimento = validated.get("data_vencimento", existing.data_vencimento)
        validated["status"] = self._calcular_status(vencimento)
        convenio = self.repo.update(convenio_id, validated)
        logger.info(f"Convênio atualizado: ID={convenio_id}")
        return convenio.to_dict() if convenio else None

    def deletar(self, convenio_id: int) -> bool:
        result = self.repo.soft_delete(convenio_id)
        if result:
            logger.info(f"Convênio removido (soft delete): ID={convenio_id}")
        return result

    def listar_criticos(self, limite: int = 10) -> List[Dict]:
        criticos = self.repo.get_criticos(limite)
        return [c.to_dict() for c in criticos]

    def _calcular_status(self, data_vencimento: date, dias_alerta: int = 30) -> str:
        hoje = date.today()
        delta = (data_vencimento - hoje).days
        if delta < 0:
            return STATUS_VENCIDO
        elif delta <= dias_alerta:
            return STATUS_PROXIMO
        else:
            return STATUS_VIGENTE

    def _validate_and_parse(self, data: Dict[str, Any], partial: bool = False) -> Dict[str, Any]:
        result = {}

        campos_obrigatorios = [
            "nome_empresa", "cnpj", "tipo_convenio",
            "data_inicio", "data_vencimento", "responsavel"
        ]

        if not partial:
            for campo in campos_obrigatorios:
                if campo not in data or not data[campo]:
                    raise ValueError(f"Campo obrigatório ausente: {campo}")

        if "nome_empresa" in data:
            result["nome_empresa"] = str(data["nome_empresa"]).strip()
        if "cnpj" in data:
            result["cnpj"] = str(data["cnpj"]).strip()
        if "tipo_convenio" in data:
            result["tipo_convenio"] = str(data["tipo_convenio"]).strip()
        if "responsavel" in data:
            result["responsavel"] = str(data["responsavel"]).strip()
        if "email_empresa" in data:
            result["email_empresa"] = data["email_empresa"]
        if "observacoes" in data:
            result["observacoes"] = data["observacoes"]

        if "data_inicio" in data:
            result["data_inicio"] = self._parse_date(data["data_inicio"])
        if "data_vencimento" in data:
            result["data_vencimento"] = self._parse_date(data["data_vencimento"])

        if "data_inicio" in result and "data_vencimento" in result:
            if result["data_vencimento"] <= result["data_inicio"]:
                raise ValueError("Data de vencimento deve ser posterior à data de início")

        return result

    def _parse_date(self, value) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
        raise ValueError(f"Formato de data inválido: {value}")
