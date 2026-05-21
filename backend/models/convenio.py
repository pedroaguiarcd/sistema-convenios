from datetime import date

from backend.database import db


class Convenio(db.Model):
    __tablename__ = "convenios"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    empresa = db.relationship(
        "Empresa",
        backref="convenios"
    )

    descricao = db.Column(
        db.String(100),
        nullable=False
    )

    tipo_convenio = db.Column(
        db.Enum(
            "obrigatorio",
            "nao_obrigatorio",
            "supervisionado"
        ),
        nullable=False,
        default="supervisionado"
    )

    data_inicio = db.Column(
        db.Date,
        nullable=True
    )

    data_fim = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.Enum(
            "ativo",
            "pendente",
            "cancelado"
        ),
        nullable=False,
        default="pendente"
    )

    telefone = db.Column(db.String(20))

    cnpj = db.Column(
        db.String(100),
        nullable=False
    )

    endereco = db.Column(db.String(255))

    responsavel_legal = db.Column(db.String(100))

    documento_anexo = db.Column(
    db.String(255))

    data_aprovacao = db.Column(db.Date)

    data_cancelamento = db.Column(db.Date)

    aprovado_por = db.Column(db.String(100))

    motivo_cancelamento = db.Column(db.String(255))

    alterado_em = db.Column(db.DateTime)

    excluido_em = db.Column(db.DateTime)

    motivo_alteracao = db.Column(db.String(255))

    campos_alterados = db.Column(db.Text)

    motivo_exclusao = db.Column(db.String(255))

    deletado = db.Column(
        db.Boolean,
        default=False
    )

    @property
    def dias_para_vencer(self):

        if not self.data_fim:
            return None

        return (
            self.data_fim
            -
            date.today()
        ).days

    @property
    def status_real(self):

        if self.status == "pendente":
            return "pendente"

        if self.status == "cancelado":
            return "cancelado"

        if self.dias_para_vencer is not None and self.dias_para_vencer <= 0:
            return "vencido"

        return "ativo"

    @property
    def tipo_convenio_formatado(self):

        if self.tipo_convenio == "obrigatorio":
            return "Obrigatório"

        if self.tipo_convenio == "nao_obrigatorio":
            return "Não obrigatório"

        return "Supervisionado"