from backend.database import criar_app_flask, db
from backend.models.usuario import Usuario

app = criar_app_flask()

with app.app_context():
    db.create_all()
    print("Tabelas criadas!")