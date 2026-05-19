import flet as ft

from frontend.views.convenios import tela_convenios


def main(page: ft.Page):
    page.title = "Sistema de Gestão de Convênios"

    page.theme_mode = ft.ThemeMode.LIGHT

    page.bgcolor = "#F4F6F9"

    page.padding = 30

    page.scroll = ft.ScrollMode.AUTO

    tela_convenios(page)

