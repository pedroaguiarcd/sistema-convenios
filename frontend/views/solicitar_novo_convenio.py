import flet as ft

import os

from backend.database import criar_app_flask, db
from backend.models.empresa import Empresa
from backend.services.convenio_service import criar_convenio


app_flask = criar_app_flask()


def tela_solicitar_convenio(page: ft.Page):

    page.controls.clear()

    arquivo_nome = ""
    arquivo_bytes = None

    titulo = ft.Text(
        "Solicitar Novo Convênio",
        size=28,
        weight=ft.FontWeight.BOLD,
        color="#222"
    )

    nome_empresa = ft.TextField(
        label="Nome da empresa",
        width=500
    )

    descricao = ft.TextField(
        label="Descrição do convênio",
        width=500
    )

    tipo_convenio = ft.Dropdown(
        label="Tipo do convênio",
        width=500,
        value="supervisionado",
        options=[
            ft.dropdown.Option("obrigatorio"),
            ft.dropdown.Option("nao_obrigatorio"),
            ft.dropdown.Option("supervisionado"),
        ]
    )

    data_fim = ft.TextField(
        label="Data de fim",
        width=500,
        read_only=True
    )

    responsavel = ft.TextField(
        label="Responsável legal",
        width=500
    )

    telefone = ft.TextField(
        label="Telefone",
        width=500
    )

    cnpj = ft.TextField(
        label="CNPJ",
        width=500
    )

    endereco = ft.TextField(
        label="Endereço",
        width=500
    )

    texto_documento = ft.Text(
        "Nenhum documento selecionado",
        color="#555"
    )

    mensagem = ft.Text(
        "",
        color="green"
    )

    async def selecionar_documento(e):

        nonlocal arquivo_nome
        nonlocal arquivo_bytes

        resultado = await ft.FilePicker().pick_files(
            allow_multiple=False,
            with_data=True
        )

        if resultado:

            arquivo = resultado[0]

            arquivo_nome = arquivo.name

            arquivo_bytes = arquivo.bytes

            texto_documento.value = (
                f"Documento selecionado: {arquivo_nome}"
            )

            page.update()

    def abrir_calendario_fim(e):

        def selecionar(ev):

            if ev.control.value:

                data_fim.value = str(
                    ev.control.value.date()
                )

                page.update()

        calendario = ft.DatePicker(
            on_change=selecionar
        )

        page.overlay.append(
            calendario
        )

        calendario.open = True

        page.update()

    def salvar(e):

        nonlocal arquivo_nome
        nonlocal arquivo_bytes

        if (
            not nome_empresa.value
            or not descricao.value
            or not tipo_convenio.value
            or not data_fim.value
            or not cnpj.value
        ):

            mensagem.value = (
                "Preencha nome da empresa, descrição, tipo, data de fim e CNPJ."
            )

            mensagem.color = "red"

            page.update()

            return

        try:

            arquivo_salvo = None
            nome_documento = ""

            if arquivo_nome and arquivo_bytes:

                os.makedirs(
                    "uploads/documentos",
                    exist_ok=True
                )

                nome_documento = arquivo_nome.replace(
                    " ",
                    "_"
                )

                destino = os.path.join(
                    "uploads",
                    "documentos",
                    nome_documento
                )

                with open(destino, "wb") as arquivo_final:

                    arquivo_final.write(
                        arquivo_bytes
                    )

                arquivo_salvo = destino

            with app_flask.app_context():

                empresa = Empresa.query.filter_by(
                    cnpj=cnpj.value
                ).first()

                if not empresa:

                    empresa = Empresa(
                        nome=nome_empresa.value,
                        cnpj=cnpj.value,
                        email="",
                        telefone=telefone.value
                    )

                    db.session.add(
                        empresa
                    )

                    db.session.commit()

                criar_convenio(
                    empresa_id=empresa.id,
                    descricao=descricao.value,
                    tipo_convenio=tipo_convenio.value,
                    data_fim=data_fim.value,
                    telefone=telefone.value,
                    cnpj=cnpj.value,
                    endereco=endereco.value,
                    responsavel_legal=responsavel.value,
                    documento_anexo=nome_documento,
                    arquivo_documento=arquivo_salvo
                )

            mensagem.value = "Solicitação enviada com sucesso!"
            mensagem.color = "green"

            nome_empresa.value = ""
            descricao.value = ""
            tipo_convenio.value = "supervisionado"
            data_fim.value = ""
            responsavel.value = ""
            telefone.value = ""
            cnpj.value = ""
            endereco.value = ""

            arquivo_nome = ""
            arquivo_bytes = None
            texto_documento.value = "Nenhum documento selecionado"

            page.update()

        except Exception as erro:

            mensagem.value = f"Erro ao salvar: {erro}"
            mensagem.color = "red"

            page.update()

    def voltar(e):

        from frontend.views.painel_empresa import tela_empresa

        tela_empresa(page)

    botao_data_fim = ft.Button(
        "Selecionar data de fim",
        on_click=abrir_calendario_fim
    )

    botao_documento = ft.Button(
        "Selecionar documento",
        on_click=selecionar_documento
    )

    botao_salvar = ft.Button(
        "Enviar solicitação",
        on_click=salvar
    )

    botao_voltar = ft.Button(
        "Voltar",
        on_click=voltar
    )

    page.add(
        titulo,
        nome_empresa,
        descricao,
        tipo_convenio,
        ft.Row(
            controls=[
                data_fim,
                botao_data_fim
            ]
        ),
        responsavel,
        telefone,
        cnpj,
        endereco,
        botao_documento,
        texto_documento,
        ft.Row(
            controls=[
                botao_salvar,
                botao_voltar
            ]
        ),
        mensagem
    )

    page.update()