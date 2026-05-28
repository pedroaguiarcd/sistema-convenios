import flet as ft
from datetime import date

from backend.database import criar_app_flask
from frontend.components.cards import criar_card_convenio
from backend.models.convenio import Convenio


app_flask = criar_app_flask()


def tela_convenios(page: ft.Page):

    page.controls.clear()

    filtro_atual = "ativos"

    lista = ft.ListView(
        expand=True,
        spacing=6,
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

    info_gestor = ft.Container(
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
                            "Gestor de Convênios",
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
                            "Administrador institucional",
                            size=11,
                            color="#64748B"
                        )
                    ]
                )
            ]
        )
    )

    busca = ft.TextField(
        hint_text="Buscar convênio, empresa, local ou CNPJ...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        bgcolor="#FFFFFF",
        width=360
    )

    dashboard = ft.Row(
        spacing=10,
        wrap=True
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

    def abrir_pendentes(e):
        from frontend.views.painel_gestor import tela_gestor
        tela_gestor(page)

    def abrir_proximos_vencimento(e):
        nonlocal filtro_atual
        filtro_atual = "proximos"
        carregar_convenios()

    def criar_bloco(titulo_bloco, valor, cor, filtro):
        return ft.Container(
            bgcolor="#FFFFFF",
            border_radius=12,
            padding=15,
            width=170,
            ink=True,
            on_click=lambda e: mudar_filtro(filtro),
            content=ft.Column(
                spacing=2,
                controls=[
                    ft.Text(
                        titulo_bloco,
                        size=12,
                        color="#6B7280"
                    ),
                    ft.Text(
                        str(valor),
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=cor
                    )
                ]
            )
        )

    def mudar_filtro(novo_filtro):
        nonlocal filtro_atual
        filtro_atual = novo_filtro
        carregar_convenios()

    def carregar_notificacoes_vencimento():

        notificacoes_vencimento.controls.clear()

        with app_flask.app_context():

            hoje = date.today()

            convenios = (
                Convenio.query
                .filter(
                    Convenio.data_fim != None,
                    Convenio.status == "ativo",
                    Convenio.deletado == False
                )
                .all()
            )

            proximos = [
                c for c in convenios
                if 1 <= (c.data_fim - hoje).days <= 30
            ]

            if not proximos:
                notificacoes_vencimento.visible = False
                return

            notificacoes_vencimento.visible = True

            notificacoes_vencimento.controls.append(
                ft.Container(
                    padding=14,
                    border_radius=10,
                    bgcolor="#FEF3C7",
                    ink=True,
                    on_click=abrir_proximos_vencimento,
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text(
                                "⚠️ Convênios próximos do vencimento",
                                weight=ft.FontWeight.BOLD,
                                color="#92400E"
                            ),
                            ft.Text(
                                f"{len(proximos)} convênio(s) próximos do vencimento",
                                color="#92400E"
                            )
                        ]
                    )
                )
            )

    notificacao = ft.Container(
        padding=14,
        border_radius=10,
        bgcolor="#FFF4CC",
        visible=False,
        on_click=abrir_pendentes,
        content=ft.Row(
            controls=[
                ft.Text("🔔"),
                notificacao_texto,
                ft.Text(
                    "Ver solicitações",
                    color="#2563EB",
                    weight=ft.FontWeight.BOLD
                )
            ]
        )
    )

    def carregar_convenios(e=None):

        lista.controls.clear()
        dashboard.controls.clear()

        carregar_notificacoes_vencimento()

        with app_flask.app_context():

            todos = (
                Convenio.query
                .filter(
                    Convenio.deletado == False
                )
                .all()
            )

            excluidos = (
                Convenio.query
                .filter(
                    Convenio.deletado == True
                )
                .all()
            )

            ativos = [
                c for c in todos
                if c.status_real == "ativo"
            ]

            vencidos = [
                c for c in todos
                if c.status_real == "vencido"
            ]

            proximos = [
                c for c in ativos
                if c.dias_para_vencer is not None
                and 0 <= c.dias_para_vencer <= 30
            ]

            cancelados = [
                c for c in todos
                if c.status_real == "cancelado"
            ]

            alterados = [
                c for c in todos
                if c.alterado_em is not None
            ]

            pendentes = (
                Convenio.query
                .filter_by(status="pendente")
                .count()
            )

            if pendentes > 0:
                notificacao.visible = True
                notificacao.bgcolor = "#FFF4CC"
                notificacao_texto.value = (
                    f"{pendentes} solicitação(ões) de convênios aguardando análise."
                )
                notificacao_texto.color = "#8A5A00"
            else:
                notificacao.visible = True
                notificacao.bgcolor = "#E7F7E7"
                notificacao_texto.value = "Nenhuma solicitação pendente."
                notificacao_texto.color = "#1A7F37"

            dashboard.controls.extend([
                criar_bloco(
                    "Convênios",
                    len(todos),
                    "#2563EB",
                    "todos"
                ),
                criar_bloco(
                    "Ativos",
                    len(ativos),
                    "#16A34A",
                    "ativos"
                ),
                criar_bloco(
                    "Vencidos",
                    len(vencidos),
                    "#DC2626",
                    "vencidos"
                ),
                criar_bloco(
                    "Próximos",
                    len(proximos),
                    "#D97706",
                    "proximos"
                ),
                criar_bloco(
                    "Cancelados",
                    len(cancelados),
                    "#6B7280",
                    "cancelados"
                ),
                criar_bloco(
                    "Alterados",
                    len(alterados),
                    "#7C3AED",
                    "alterados"
                ),
                criar_bloco(
                    "Excluídos",
                    len(excluidos),
                    "#991B1B",
                    "excluidos"
                )
            ])

            if filtro_atual == "todos":
                convenios = todos

            elif filtro_atual == "ativos":
                convenios = ativos

            elif filtro_atual == "vencidos":
                convenios = vencidos

            elif filtro_atual == "proximos":
                convenios = proximos

            elif filtro_atual == "cancelados":
                convenios = cancelados

            elif filtro_atual == "alterados":
                convenios = alterados

            elif filtro_atual == "excluidos":
                convenios = excluidos

            else:
                convenios = ativos

            texto = busca.value.lower().strip()

            if texto:
                convenios = [
                    c for c in convenios
                    if (
                        texto in (c.descricao or "").lower()
                        or texto in (c.endereco or "").lower()
                        or texto in (c.cnpj or "").lower()
                        or (
                            c.empresa
                            and texto in (c.empresa.nome or "").lower()
                        )
                    )
                ]

            convenios.sort(
                key=lambda c: (
                    c.data_fim is None,
                    c.data_fim
                )
            )

            if not convenios:
                lista.controls.append(
                    ft.Container(
                        padding=16,
                        bgcolor="#FFFFFF",
                        border_radius=10,
                        content=ft.Text("Nenhum convênio encontrado.")
                    )
                )

            for i, convenio in enumerate(
                convenios,
                start=1
            ):
                lista.controls.append(
                    criar_card_convenio(
                        convenio,
                        page,
                        carregar_convenios,
                        numero=i
                    )
                )

        page.update()

    busca.on_change = carregar_convenios

    avisos = ft.Row(
        spacing=12,
        controls=[
            ft.Container(
                expand=1,
                content=notificacao
            ),
            ft.Container(
                expand=1,
                content=notificacoes_vencimento
            )
        ]
    )

    cabecalho = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Column(
                spacing=4,
                controls=[
                    titulo,
                    subtitulo
                ]
            ),
            info_gestor
        ]
    )

    conteudo = ft.Container(
        expand=True,
        padding=18,
        bgcolor="#F4F6F9",
        content=ft.Column(
            spacing=10,
            controls=[
                cabecalho,
                avisos,
                dashboard,
                busca,
                lista
            ]
        )
    )

    page.add(conteudo)

    carregar_convenios()