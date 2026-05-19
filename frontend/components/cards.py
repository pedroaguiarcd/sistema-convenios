import flet as ft


def cor_card(convenio):
    if convenio.status_real == "vencido":
        return "#FFE5E5"

    if convenio.status_real == "pendente":
        return "#FFF4CC"

    return "#FFFFFF"


def criar_card_convenio(convenio):
    return ft.Container(
        width=560,
        bgcolor=cor_card(convenio),
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color="#00000022",
            offset=ft.Offset(0, 2),
        ),
        content=ft.Column(
            controls=[
                ft.Text(
                    convenio.descricao,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#222"
                ),

                ft.Text(
                    f"Responsável: {convenio.responsavel_legal}",
                    color="#333"
                ),

                ft.Text(
                    f"CNPJ: {convenio.cnpj}",
                    color="#333"
                ),

                ft.Text(
                    f"Telefone: {convenio.telefone}",
                    color="#333"
                ),

                ft.Text(
                    f"Vencimento: {convenio.data_fim}",
                    color="#333"
                ),

                ft.Text(
                    f"Status: {convenio.status_real}",
                    color="#222",
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    f"Dias para vencer: {convenio.dias_para_vencer}",
                    color="#333"
                ),
            ]
        )
    )