import flet as ft
from styles.theme import SURFACE, BORDER, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT


class MetricCard(ft.UserControl):
    def __init__(self, title: str, value: str, subtitle: str = "", color: str = ACCENT, icon=None):
        super().__init__()
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.color = color
        self.icon = icon

    def build(self):
        return ft.Container(
            expand=True,
            bgcolor=SURFACE,
            border_radius=10,
            padding=20,
            border=ft.border.all(1, BORDER),
            content=ft.Column([
                ft.Row([
                    ft.Text(self.title, size=12, color=TEXT_SECONDARY, weight=ft.FontWeight.W_500),
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Icon(self.icon or ft.icons.INFO_OUTLINE, color=self.color, size=16),
                        bgcolor=f"#{self.color.lstrip('#')}22" if self.color.startswith("#") else None,
                        border_radius=6,
                        padding=6,
                    ) if self.icon else ft.Container(),
                ]),
                ft.Text(self.value, size=32, weight=ft.FontWeight.W_700, color=TEXT_PRIMARY),
                ft.Text(self.subtitle, size=12, color=TEXT_SECONDARY) if self.subtitle else ft.Container(height=0),
            ], spacing=6),
        )
