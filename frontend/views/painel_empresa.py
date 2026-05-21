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
                    empresa_id=usuario.empresa_id
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


                informacoes = [

                    ft.Text(
                        convenio.descricao,
                        size=18,
                        weight=ft.FontWeight.BOLD
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

                    ft.Button(
                        "Abrir termo",
                        on_click=abrir_termo
                    )

                    if arquivo_termo

                    else ft.Text(
                        "Termo ainda não gerado",
                        color="#D97706"
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
        titulo,
        subtitulo,
        descricao,
        botao,
        ft.Divider(),
        ft.Text(
            "Minhas solicitações",
            size=20,
            weight=ft.FontWeight.BOLD
        ),
        lista
    )

    carregar()

    page.update()