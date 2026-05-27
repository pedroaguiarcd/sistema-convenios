import flet as ft
import os
import webbrowser

from backend.database import criar_app_flask
from backend.models.convenio import Convenio

from frontend.views.solicitar_novo_convenio import (
    tela_solicitar_convenio
)


app_flask = criar_app_flask()


def tela_empresa(page: ft.Page):

    page.controls.clear()

    usuario = page.usuario_logado

    titulo = ft.Text(
        f"Bem-vindo, {usuario.nome}",
        size=28,
        weight=ft.FontWeight.BOLD
    )

    subtitulo = ft.Text(
        "Painel da Empresa",
        size=18,
        color="#555"
    )

    descricao = ft.Text(
        "Solicitações e acompanhamento de convênios"
    )

    info_empresa = ft.Container(
        bgcolor="#FFFFFF",
        border_radius=12,
        padding=12,
        content=ft.Row(
            spacing=12,
            controls=[
                ft.Image(
                    src="assets/brasao_uespi.png",
                    width=42,
                    height=42,
                    fit="contain"
                ),
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(
                            "Empresa Conveniada",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color="#1E3A8A"
                        ),
                        ft.Text(
                            "Universidade Estadual do Piauí - UESPI",
                            size=12,
                            color="#475569"
                        ),
                        ft.Text(
                            "Acesso: empresa",
                            size=11,
                            color="#64748B"
                        )
                    ]
                )
            ]
        )
    )

    cabecalho = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Column(
                spacing=4,
                controls=[
                    titulo,
                    subtitulo,
                    descricao
                ]
            ),
            info_empresa
        ]
    )

    lista = ft.ListView(
        expand=True,
        spacing=12
    )

    def carregar():

        lista.controls.clear()

        with app_flask.app_context():

            convenios = (
                Convenio.query
                .filter_by(
                    empresa_id=usuario.empresa_id,
                    deletado=False
                )
                .filter(
                    Convenio.status != "cancelado"
                )
                .order_by(
                    Convenio.id.desc()
                )
                .all()
            )

            if not convenios:

                lista.controls.append(
                    ft.Text(
                        "Nenhuma solicitação encontrada."
                    )
                )

            for convenio in convenios:

                def abrir_termo(
                    e,
                    convenio_id=convenio.id
                ):

                    caminho = os.path.abspath(
                        f"uploads/termos_gerados/termo_{convenio_id}.pdf"
                    )

                    if os.path.exists(caminho):

                        webbrowser.open(
                            f"file://{caminho}"
                        )

                arquivo_termo = os.path.exists(
                    f"uploads/termos_gerados/termo_{convenio.id}.pdf"
                )

                nome_convenio = (
                    convenio.nome
                    if hasattr(convenio, "nome")
                    and convenio.nome
                    else convenio.descricao
                )

                informacoes = [

                    ft.Text(
                        nome_convenio,
                        size=18,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Text(
                        convenio.descricao,
                        size=13,
                        color="#6B7280"
                    ),

                    ft.Text(
                        f"Tipo: {convenio.tipo_convenio_formatado}",
                        color="#2563EB",
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Text(
                        f"Status: {convenio.status_real}"
                    ),

                    ft.Text(
                        f"CNPJ: {convenio.cnpj}"
                    ),

                    ft.Text(
                        f"Responsável legal: {convenio.responsavel_legal}"
                    ),

                    ft.Text(
                        f"Telefone: {convenio.telefone}"
                    ),

                    ft.Text(
                        f"Endereço: {convenio.endereco}"
                    ),

                    ft.Text(
                        f"Documento: {convenio.documento_anexo}"
                        if convenio.documento_anexo
                        else "Documento: não informado"
                    ),

                    ft.Text(
                        f"Vencimento: {convenio.data_fim}"
                    ),

                    (
                        ft.Button(
                            "Abrir termo",
                            on_click=abrir_termo
                        )
                        if arquivo_termo
                        else ft.Text(
                            "Termo ainda não gerado",
                            color="#D97706"
                        )
                    )
                ]

                lista.controls.append(
                    ft.Container(
                        padding=18,
                        border_radius=10,
                        bgcolor="#FFFFFF",
                        content=ft.Column(
                            spacing=8,
                            controls=informacoes
                        )
                    )
                )

    botao = ft.Button(
        "Solicitar novo convênio",
        on_click=lambda e:
        tela_solicitar_convenio(page)
    )

    page.add(
        ft.Container(
            expand=True,
            padding=18,
            bgcolor="#F4F6F9",
            content=ft.Column(
                spacing=12,
                controls=[
                    cabecalho,
                    botao,
                    ft.Divider(),
                    ft.Text(
                        "Minhas solicitações",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),
                    lista
                ]
            )
        )
    )

    carregar()

    page.update()