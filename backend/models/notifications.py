from datetime import datetime
from backend.database import db

class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    convenio_id = db.Column(db.Integer, db.Integer, db.ForeignKey("convenios.id"), nullable=False)

    titulo = db.Column(db.String(120), nullable=False)

    mensagem = db.Column(db.Text, nullable=False)

    tipo = db.Column(db.String(50), nullable=False, default="vencimento")

    lida = db.Column(db.Boolean, default=False)

    criada_em = db.Column(db.DateTime(timezone=True), default=datetime.now)
