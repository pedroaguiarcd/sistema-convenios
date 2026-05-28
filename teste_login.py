from backend.database import criar_app_flask

from backend.models.usuario import Usuario

from werkzeug.security import check_password_hash


app = criar_app_flask()


with app.app_context():

    usuario = Usuario.query.filter_by(

        email="gestor@teste.com"

    ).first()


    print(usuario)


    if usuario:

        print(usuario.nome)

        print(usuario.email)

        print(usuario.perfil)

        print(

            check_password_hash(

                usuario.senha,

                "123456"

            )

        )
