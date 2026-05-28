import flet as ft
from datetime import date

from backend.database import criar_app_flask
from backend.models.convenio import Convenio
from frontend.components.cards import criar_card_convenio


app_flask = criar_app_flask()


def tela_proximos_vencimento(page: ft.Page):

    page.controls.clear()

    lista = ft.ListView(
        expand=True,
        spacing=18
    )

    titulo = ft.Text(
        "Convênios próximos do vencimento",
        size=32,
        weight=ft.FontWeight.BOLD
    )

    subtitulo = ft.Text(
        "Convênios que vencem nos próximos 30 dias",
        color="#6B7280"
    )

    def voltar(e):

        from frontend.views.convenios import tela_convenios

        tela_convenios(page)

    with app_flask.app_context():

        hoje = date.today()

        convenios = (
            Convenio.query
            .filter(
                Convenio.status == "ativo",
                Convenio.deletado == False,
                Convenio.data_fim != None
            )
            .order_by(
                Convenio.data_fim.asc()
            )
            .all()
        )

        convenios = [

            convenio

            for convenio in convenios

            if 1 <= (
                convenio.data_fim
                -
                hoje
            ).days <= 30
        ]

        if not convenios:

            lista.controls.append(

                ft.Text(
                    "Nenhum convênio próximo do vencimento."
                )
            )

        for convenio in convenios:

            lista.controls.append(
                criar_card_convenio(
                    convenio,
                    page
                )
            )

    page.add(

        ft.Container(

            padding=30,

            content=ft.Column(

                controls=[

                    titulo,
                    subtitulo,

                    ft.Button(
                        "Voltar",
                        on_click=voltar
                    ),

                    lista

                ]
            )
        )
    )