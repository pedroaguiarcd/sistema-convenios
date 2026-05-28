#Dashboard principal

import flet as ft

from components.sidebar import Sidebar


class DashboardView(ft.View):

    def __init__(self, page: ft.Page):

        super().__init__(
            route="/dashboard"
        )

        self.controls = [
            ft.Row(
                expand=True,
                controls=[

                    # SIDEBAR
                    Sidebar(page),

                    # CONTEÚDO PRINCIPAL
                    ft.Container(
                        expand=True,
                        padding=30,

                        content=ft.Column(
                            scroll=ft.ScrollMode.AUTO,

                            controls=[

                                # TOPO
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                    controls=[

                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Dashboard",
                                                    size=34,
                                                    weight=ft.FontWeight.BOLD,
                                                    color="#111827"
                                                ),

                                                ft.Text(
                                                    "Painel de gerenciamento de convênios",
                                                    size=14,
                                                    color="#6B7280"
                                                )
                                            ]
                                        ),

                                        ft.Container(
                                            padding=12,
                                            border_radius=12,
                                            bgcolor="white",

                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(
                                                        ft.Icons.NOTIFICATIONS,
                                                        color="#F59E0B"
                                                    ),

                                                    ft.Text(
                                                        "12 Alertas",
                                                        weight=ft.FontWeight.W_600
                                                    )
                                                ]
                                            )
                                        )
                                    ]
                                ),

                                ft.Container(height=30),

                                # CARDS RESPONSIVOS
                                ft.ResponsiveRow(
                                    controls=[

                                        ft.Container(
                                            col={"sm": 12, "md": 6, "xl": 3},

                                            content=self.metric_card(
                                                title="Convênios Ativos",
                                                value="152",
                                                icon=ft.Icons.CHECK_CIRCLE,
                                                color="#2563EB"
                                            )
                                        ),

                                        ft.Container(
                                            col={"sm": 12, "md": 6, "xl": 3},

                                            content=self.metric_card(
                                                title="Vencendo em 30 dias",
                                                value="12",
                                                icon=ft.Icons.WARNING,
                                                color="#F59E0B"
                                            )
                                        ),

                                        ft.Container(
                                            col={"sm": 12, "md": 6, "xl": 3},

                                            content=self.metric_card(
                                                title="Expirados",
                                                value="3",
                                                icon=ft.Icons.ERROR,
                                                color="#DC2626"
                                            )
                                        ),

                                        ft.Container(
                                            col={"sm": 12, "md": 6, "xl": 3},

                                            content=self.metric_card(
                                                title="Instituições",
                                                value="48",
                                                icon=ft.Icons.ACCOUNT_BALANCE,
                                                color="#16A34A"
                                            )
                                        ),
                                    ]
                                ),

                                ft.Container(height=40),

                                # TÍTULO TABELA
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                    controls=[

                                        ft.Text(
                                            "Convênios Recentes",
                                            size=24,
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
                                                ),
                                                padding=20
                                            )
                                        )
                                    ]
                                ),

                                ft.Container(height=20),

                                # TABELA
                                self.convenios_table()
                            ]
                        )
                    )
                ]
            )
        ]

    
    # CARD DE MÉTRICA
    

    def metric_card(self, title, value, icon, color):

        return ft.Card(
            elevation=3,

            content=ft.Container(
                padding=25,
                border_radius=20,
                bgcolor="white",

                content=ft.Column(

                    controls=[

                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                            controls=[

                                ft.Container(
                                    padding=12,
                                    border_radius=12,
                                    bgcolor=color,

                                    content=ft.Icon(
                                        icon,
                                        color="white",
                                        size=28
                                    )
                                ),

                                ft.PopupMenuButton(
                                    items=[
                                        ft.PopupMenuItem(content=ft.Text("Detalhes")),
                                        ft.PopupMenuItem(content=ft.Text("Atualizar")),
                                    ]
                                )
                            ]
                        ),

                        ft.Container(height=25),

                        ft.Text(
                            value,
                            size=38,
                            weight=ft.FontWeight.BOLD,
                            color="#111827"
                        ),

                        ft.Text(
                            title,
                            size=14,
                            color="#6B7280"
                        )
                    ]
                )
            )
        )

    
    # TABELA

    def convenios_table(self):

        return ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=20,

            content=ft.Column(
                controls=[

                    ft.DataTable(

                        heading_row_color="#F3F4F6",

                        columns=[

                            ft.DataColumn(
                                ft.Text(
                                    "Instituição",
                                    weight=ft.FontWeight.BOLD
                                )
                            ),

                            ft.DataColumn(
                                ft.Text(
                                    "Responsável",
                                    weight=ft.FontWeight.BOLD
                                )
                            ),

                            ft.DataColumn(
                                ft.Text(
                                    "Vencimento",
                                    weight=ft.FontWeight.BOLD
                                )
                            ),

                            ft.DataColumn(
                                ft.Text(
                                    "Status",
                                    weight=ft.FontWeight.BOLD
                                )
                            ),

                            ft.DataColumn(
                                ft.Text(
                                    "Ações",
                                    weight=ft.FontWeight.BOLD
                                )
                            ),
                        ],

                        rows=[

                            self.create_row(
                                instituicao="Hospital Regional",
                                responsavel="Maria Silva",
                                vencimento="12/08/2026",
                                status="ATIVO"
                            ),

                            self.create_row(
                                instituicao="Prefeitura Municipal",
                                responsavel="Carlos Lima",
                                vencimento="02/06/2026",
                                status="ALERTA"
                            ),

                            self.create_row(
                                instituicao="Clínica São Lucas",
                                responsavel="Fernanda Costa",
                                vencimento="29/05/2026",
                                status="EXPIRADO"
                            ),
                        ]
                    )
                ]
            )
        )

    
    # LINHAS DA TABELA
    

    def create_row(
        self,
        instituicao,
        responsavel,
        vencimento,
        status
    ):

        colors = {
            "ATIVO": "#16A34A",
            "ALERTA": "#F59E0B",
            "EXPIRADO": "#DC2626"
        }

        return ft.DataRow(

            cells=[

                ft.DataCell(
                    ft.Text(instituicao)
                ),

                ft.DataCell(
                    ft.Text(responsavel)
                ),

                ft.DataCell(
                    ft.Text(vencimento)
                ),

                ft.DataCell(

                    ft.Container(
                        bgcolor=colors[status],
                        padding=10,
                        border_radius=30,

                        content=ft.Text(
                            status,
                            color="white",
                            weight=ft.FontWeight.BOLD
                        )
                    )
                ),

                ft.DataCell(

                    ft.Row(
                        spacing=0,

                        controls=[

                            ft.IconButton(
                                icon=ft.Icons.VISIBILITY,
                                icon_color="#2563EB",
                                tooltip="Visualizar"
                            ),

                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color="#F59E0B",
                                tooltip="Editar"
                            ),

                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color="#DC2626",
                                tooltip="Excluir"
                            )
                        ]
                    )
                )
            ]
        )