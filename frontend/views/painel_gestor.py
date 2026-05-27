import flet as ft
import os
import webbrowser
from datetime import date

from backend.database import criar_app_flask, db
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

    def voltar(e):

        from frontend.views.convenios import tela_convenios

        tela_convenios(page)

    def carregar_pendentes():

        lista.controls.clear()

        with app_flask.app_context():

            pendentes = (
                Convenio.query
                .filter_by(status="pendente")
                .order_by(Convenio.id.desc())
                .all()
            )

            if not pendentes:

                lista.controls.append(
                    ft.Text("Nenhuma solicitação pendente.")
                )

            for convenio in pendentes:

                def aprovar(e, convenio_id=convenio.id):

                    data_fim_escolhida = {
                        "valor": None
                    }

                    texto_data = ft.Text(
                        "Nenhuma data selecionada.",
                        color="#6B7280"
                    )

                    mensagem_dialog = ft.Text(
                        "",
                        color="red"
                    )

                    def selecionar_data(ev):

                        if ev.control.value:

                            data_fim_escolhida["valor"] = (
                                ev.control.value.date()
                            )

                            texto_data.value = (
                                f"Data de vencimento: "
                                f"{data_fim_escolhida['valor'].strftime('%d/%m/%Y')}"
                            )

                            page.update()

                    calendario = ft.DatePicker(
                        on_change=selecionar_data
                    )

                    page.overlay.append(calendario)

                    def abrir_calendario(ev):

                        calendario.open = True

                        page.update()

                    def fechar_dialog():

                        dialog.open = False

                        page.update()

                    def confirmar_aprovacao(ev):

                        if not data_fim_escolhida["valor"]:

                            mensagem_dialog.value = (
                                "Selecione a data de vencimento do convênio."
                            )

                            page.update()

                            return

                        if data_fim_escolhida["valor"] <= date.today():

                            mensagem_dialog.value = (
                                "A data de vencimento deve ser futura."
                            )

                            page.update()

                            return

                        with app_flask.app_context():

                            convenio_banco = Convenio.query.get(
                                convenio_id
                            )

                            convenio_banco.data_fim = (
                                data_fim_escolhida["valor"]
                            )

                            db.session.commit()

                            aprovar_convenio(
                                convenio_id
                            )

                        fechar_dialog()

                        mensagem.value = (
                            "Convênio aprovado com data de vencimento definida."
                        )

                        mensagem.color = "green"

                        carregar_pendentes()

                    dialog = ft.AlertDialog(
                        title=ft.Text(
                            "Definir data de vencimento"
                        ),
                        content=ft.Column(
                            tight=True,
                            spacing=12,
                            controls=[
                                ft.Text(
                                    "Antes de aprovar, informe a data de vencimento do convênio."
                                ),
                                texto_data,
                                ft.Button(
                                    "Selecionar data de vencimento",
                                    on_click=abrir_calendario
                                ),
                                mensagem_dialog
                            ]
                        ),
                        actions=[
                            ft.Button(
                                "Cancelar",
                                on_click=lambda ev: fechar_dialog()
                            ),
                            ft.Button(
                                "Aprovar",
                                on_click=confirmar_aprovacao
                            )
                        ]
                    )

                    page.overlay.append(dialog)

                    dialog.open = True

                    page.update()

                def rejeitar(e, convenio_id=convenio.id):

                    motivo = ft.TextField(
                        label="Motivo do cancelamento",
                        width=400
                    )

                    def fechar_dialog():

                        dialog.open = False

                        page.update()

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

                        fechar_dialog()

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
                                on_click=lambda x: fechar_dialog()
                            ),

                            ft.Button(
                                "Confirmar",
                                on_click=confirmar
                            )

                        ]

                    )

                    page.overlay.append(
                        dialog
                    )

                    dialog.open = True

                    page.update()

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

                def abrir_documento(e, convenio_obj=convenio):

                    if not convenio_obj.arquivo_documento:

                        mensagem.value = "Nenhum documento anexado."
                        mensagem.color = "red"

                        page.update()

                        return

                    caminho = os.path.abspath(
                        convenio_obj.arquivo_documento
                    )

                    if os.path.exists(caminho):

                        webbrowser.open(
                            f"file://{caminho}"
                        )

                    else:

                        mensagem.value = (
                            "Arquivo do documento não encontrado."
                        )

                        mensagem.color = "red"

                        page.update()

                nome_empresa = (
                    convenio.empresa.nome
                    if convenio.empresa
                    else "Empresa não informada"
                )

                data_vencimento = (
                    convenio.data_fim.strftime("%d/%m/%Y")
                    if convenio.data_fim
                    else "Aguardando definição pelo gestor"
                )

                card = ft.Container(
                    padding=22,
                    border_radius=12,
                    bgcolor="#FFFFFF",
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                convenio.nome if convenio.nome else convenio.descricao,
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
                                f"Vencimento: {data_vencimento}"
                            ),

                            ft.Row(
                                wrap=True,
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
                                    ),

                                    ft.Button(
                                        "Abrir documento",
                                        on_click=abrir_documento
                                    )
                                ]
                            )
                        ]
                    )
                )

                lista.controls.append(card)

        page.update()

    page.add(
        titulo,
        subtitulo,
        mensagem,
        lista,

        ft.Button(
            "Voltar",
            on_click=voltar
        )
    )

    carregar_pendentes()