
import flet as ft

PRIMARY = "#1E3A8A"
SECONDARY = "#2563EB"
BACKGROUND = "#F5F7FA"


def get_theme():

    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=PRIMARY,
            secondary=SECONDARY,
        )
    )