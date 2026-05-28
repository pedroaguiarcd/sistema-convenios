from werkzeug.security import generate_password_hash, check_password_hash

from backend.database import db
from backend.models.usuario import Usuario


def cadastrar_usuario(nome, email, senha, perfil):
    usuario_existente = Usuario.query.filter_by(
        email=email
    ).first()

    if usuario_existente:
        return None

    senha_criptografada = generate_password_hash(
        senha
    )

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha_criptografada,
        perfil=perfil
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return novo_usuario


def autenticar_usuario(email, senha):
    usuario = Usuario.query.filter_by(
        email=email
    ).first()

    if not usuario:
        return None

    senha_valida = check_password_hash(
        usuario.senha,
        senha
    )

    if not senha_valida:
        return None

    return usuario