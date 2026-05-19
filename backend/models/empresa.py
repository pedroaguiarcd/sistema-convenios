from backend.database import db


class Empresa(db.Model):
    __tablename__ = "empresas"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(255), nullable=False)

    cnpj = db.Column(db.String(20))

    email = db.Column(db.String(255))

    telefone = db.Column(db.String(20))