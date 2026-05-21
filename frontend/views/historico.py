import flet as ft

from backend.database import criar_app_flask
from backend.services.convenio_service import listar_convenios
from frontend.components.cards import criar_card_convenio


app_flask = criar_app_flask()


def tela_historico(page: ft.Page):

    page.controls.clear()

    filtro = "historico"

    lista = ft.ListView(
        expand=True,
        spacing=15
    )

    titulo = ft.Text(
        "Histórico",
        size=30,
        weight=ft.FontWeight.BOLD
    )

    subtitulo = ft.Text(
        "Eventos e alterações dos convênios",
        color="#666"
    )

    def carregar():

        lista.controls.clear()

        with app_flask.app_context():

            convenios = listar_convenios(
                filtro
            )

            if not convenios:

                lista.controls.append(
                    ft.Text(
                        "Nenhum item encontrado."
                    )
                )

            for convenio in convenios:

                lista.controls.append(
                    criar_card_convenio(
                        convenio,
                        page,
                        carregar
                    )
                )

        page.update()

    def mudar(novo):

        nonlocal filtro

        filtro = novo

        carregar()

    def voltar(e):

        from frontend.views.convenios import tela_convenios

        tela_convenios(page)

    filtros = ft.Row(
        controls=[
            ft.Button(
                "Todos",
                on_click=lambda e: mudar("historico")
            ),
            ft.Button(
                "Vencidos",
                on_click=lambda e: mudar("vencido")
            ),
            ft.Button(
            "Cancelados",
            on_click=lambda e: mudar("cancelado")
            ),
            ft.Button(
                "Voltar",
                on_click=voltar
            ),
            ft.Button(
                "Alterações",
                on_click=lambda e: mudar("alterado")
            ),
        ]
    )

    page.add(
        titulo,
        subtitulo,
        filtros,
        lista
    )

    carregar()