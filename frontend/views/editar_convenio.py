import flet as ft

from datetime import datetime

from backend.database import criar_app_flask, db
from backend.models.convenio import Convenio


app_flask = criar_app_flask()


def tela_editar_convenio(page, convenio_id):

    page.controls.clear()

    with app_flask.app_context():

        convenio = Convenio.query.get(
            convenio_id
        )

        descricao_valor = convenio.descricao
        tipo_convenio_valor = convenio.tipo_convenio
        telefone_valor = convenio.telefone
        endereco_valor = convenio.endereco
        responsavel_valor = convenio.responsavel_legal

    titulo = ft.Text(
        "Editar Convênio",
        size=28,
        weight=ft.FontWeight.BOLD
    )

    descricao = ft.TextField(
        label="Descrição",
        value=descricao_valor,
        width=500
    )

    tipo_convenio = ft.Dropdown(
        label="Tipo do convênio",
        width=500,
        value=tipo_convenio_valor,
        options=[
            ft.dropdown.Option("obrigatorio"),
            ft.dropdown.Option("nao_obrigatorio"),
            ft.dropdown.Option("supervisionado"),
        ]
    )

    telefone = ft.TextField(
        label="Telefone",
        value=telefone_valor,
        width=500
    )

    endereco = ft.TextField(
        label="Endereço",
        value=endereco_valor,
        width=500
    )

    responsavel = ft.TextField(
        label="Responsável",
        value=responsavel_valor,
        width=500
    )

    motivo = ft.TextField(
        label="Motivo da alteração",
        width=500
    )

    mensagem = ft.Text(
        "",
        color="green"
    )

    def salvar(e):

        if not motivo.value:

            mensagem.value = "Informe o motivo da alteração."

            mensagem.color = "red"

            page.update()

            return

        campos_alterados = []

        if descricao.value != descricao_valor:

            campos_alterados.append(
                f"Descrição: '{descricao_valor}' → '{descricao.value}'"
            )

        if tipo_convenio.value != tipo_convenio_valor:

            campos_alterados.append(
                f"Tipo do convênio: '{tipo_convenio_valor}' → '{tipo_convenio.value}'"
            )

        if telefone.value != telefone_valor:

            campos_alterados.append(
                f"Telefone: '{telefone_valor}' → '{telefone.value}'"
            )

        if endereco.value != endereco_valor:

            campos_alterados.append(
                f"Endereço: '{endereco_valor}' → '{endereco.value}'"
            )

        if responsavel.value != responsavel_valor:

            campos_alterados.append(
                f"Responsável: '{responsavel_valor}' → '{responsavel.value}'"
            )

        if not campos_alterados:

            mensagem.value = "Nenhum campo foi alterado."

            mensagem.color = "red"

            page.update()

            return

        with app_flask.app_context():

            convenio = Convenio.query.get(
                convenio_id
            )

            convenio.descricao = descricao.value
            convenio.tipo_convenio = tipo_convenio.value
            convenio.telefone = telefone.value
            convenio.endereco = endereco.value
            convenio.responsavel_legal = responsavel.value

            convenio.alterado_em = datetime.now()
            convenio.motivo_alteracao = motivo.value
            convenio.campos_alterados = "\n".join(
                campos_alterados
            )

            db.session.commit()

        mensagem.value = "Alterado com sucesso!"
        mensagem.color = "green"

        page.update()

    def voltar(e):

        from frontend.views.convenios import tela_convenios

        tela_convenios(page)

    page.add(
        titulo,
        descricao,
        tipo_convenio,
        telefone,
        endereco,
        responsavel,
        motivo,
        ft.Row(
            controls=[
                ft.Button(
                    "Salvar",
                    on_click=salvar
                ),
                ft.Button(
                    "Voltar",
                    on_click=voltar
                )
            ]
        ),
        mensagem
    )

    page.update()