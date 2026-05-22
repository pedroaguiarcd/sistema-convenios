import flet as ft
import os
import webbrowser
from datetime import date

from backend.database import criar_app_flask
from backend.models.convenio import Convenio

from backend.services.convenio_service import (
    aprovar_convenio,
    cancelar_convenio
)

from backend.services.pdf_service import (
    gerar_termo_convenio
)


app_flask = criar_app_flask()


def tela_gestor(page: ft.Page):

    page.controls.clear()

    titulo = ft.Text(
        "Painel do Gestor",
        size=32,
        weight=ft.FontWeight.BOLD,
        color="#222"
    )

    subtitulo = ft.Text(
        "Solicitações aguardando análise",
        size=15,
        color="#555"
    )

    lista = ft.ListView(
        expand=True,
        spacing=15
    )

    mensagem = ft.Text(
        "",
        color="green"
    )

    alertas = ft.Column(
        spacing=10
    )

    def carregar_alertas_vencimento():

        alertas.controls.clear()

        with app_flask.app_context():

            hoje = date.today()

            convenios = (
                Convenio.query
                .filter(
                    Convenio.data_fim != None,
                    Convenio.status != "pendente"
                )
                .all()
            )

            proximos = []
            vencidos = []

            for convenio in convenios:

                dias_restantes = (convenio.data_fim - hoje).days

                nome_empresa = (
                    convenio.empresa.nome
                    if convenio.empresa
                    else "Empresa não informada"
                )

                if dias_restantes < 0:
                    vencidos.append((convenio, nome_empresa, dias_restantes))

                elif dias_restantes <= 30:
                    proximos.append((convenio, nome_empresa, dias_restantes))

            if not proximos and not vencidos:

                alertas.controls.append(
                    ft.Container(
                        padding=15,
                        border_radius=10,
                        bgcolor="#ECFDF5",
                        content=ft.Text(
                            "✅ Nenhum convênio próximo do vencimento.",
                            color="#065F46",
                            weight=ft.FontWeight.BOLD
                        )
                    )
                )

        for convenio, nome_empresa, dias in vencidos:

            alertas.controls.append(
                ft.Container(
                    padding=15,
                    border_radius=10,
                    bgcolor="#FEE2E2",
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "❌ Convênio vencido",
                                weight=ft.FontWeight.BOLD,
                                color="#991B1B"
                            ),
                            ft.Text(
                                f"{nome_empresa} venceu há {abs(dias)} dias.",
                                color="#7F1D1D"
                            )
                        ]
                    )
                )
            )

        for convenio, nome_empresa, dias in proximos:

            alertas.controls.append(
                ft.Container(
                    padding=15,
                    border_radius=10,
                    bgcolor="#FEF3C7",
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "⚠️ Convênio próximo do vencimento",
                                weight=ft.FontWeight.BOLD,
                                color="#92400E"
                            ),
                            ft.Text(
                                f"{nome_empresa} vence em {dias} dias.",
                                color="#78350F"
                            )
                        ]
                    )
                )
            )

    def voltar(e):

        from frontend.views.convenios import tela_convenios

        tela_convenios(page)


    def carregar_pendentes():

        lista.controls.clear()

        with app_flask.app_context():

            pendentes = (
                Convenio.query
                .filter_by(
                    status="pendente"
                )
                .order_by(
                    Convenio.id.desc()
                )
                .all()
            )

            if not pendentes:

                lista.controls.append(
                    ft.Text(
                        "Nenhuma solicitação pendente."
                    )
                )

            for convenio in pendentes:

                def aprovar(e, convenio_id=convenio.id):

                    with app_flask.app_context():

                        aprovar_convenio(
                            convenio_id
                        )

                    mensagem.value = "Convênio aprovado."
                    mensagem.color = "green"

                    carregar_pendentes()

                def rejeitar(e, convenio_id=convenio.id):

                    motivo = ft.TextField(
                        label="Motivo do cancelamento",
                        width=400
                    )

                    def confirmar(ev):

                        if not motivo.value:

                            mensagem.value = "Informe o motivo."
                            mensagem.color = "red"
                            page.update()
                            return

                        with app_flask.app_context():

                            cancelar_convenio(
                                convenio_id,
                                motivo.value
                            )

                        page.close(dialog)

                        mensagem.value = "Convênio rejeitado."
                        mensagem.color = "red"

                        carregar_pendentes()

                    dialog = ft.AlertDialog(
                        title=ft.Text(
                            "Rejeitar solicitação"
                        ),
                        content=motivo,
                        actions=[
                            ft.Button(
                                "Cancelar",
                                on_click=lambda x:
                                page.close(dialog)
                            ),
                            ft.Button(
                                "Confirmar",
                                on_click=confirmar
                            )
                        ]
                    )

                    page.open(dialog)

                def gerar_pdf(e, convenio_obj=convenio):

                    try:

                        arquivo = gerar_termo_convenio(
                            convenio_obj
                        )

                        mensagem.value = (
                            f"PDF gerado com sucesso: {arquivo}"
                        )

                        mensagem.color = "green"

                    except Exception as erro:

                        mensagem.value = (
                            f"Erro ao gerar PDF: {erro}"
                        )

                        mensagem.color = "red"

                    page.update()

                def abrir_termo(e, convenio_id=convenio.id):

                    caminho = os.path.abspath(
                        f"uploads/termos_gerados/termo_{convenio_id}.pdf"
                    )

                    if os.path.exists(caminho):

                        webbrowser.open(
                            f"file://{caminho}"
                        )

                    else:

                        mensagem.value = "Termo ainda não gerado."
                        mensagem.color = "red"

                        page.update()

                nome_empresa = (
                    convenio.empresa.nome
                    if convenio.empresa
                    else "Empresa não informada"
                )

                card = ft.Container(
                    padding=22,
                    border_radius=12,
                    bgcolor="#FFFFFF",
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                nome_empresa,
                                size=22,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Text(
                                convenio.descricao
                            ),

                            ft.Text(
                                f"Tipo: {convenio.tipo_convenio_formatado}",
                                color="#2563EB",
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Text(
                                f"CNPJ: {convenio.cnpj}"
                            ),

                            ft.Text(
                                f"Responsável: {convenio.responsavel_legal}"
                            ),

                            ft.Text(
                                f"Telefone: {convenio.telefone}"
                            ),

                            ft.Text(
                                f"Documento: {convenio.documento_anexo}"
                                if convenio.documento_anexo
                                else "Documento: não informado"
                            ),

                            ft.Text(
                                f"Vencimento: {convenio.data_fim}"
                            ),

                            ft.Row(
                                controls=[
                                    ft.Button(
                                        "Aprovar",
                                        on_click=aprovar
                                    ),

                                    ft.Button(
                                        "Rejeitar",
                                        on_click=rejeitar
                                    ),

                                    ft.Button(
                                        "Gerar termo",
                                        on_click=gerar_pdf
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

                lista.controls.append(
                    card
                )

        page.update()

    page.add(
    titulo,

    ft.Text(
        "Alertas de vencimento",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#222"
    ),

    alertas,

    ft.Divider(),

    subtitulo,
    mensagem,
    lista,

    ft.Button(
        "Voltar",
        on_click=voltar
    )
)
    carregar_alertas_vencimento()
    carregar_pendentes()