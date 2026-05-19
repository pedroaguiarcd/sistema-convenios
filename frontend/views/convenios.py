import flet as ft

from backend.database import criar_app_flask
from backend.services.convenio_service import listar_convenios
from frontend.components.cards import criar_card_convenio


app_flask = criar_app_flask()


def tela_convenios(page: ft.Page):

    filtro_status = "todos"

    lista = ft.ListView(
        expand=True,
        spacing=15,
        auto_scroll=False
    )

    titulo = ft.Text(
        "Sistema de Gestão de Convênios",
        size=30,
        weight=ft.FontWeight.BOLD,
        color="#222"
    )

    def carregar_convenios():
        lista.controls.clear()

        with app_flask.app_context():
            convenios = listar_convenios(
                filtro_status
            )

            if not convenios:
                lista.controls.append(
                    ft.Text(
                        "Nenhum convênio encontrado.",
                        color="#333"
                    )
                )

            for convenio in convenios:
                lista.controls.append(
                    criar_card_convenio(convenio)
                )

        page.update()

    def filtrar(status):
        nonlocal filtro_status

        filtro_status = status

        carregar_convenios()

    filtros = ft.Row(
        controls=[
            ft.Button(
                "Todos",
                on_click=lambda e: filtrar("todos")
            ),

            ft.Button(
                "Ativos",
                on_click=lambda e: filtrar("ativo")
            ),

            ft.Button(
                "Pendentes",
                on_click=lambda e: filtrar("pendente")
            ),

            ft.Button(
                "Vencidos",
                on_click=lambda e: filtrar("vencido")
            ),
        ]
    )

    page.add(
        titulo,
        filtros,
        lista
    )

    carregar_convenios()