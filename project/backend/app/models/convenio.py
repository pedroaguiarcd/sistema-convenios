from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Convenio(db.Model):
    __tablename__ = "convenios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_empresa = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(18), nullable=False)
    tipo_convenio = db.Column(db.String(100), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Vigente")
    responsavel = db.Column(db.String(255), nullable=False)
    email_empresa = db.Column(db.String(255), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        from datetime import date
        hoje = date.today()
        dias_restantes = (self.data_vencimento - hoje).days if self.data_vencimento else None

        return {
            "id": self.id,
            "nome_empresa": self.nome_empresa,
            "cnpj": self.cnpj,
            "tipo_convenio": self.tipo_convenio,
            "data_inicio": self.data_inicio.isoformat() if self.data_inicio else None,
            "data_vencimento": self.data_vencimento.isoformat() if self.data_vencimento else None,
            "status": self.status,
            "responsavel": self.responsavel,
            "email_empresa": self.email_empresa,
            "observacoes": self.observacoes,
            "ativo": self.ativo,
            "dias_restantes": dias_restantes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Convenio {self.id} - {self.nome_empresa}>"


class LogMonitoramento(db.Model):
    __tablename__ = "logs_monitoramento"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    executado_em = db.Column(db.DateTime, default=datetime.utcnow)
    total_verificados = db.Column(db.Integer, default=0)
    total_atualizados = db.Column(db.Integer, default=0)
    vigentes = db.Column(db.Integer, default=0)
    proximos_vencimento = db.Column(db.Integer, default=0)
    vencidos = db.Column(db.Integer, default=0)
    detalhes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "executado_em": self.executado_em.isoformat() if self.executado_em else None,
            "total_verificados": self.total_verificados,
            "total_atualizados": self.total_atualizados,
            "vigentes": self.vigentes,
            "proximos_vencimento": self.proximos_vencimento,
            "vencidos": self.vencidos,
            "detalhes": self.detalhes,
        }
