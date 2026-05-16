import flet as ft
from styles.theme import (
    SURFACE, BORDER, ACCENT, TEXT_PRIMARY, TEXT_SECONDARY,
    TEXT_MUTED, SURFACE_2, DARK_BG
)


class Sidebar(ft.UserControl):
    ITEMS = [
        ("dashboard",  "\ue871", "Dashboard"),
        ("convenios",  "\ue8b8", "Convênios"),
        ("monitoramento", "\ue8b6", "Monitoramento"),
    ]

    def __init__(self, on_navigate, active_page="dashboard"):
        super().__init__()
        self.on_navigate = on_navigate
        self.active_page = active_page

    def build(self):
        nav_items = []
        for key, icon, label in self.ITEMS:
            is_active = key == self.active_page
            nav_items.append(self._nav_item(key, icon, label, is_active))

        return ft.Container(
            width=220,
            bgcolor=SURFACE,
            border=ft.border.only(right=ft.BorderSide(1, BORDER)),
            content=ft.Column(
                [
                    # Logo
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Icon(ft.icons.ACCOUNT_BALANCE, color=ACCENT, size=22),
                                    bgcolor="#1A2744",
                                    border_radius=8,
                                    padding=8,
                                ),
                                ft.Column([
                                    ft.Text("ConvênioMgr", size=13, weight=ft.FontWeight.W_700, color=TEXT_PRIMARY),
                                    ft.Text("Sistema de Gestão", size=10, color=TEXT_MUTED),
                                ], spacing=0),
                            ], spacing=10),
                        ]),
                        padding=ft.padding.symmetric(horizontal=16, vertical=20),
                        border=ft.border.only(bottom=ft.BorderSide(1, BORDER)),
                    ),

                    # Nav
                    ft.Container(
                        content=ft.Column(
                            [ft.Text("NAVEGAÇÃO", size=10, color=TEXT_MUTED, weight=ft.FontWeight.W_600)] + nav_items,
                            spacing=4,
                        ),
                        padding=ft.padding.only(left=12, right=12, top=20, bottom=12),
                    ),

                    ft.Column(expand=True),

                    # Footer
                    ft.Container(
                        content=ft.Text("MVP v1.0.0", size=10, color=TEXT_MUTED),
                        padding=ft.padding.symmetric(horizontal=16, vertical=16),
                        border=ft.border.only(top=ft.BorderSide(1, BORDER)),
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            expand=False,
        )

    def _nav_item(self, key, icon_code, label, is_active):
        color = ACCENT if is_active else TEXT_SECONDARY
        bg = "#1A2744" if is_active else "transparent"

        def on_click(e, k=key):
            self.on_navigate(k)

        return ft.Container(
            content=ft.Row([
                ft.Icon(name=icon_code, color=color, size=18),
                ft.Text(label, size=13, color=color, weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.W_400),
            ], spacing=10),
            bgcolor=bg,
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            on_click=on_click,
            border=ft.border.all(1, ACCENT if is_active else "transparent"),
        )
