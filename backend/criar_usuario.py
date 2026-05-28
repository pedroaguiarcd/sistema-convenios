from backend.database import criar_app_flask, db

from backend.models.usuario import Usuario

from werkzeug.security import generate_password_hash


app = criar_app_flask()


with app.app_context():

    usuario = Usuario(

        nome="Gestor de Convênios",

        email="gestor@teste.com",

        senha=generate_password_hash("123456"),

        perfil="gestor"

    )


    db.session.add(usuario)

    db.session.commit()


    print("Usuário gestor criado!")
