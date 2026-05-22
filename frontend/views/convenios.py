import flet as ft

from backend.database import criar_app_flask
from backend.services.convenio_service import listar_convenios
from frontend.components.cards import criar_card_convenio
from backend.models.convenio import Convenio
from datetime import date



app_flask = criar_app_flask()


def tela_convenios(page: ft.Page):

    page.controls.clear()

    filtro_status = "ativo"

    lista = ft.ListView(
        expand=True,
        spacing=18,
        auto_scroll=False
    )

    titulo = ft.Text(
        "Sistema de Gestão de Convênios",
        size=32,
        weight=ft.FontWeight.BOLD,
        color="#1F2937"
    )

    subtitulo = ft.Text(
        "Painel de monitoramento e análise de convênios",
        size=14,
        color="#6B7280"
    )

    notificacao_texto = ft.Text(
        "",
        color="#8A5A00",
        weight=ft.FontWeight.BOLD,
        size=15
    )

    notificacoes_vencimento = ft.Column(
        spacing=10,
        visible=False
)
    def carregar_notificacoes_vencimento():

        notificacoes_vencimento.controls.clear()

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

            alertas = []

            for convenio in convenios:

                dias_restantes = (convenio.data_fim - hoje).days

                if dias_restantes <= 30:

                    nome_empresa = (
                        convenio.empresa.nome
                        if convenio.empresa
                        else "Empresa não informada"
                    )

                    alertas.append(
                        {
                            "empresa": nome_empresa,
                            "dias": dias_restantes,
                            "convenio": convenio
                        }
                    )

            if not alertas:

                notificacoes_vencimento.visible = False
                return

            notificacoes_vencimento.visible = True

            for alerta in alertas:

                if alerta["dias"] < 0:

                    titulo_alerta = "❌ Convênio vencido"
                    mensagem_alerta = (
                        f"{alerta['empresa']} venceu há "
                        f"{abs(alerta['dias'])} dia(s)."
                    )
                    cor_fundo = "#FEE2E2"
                    cor_texto = "#991B1B"

                else:

                    titulo_alerta = "⚠️ Convênio próximo do vencimento"
                    mensagem_alerta = (
                        f"{alerta['empresa']} vence em "
                        f"{alerta['dias']} dia(s)."
                    )
                    cor_fundo = "#FEF3C7"
                    cor_texto = "#92400E"

                notificacoes_vencimento.controls.append(
                    ft.Container(
                        padding=15,
                        border_radius=10,
                        bgcolor=cor_fundo,
                        expand=True,
                        content=ft.Column(
                            spacing=4,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                ft.Text(
                                    titulo_alerta,
                                    weight=ft.FontWeight.BOLD,
                                    color=cor_texto,
                                    size=16
                                ),
                                ft.Text(
                                    mensagem_alerta,
                                    color=cor_texto
                                )
                            ]
                        )
                    )
                )
        

    def abrir_pendentes(e):

        from frontend.views.painel_gestor import tela_gestor

        tela_gestor(page)

    def abrir_historico(e):

        from frontend.views.historico import tela_historico

        tela_historico(page)

    notificacao = ft.Container(
        padding=14,
        border_radius=10,
        bgcolor="#FFF4CC",
        visible=False,
        on_click=abrir_pendentes,

        content=ft.Row(
            controls=[
                ft.Text(
                    "🔔",
                    size=18
                ),

                notificacao_texto,

                ft.Text(
                    "Ver solicitações",
                    color="#1F6FEB",
                    weight=ft.FontWeight.BOLD
                )
            ],

            spacing=10
        )
    )

    def carregar_convenios():

        lista.controls.clear()

        carregar_notificacoes_vencimento()

        with app_flask.app_context():

            pendentes = (
                Convenio.query
                .filter_by(
                    status="pendente"
                )
                .count()
            )

            if pendentes > 0:

                notificacao.visible = True

                notificacao.bgcolor = "#FFF4CC"

                notificacao_texto.value = (
                    f"{pendentes} solicitação(ões) aguardando análise."
                )

            else:

                notificacao.visible = True

                notificacao.bgcolor = "#E7F7E7"

                notificacao_texto.value = (
                    "Nenhuma solicitação pendente."
                )

                notificacao_texto.color = "#1A7F37"

            convenios = listar_convenios(
                filtro_status
            )

            if not convenios:

                lista.controls.append(

                    ft.Container(

                        padding=20,

                        bgcolor="#FFFFFF",

                        border_radius=10,

                        content=ft.Text(
                            "Nenhum convênio encontrado."
                        )
                    )
                )

            for convenio in convenios:

                lista.controls.append(
                    criar_card_convenio(
                    convenio,
                    page,
                    carregar_convenios
                )
                )

        page.update()

    def filtrar(status):

        nonlocal filtro_status

        filtro_status = status

        carregar_convenios()

    filtros = ft.Row(

        controls=[

            ft.Button(
                "Ativos",
                on_click=lambda e:
                filtrar(
                    "ativo"
                )
            ),

            ft.Button(
                "Histórico",
                on_click=abrir_historico
            )

        ],

        spacing=10

    )

    conteudo = ft.Container(

        padding=30,

        bgcolor="#F4F6F9",

        expand=True,

        content=ft.Column(

            controls=[

                titulo,
                subtitulo,
                notificacao,
                notificacoes_vencimento,
                filtros,
                lista

            ],

            spacing=18

        )
    )

    page.add(
        conteudo
    )

    carregar_convenios()