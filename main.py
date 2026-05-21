
import flet as ft
from app import App


def main(page: ft.Page):
    app = App(page)
    app.initialize()


ft.app(target=main)