import flet as ft
from styles.theme import (
    SURFACE, SURFACE_2, BORDER, TEXT_PRIMARY, TEXT_SECONDARY,
    TEXT_MUTED, DANGER, WARNING, SUCCESS, status_badge, STATUS_COLORS
)


class CriticalTable(ft.UserControl):
    def __init__(self, convenios: list):
        super().__init__()
        self.convenios = convenios

    def build(self):
        if not self.convenios:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, color=SUCCESS, size=40),
                    ft.Text("Nenhum convênio crítico.", color=TEXT_SECONDARY, size=14),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                alignment=ft.alignment.center,
                padding=40,
            )

        header = ft.Container(
            content=ft.Row([
                ft.Text("Empresa", size=11, color=TEXT_MUTED, weight=ft.FontWeight.W_600, expand=3),
                ft.Text("Tipo", size=11, color=TEXT_MUTED, weight=ft.FontWeight.W_600, expand=2),
                ft.Text("Vencimento", size=11, color=TEXT_MUTED, weight=ft.FontWeight.W_600, expand=2),
                ft.Text("Dias", size=11, color=TEXT_MUTED, weight=ft.FontWeight.W_600, expand=1),
                ft.Text("Status", size=11, color=TEXT_MUTED, weight=ft.FontWeight.W_600, expand=2),
            ]),
            padding=ft.padding.symmetric(horizontal=16, vertical=10),
            bgcolor=SURFACE_2,
            border_radius=ft.border_radius.only(top_left=8, top_right=8),
            border=ft.border.only(bottom=ft.BorderSide(1, BORDER)),
        )

        rows = []
        for i, c in enumerate(self.convenios):
            dias = c.get("dias_restantes", 0)
            status = c.get("status", "")
            color = STATUS_COLORS.get(status, TEXT_SECONDARY)
            dias_text = str(dias) if dias >= 0 else f"{abs(dias)}d atrás"
            dias_color = DANGER if dias < 0 else (WARNING if dias <= 30 else SUCCESS)

            bg = "#1A0A0A" if i % 2 == 0 else "transparent"

            rows.append(ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(c.get("nome_empresa", ""), size=13, color=TEXT_PRIMARY,
                                weight=ft.FontWeight.W_500, no_wrap=True),
                        ft.Text(c.get("responsavel", ""), size=11, color=TEXT_MUTED),
                    ], expand=3, spacing=2),
                    ft.Text(c.get("tipo_convenio", ""), size=12, color=TEXT_SECONDARY, expand=2),
                    ft.Text(
                        c.get("data_vencimento", "")[:10] if c.get("data_vencimento") else "",
                        size=12, color=TEXT_SECONDARY, expand=2
                    ),
                    ft.Container(
                        content=ft.Text(dias_text, size=12, color=dias_color, weight=ft.FontWeight.W_600),
                        expand=1,
                    ),
                    ft.Container(content=status_badge(status), expand=2),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                bgcolor=bg,
            ))

        return ft.Column([header] + rows, spacing=0)
