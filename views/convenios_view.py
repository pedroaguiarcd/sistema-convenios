
import flet as ft

from components.sidebar import Sidebar


class ConveniosView(ft.View):

    def __init__(self, page: ft.Page):

        super().__init__(
            route="/convenios"
        )

        self.search = ft.TextField(
            label="Buscar convênio",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=12,
            width=400
        )

        self.controls = [

            ft.Row(
                expand=True,

                controls=[

                    Sidebar(page),

                    ft.Container(
                        expand=True,
                        padding=30,

                        content=ft.Column(
                            scroll=ft.ScrollMode.AUTO,

                            controls=[

                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                    controls=[

                                        ft.Text(
                                            "Gerenciamento de Convênios",
                                            size=30,
                                            weight=ft.FontWeight.BOLD
                                        ),

                                        ft.ElevatedButton(
                                            "Novo Convênio",
                                            icon=ft.Icons.ADD,

                                            style=ft.ButtonStyle(
                                                bgcolor="#2563EB",
                                                color="white",
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=10
                                                )
                                            )
                                        )
                                    ]
                                ),

                                ft.Container(height=20),

                                self.search,

                                ft.Container(height=20),

                                self.table()
                            ]
                        )
                    )
                ]
            )
        ]

    def table(self):

        return ft.Container(
        height=400,
        bgcolor="red"
    )

    def convenio_card(
        self,
        instituicao,
        tipo,
        inicio,
        fim,
        status
    ):

        colors = {
            "ATIVO": "#16A34A",
            "ALERTA": "#F59E0B",
            "EXPIRADO": "#DC2626"
        }

        return ft.Card(

            elevation=2,

            content=ft.Container(

                bgcolor="white",
                border_radius=16,

                content=ft.Row(

                    controls=[

                        # BARRA LATERAL
                        ft.Container(
                            width=10,
                            height=120,
                            bgcolor=colors[status],
                            border_radius=10
                        ),

                        # CONTEÚDO
                        ft.Container(
                            expand=True,
                            padding=20,

                            content=ft.Row(

                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    # ESQUERDA
                                    ft.Column(

                                        spacing=5,

                                        controls=[

                                            ft.Text(
                                                instituicao,
                                                size=20,
                                                weight=ft.FontWeight.BOLD
                                            ),

                                            ft.Text(
                                                f"Tipo: {tipo}"
                                            ),

                                            ft.Text(
                                                f"Início: {inicio}"
                                            ),

                                            ft.Text(
                                                f"Vencimento: {fim}"
                                            ),
                                        ]
                                    ),

                                    # DIREITA
                                    ft.Container(
                                        bgcolor=colors[status],
                                        padding=10,
                                        border_radius=20,

                                        content=ft.Text(
                                            status,
                                            color="white",
                                            weight=ft.FontWeight.BOLD
                                        )
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        )