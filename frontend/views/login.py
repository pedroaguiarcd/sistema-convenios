import flet as ft

from backend.database import criar_app_flask
from backend.services.auth_service import autenticar_usuario
from frontend.views.convenios import tela_convenios
from frontend.views.painel_empresa import tela_empresa


app_flask = criar_app_flask()


def tela_login(page: ft.Page):

    page.controls.clear()

    email = ft.TextField(
        label="E-mail",
        width=350
    )

    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=350
    )

    mensagem = ft.Text(
        "",
        color="red"
    )

    def entrar(e):

        with app_flask.app_context():

            usuario = autenticar_usuario(
                email.value,
                senha.value
            )

        if not usuario:

            mensagem.value = "E-mail ou senha inválidos."
            page.update()
            return

        page.usuario_logado = usuario

        page.controls.clear()

        if usuario.perfil == "empresa":

            tela_empresa(page)

        else:

            tela_convenios(page)

        page.update()

    card_login = ft.Container(
        width=420,
        padding=30,
        bgcolor="#FFFFFF",
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color="#00000022",
            offset=ft.Offset(0, 2),
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Login",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#222"
                ),

                ft.Text(
                    "Sistema de Gestão de Convênios",
                    size=14,
                    color="#555"
                ),

                email,

                senha,

                ft.Button(
                    "Entrar",
                    on_click=entrar
                ),

                mensagem
            ]
        )
    )

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                card_login
            ]
        )
    )