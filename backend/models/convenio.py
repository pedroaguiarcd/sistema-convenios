from datetime import date

from backend.database import db


class Convenio(db.Model):
    __tablename__ = "convenios"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, nullable=False)

    descricao = db.Column(db.String(100), nullable=False)

    data_inicio = db.Column(db.Date, nullable=False)

    data_fim = db.Column(db.Date, nullable=False)

    status = db.Column(
        db.Enum(
            "ativo",
            "pendente",
            "vencido",
            "cancelado"
        ),
        nullable=False,
        default="pendente"
    )

    telefone = db.Column(db.String(20))

    cnpj = db.Column(db.String(100), nullable=False)

    endereco = db.Column(db.String(255))

    responsavel_legal = db.Column(db.String(100))

    @property
    def dias_para_vencer(self):
        return (self.data_fim - date.today()).days

    @property
    def status_real(self):
        if self.dias_para_vencer < 0:
            return "vencido"

        if self.dias_para_vencer <= 30:
            return "pendente"

        return "ativo"