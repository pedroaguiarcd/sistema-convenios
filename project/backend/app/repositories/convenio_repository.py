from typing import List, Optional, Dict, Any
from datetime import date
from app.models import db, Convenio


class ConvenioRepository:
    """Repositório responsável por toda persistência de Convenio."""

    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Convenio]:
        query = Convenio.query.filter_by(ativo=True)

        if filters:
            if filters.get("status"):
                query = query.filter(Convenio.status == filters["status"])
            if filters.get("nome_empresa"):
                query = query.filter(
                    Convenio.nome_empresa.ilike(f"%{filters['nome_empresa']}%")
                )
            if filters.get("tipo_convenio"):
                query = query.filter(
                    Convenio.tipo_convenio.ilike(f"%{filters['tipo_convenio']}%")
                )

        return query.order_by(Convenio.data_vencimento.asc()).all()

    def get_by_id(self, convenio_id: int) -> Optional[Convenio]:
        return Convenio.query.filter_by(id=convenio_id, ativo=True).first()

    def create(self, data: Dict[str, Any]) -> Convenio:
        convenio = Convenio(**data)
        db.session.add(convenio)
        db.session.commit()
        return convenio

    def update(self, convenio_id: int, data: Dict[str, Any]) -> Optional[Convenio]:
        convenio = self.get_by_id(convenio_id)
        if not convenio:
            return None
        for key, value in data.items():
            if hasattr(convenio, key):
                setattr(convenio, key, value)
        db.session.commit()
        return convenio

    def soft_delete(self, convenio_id: int) -> bool:
        convenio = self.get_by_id(convenio_id)
        if not convenio:
            return False
        convenio.ativo = False
        db.session.commit()
        return True

    def get_criticos(self, limite: int = 10) -> List[Convenio]:
        hoje = date.today()
        return (
            Convenio.query
            .filter_by(ativo=True)
            .filter(Convenio.status.in_(["Próximo do vencimento", "Vencido"]))
            .order_by(Convenio.data_vencimento.asc())
            .limit(limite)
            .all()
        )

    def get_all_ativos_para_monitoramento(self) -> List[Convenio]:
        return Convenio.query.filter_by(ativo=True).all()

    def bulk_update_status(self, updates: List[Dict[str, Any]]) -> int:
        """Atualiza status de múltiplos convênios. Retorna qtd atualizada."""
        count = 0
        for upd in updates:
            convenio = Convenio.query.get(upd["id"])
            if convenio and convenio.status != upd["status"]:
                convenio.status = upd["status"]
                count += 1
        db.session.commit()
        return count

    def count_by_status(self) -> Dict[str, int]:
        from sqlalchemy import func
        results = (
            db.session.query(Convenio.status, func.count(Convenio.id))
            .filter_by(ativo=True)
            .group_by(Convenio.status)
            .all()
        )
        return {status: count for status, count in results}
