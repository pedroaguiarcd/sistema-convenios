import sys
import os

# Adiciona o diretório frontend ao path
sys.path.insert(0, os.path.dirname(__file__))

import flet as ft
from components.sidebar import Sidebar
from pages import DashboardPage, ConveniosPage, MonitoramentoPage
from styles.theme import DARK_BG, SURFACE, BORDER, TEXT_PRIMARY, ACCENT


def main(page: ft.Page):
    page.title = "ConvênioMgr — Gestão Inteligente"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = DARK_BG
    page.padding = 0
    page.window_width = 1280
    page.window_height = 800
    page.window_min_width = 900
    page.window_min_height = 600

    page.fonts = {}

    current_page = {"key": "dashboard"}
    content_area = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

    def navigate(page_key: str):
        current_page["key"] = page_key
        content_area.controls.clear()

        if page_key == "dashboard":
            content_area.controls.append(
                ft.Container(content=DashboardPage(page), expand=True, padding=24)
            )
        elif page_key == "convenios":
            content_area.controls.append(
                ft.Container(content=ConveniosPage(page), expand=True, padding=24)
            )
        elif page_key == "monitoramento":
            content_area.controls.append(
                ft.Container(content=MonitoramentoPage(page), expand=True, padding=24)
            )

        sidebar.active_page = page_key
        sidebar.update()
        page.update()

    sidebar = Sidebar(on_navigate=navigate, active_page="dashboard")

    layout = ft.Row(
        [
            sidebar,
            ft.VerticalDivider(width=1, color=BORDER),
            ft.Column([content_area], expand=True),
        ],
        expand=True,
        spacing=0,
    )

    page.add(layout)
    navigate("dashboard")


if __name__ == "__main__":
    ft.app(target=main)
