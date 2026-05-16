import flet as ft
import threading
from services import api
from styles.theme import (
    SURFACE, SURFACE_2, BORDER, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    ACCENT, SUCCESS, WARNING, DANGER, section_title
)


class MonitoramentoPage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self._logs = []
        self._running = False

    def build(self):
        self._status_text = ft.Text("", size=13, color=SUCCESS)
        self._run_btn = ft.ElevatedButton(
            "Executar Monitoramento Agora",
            icon=ft.icons.PLAY_ARROW,
            on_click=self._run,
            bgcolor=ACCENT,
            color="#FFFFFF",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        )
        self._logs_col = ft.Column(spacing=8)

        threading.Thread(target=self._load_logs, daemon=True).start()

        return ft.Column([
            ft.Row([section_title("Monitoramento", "Agente automatizado de verificação de convênios")]),
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.SMART_TOY_OUTLINED, color=ACCENT, size=28),
                        ft.Column([
                            ft.Text("Agente de Monitoramento Preventivo", size=15, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                            ft.Text("Verifica e atualiza automaticamente o status de todos os convênios.", size=12, color=TEXT_SECONDARY),
                        ], spacing=2),
                    ], spacing=12),
                    ft.Divider(height=1, color=BORDER),
                    ft.Row([
                        self._run_btn,
                        self._status_text,
                    ], spacing=16),
                    ft.Text("Regras de status:", size=12, color=TEXT_MUTED, weight=ft.FontWeight.W_600),
                    ft.Row([
                        ft.Container(
                            content=ft.Text("🟢 Vigente — mais de 30 dias", size=12, color=TEXT_SECONDARY),
                            bgcolor=SURFACE_2, border_radius=6, padding=ft.padding.symmetric(8, 6),
                        ),
                        ft.Container(
                            content=ft.Text("🟡 Próximo — ≤ 30 dias", size=12, color=TEXT_SECONDARY),
                            bgcolor=SURFACE_2, border_radius=6, padding=ft.padding.symmetric(8, 6),
                        ),
                        ft.Container(
                            content=ft.Text("🔴 Vencido — data expirada", size=12, color=TEXT_SECONDARY),
                            bgcolor=SURFACE_2, border_radius=6, padding=ft.padding.symmetric(8, 6),
                        ),
                    ], spacing=8),
                ], spacing=16),
                bgcolor=SURFACE,
                border_radius=10,
                padding=20,
                border=ft.border.all(1, BORDER),
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Histórico de Execuções", size=14, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                    ft.Divider(height=1, color=BORDER),
                    self._logs_col,
                ], spacing=12),
                bgcolor=SURFACE,
                border_radius=10,
                padding=20,
                border=ft.border.all(1, BORDER),
            ),
        ], spacing=20, scroll=ft.ScrollMode.AUTO, expand=True)

    def _run(self, e):
        self._run_btn.disabled = True
        self._status_text.value = "Executando..."
        self._status_text.color = WARNING
        self.update()

        def _do():
            resp = api.executar_monitoramento()
            data = resp.get("data", {})
            msg = (
                f"✓ {data.get('total_verificados', 0)} verificados, "
                f"{data.get('total_atualizados', 0)} atualizados, "
                f"{data.get('vencidos', 0)} vencidos, "
                f"{data.get('proximos_vencimento', 0)} próximos."
            )
            self._status_text.value = msg
            self._status_text.color = SUCCESS
            self._run_btn.disabled = False
            self._load_logs()

        threading.Thread(target=_do, daemon=True).start()

    def _load_logs(self):
        resp = api.get_logs_monitoramento(10)
        self._logs = resp.get("data", [])
        if self.page:
            self.page.run_thread(self._render_logs)

    def _render_logs(self):
        self._logs_col.controls = []

        if not self._logs:
            self._logs_col.controls.append(
                ft.Text("Nenhuma execução registrada ainda.", color=TEXT_MUTED, size=13)
            )
        else:
            for log in self._logs:
                ts = (log.get("executado_em") or "")[:16].replace("T", " ")
                self._logs_col.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.HISTORY, color=ACCENT, size=16),
                            ft.Column([
                                ft.Text(f"Executado em {ts}", size=12, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                                ft.Text(
                                    f"{log.get('total_verificados', 0)} verificados  ·  "
                                    f"{log.get('vigentes', 0)} vigentes  ·  "
                                    f"{log.get('proximos_vencimento', 0)} próximos  ·  "
                                    f"{log.get('vencidos', 0)} vencidos",
                                    size=11, color=TEXT_SECONDARY,
                                ),
                            ], spacing=2),
                        ], spacing=10),
                        bgcolor=SURFACE_2,
                        border_radius=8,
                        padding=ft.padding.symmetric(horizontal=14, vertical=10),
                        border=ft.border.all(1, BORDER),
                    )
                )
        self.update()
