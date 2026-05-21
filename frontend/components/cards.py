import flet as ft

import os
import webbrowser

from backend.services.pdf_service import gerar_termo_convenio

from backend.database import criar_app_flask
from backend.services.convenio_service import excluir_convenio

from frontend.views.editar_convenio import tela_editar_convenio


app_flask = criar_app_flask()


def cor_status(convenio):

    if convenio.status_real == "vencido":
        return "#DC2626"

    if convenio.status_real == "pendente":
        return "#D97706"

    if convenio.status_real == "cancelado":
        return "#6B7280"

    return "#16A34A"


def texto_status(convenio):

    if convenio.status_real == "vencido":
        return "Vencido"

    if convenio.status_real == "pendente":
        return "Pendente"

    if convenio.status_real == "cancelado":
        return "Cancelado"

    return "Ativo"


def criar_card_convenio(
    convenio,
    page=None,
    atualizar=None
):

    nome_empresa = "Empresa não informada"

    if convenio.empresa:
        nome_empresa = convenio.empresa.nome

    def editar(e):

        tela_editar_convenio(
            page,
            convenio.id
        )

    def excluir(e):

        motivo = ft.TextField(
            label="Motivo da exclusão",
            width=400
        )

        def confirmar(ev):

            if not motivo.value:
                return

            with app_flask.app_context():

                excluir_convenio(
                    convenio.id,
                    motivo.value
                )

            page.close(dialog)

            if atualizar:
                atualizar()

        dialog = ft.AlertDialog(

            title=ft.Text(
                "Confirmar exclusão"
            ),

            content=motivo,

            actions=[

                ft.Button(
                    "Cancelar",
                    on_click=lambda ev:
                    page.close(dialog)
                ),

                ft.Button(
                    "Confirmar",
                    on_click=confirmar
                )

            ]

        )

        page.open(dialog)

    def gerar_termo(e):

        gerar_termo_convenio(
            convenio
        )

        if atualizar:
            atualizar()

    def abrir_termo(e):

        caminho = os.path.abspath(
            f"uploads/termos_gerados/termo_{convenio.id}.pdf"
        )

        if os.path.exists(caminho):

            webbrowser.open(
                f"file://{caminho}"
            )

    informacoes_historico = []

    if convenio.alterado_em:

        informacoes_historico.append(

            ft.Text(
                f"Alterado em: {convenio.alterado_em}",
                color="#6B7280"
            )

        )

    if convenio.motivo_alteracao:

        informacoes_historico.append(

            ft.Text(
                f"Motivo da alteração: {convenio.motivo_alteracao}",
                color="#6B7280"
            )

        )

    if convenio.excluido_em:

        informacoes_historico.append(

            ft.Text(
                f"Excluído em: {convenio.excluido_em}",
                color="#6B7280"
            )

        )

    if convenio.motivo_exclusao:

        informacoes_historico.append(

            ft.Text(
                f"Motivo da exclusão: {convenio.motivo_exclusao}",
                color="#6B7280"
            )

        )

    if convenio.data_cancelamento:

        informacoes_historico.append(

            ft.Text(
                f"Cancelado em: {convenio.data_cancelamento}",
                color="#6B7280"
            )

        )

    if convenio.motivo_cancelamento:

        informacoes_historico.append(

            ft.Text(
                f"Motivo do cancelamento: {convenio.motivo_cancelamento}",
                color="#6B7280"
            )

        )

    if convenio.campos_alterados:

        informacoes_historico.append(

            ft.Text(
                f"Campos alterados:\n{convenio.campos_alterados}",
                color="#6B7280"
            )

        )

    return ft.Container(

        bgcolor="#FFFFFF",

        padding=24,

        border_radius=14,

        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color="#00000018",
            offset=ft.Offset(0, 4),
        ),

        content=ft.Column(

            spacing=12,

            controls=[

                ft.Row(

                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                    controls=[

                        ft.Text(
                            nome_empresa,
                            size=22,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            texto_status(
                                convenio
                            ),

                            color=cor_status(
                                convenio
                            ),

                            weight=ft.FontWeight.BOLD
                        )

                    ]

                ),

                ft.Text(
                    convenio.descricao
                ),

                ft.Text(
                    f"Tipo: {convenio.tipo_convenio_formatado}",
                    color="#2563EB",
                    weight=ft.FontWeight.BOLD
                ),

                ft.Divider(),

                ft.Text(
                    f"Responsável: {convenio.responsavel_legal}"
                ),

                ft.Text(
                    f"CNPJ: {convenio.cnpj}"
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

                ft.Text(
                    f"Dias restantes: {convenio.dias_para_vencer}",
                    color=cor_status(
                        convenio
                    )
                ),

                *informacoes_historico,

                ft.Divider(),

                ft.Row(

                    alignment=ft.MainAxisAlignment.END,

                    controls=[

                        ft.Button(
                            "Editar",
                            on_click=editar
                        ),

                        ft.Button(
                            "Excluir",
                            on_click=excluir
                        ),

                        ft.Button(
                            "Gerar termo",
                            on_click=gerar_termo
                        ),

                        ft.Button(
                            "Abrir termo",
                            on_click=abrir_termo
                        )

                    ]

                )

            ]

        )

    )