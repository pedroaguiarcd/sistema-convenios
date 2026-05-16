import flet as ft
import threading
from services import api
from components.metric_card import MetricCard
from components.critical_table import CriticalTable
from styles.theme import (
    DARK_BG, SURFACE, BORDER, TEXT_PRIMARY, TEXT_SECONDARY,
    TEXT_MUTED, ACCENT, SUCCESS, WARNING, DANGER, SURFACE_2,
    section_title, card
)


class DashboardPage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self._metrics = {}
        self._criticos = []
        self._loading = True
        self._error = None

    def build(self):
        self._container = ft.Column(
            [ft.Container(
                content=ft.ProgressRing(color=ACCENT),
                alignment=ft.alignment.center,
                expand=True,
            )],
            expand=True,
        )
        threading.Thread(target=self._load_data, daemon=True).start()
        return self._container

    def _load_data(self):
        metrics_resp = api.get_metrics()
        criticos_resp = api.get_critical(15)

        self._metrics = metrics_resp.get("data", {})
        self._criticos = criticos_resp.get("data", [])
        self._loading = False

        if self.page:
            self.page.run_thread(self._render)

    def _render(self):
        m = self._metrics
        total = m.get("total", 0)
        vigentes = m.get("vigentes", 0)
        proximos = m.get("proximos_vencimento", 0)
        vencidos = m.get("vencidos", 0)
        ultima_att = m.get("ultima_atualizacao", "Nunca") or "Nunca"
        if ultima_att and ultima_att != "Nunca":
            ultima_att = ultima_att[:16].replace("T", " ")

        metrics_row = ft.Row(
            [
                MetricCard("Total de Convênios", str(total), "cadastros ativos", ACCENT, ft.icons.FOLDER_COPY_OUTLINED),
                MetricCard("Vigentes", str(vigentes), f"{m.get('percentual_vigentes', 0)}% do total", SUCCESS, ft.icons.CHECK_CIRCLE_OUTLINE),
                MetricCard("Próximos do Vencimento", str(proximos), "≤ 30 dias", WARNING, ft.icons.SCHEDULE),
                MetricCard("Vencidos", str(vencidos), "requerem ação", DANGER, ft.icons.WARNING_AMBER_OUTLINED),
            ],
            spacing=16,
        )

        criticos_section = ft.Container(
            content=ft.Column([
                ft.Row([
                    section_title("Painel de Criticidade", "Convênios que requerem atenção imediata"),
                    ft.Container(expand=True),
                    ft.Text(f"Última atualização: {ultima_att}", size=11, color=TEXT_MUTED),
                ]),
                ft.Divider(height=1, color=BORDER),
                CriticalTable(self._criticos),
            ], spacing=16),
            bgcolor=SURFACE,
            border_radius=10,
            padding=20,
            border=ft.border.all(1, BORDER),
        )

        self._container.controls = [
            ft.Column([
                ft.Row([
                    section_title("Dashboard", "Visão geral dos convênios"),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        "Executar Monitoramento",
                        icon=ft.icons.SYNC,
                        on_click=self._run_monitoring,
                        bgcolor=ACCENT,
                        color="#FFFFFF",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    ),
                ]),
                metrics_row,
                criticos_section,
            ], spacing=24, scroll=ft.ScrollMode.AUTO, expand=True),
        ]
        self.update()

    def _run_monitoring(self, e):
        e.control.disabled = True
        e.control.text = "Executando..."
        self.update()

        def _do():
            api.executar_monitoramento()
            self._load_data()
            e.control.disabled = False
            e.control.text = "Executar Monitoramento"

        threading.Thread(target=_do, daemon=True).start()
