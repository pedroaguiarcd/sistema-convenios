
import flet as ft


class Sidebar(ft.Container):

    def __init__(self, page: ft.Page):
        super().__init__()

        self.current_page = page
        self.width = 260
        self.bgcolor = "#1E293B"
        self.padding = 20

        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Convênios UESPI",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),

                ft.Divider(color="#334155"),

                self.menu_button(
                    "Dashboard",
                    ft.Icons.DASHBOARD,
                    "/dashboard"
                ),

                self.menu_button(
                    "Convênios",
                    ft.Icons.DESCRIPTION,
                    "/convenios"
                ),

                self.menu_button(
                    "Notificações",
                    ft.Icons.NOTIFICATIONS,
                    "/notificacoes"
                ),

                self.menu_button(
                    "Usuários",
                    ft.Icons.PEOPLE,
                    "/usuarios"
                ),
            ]
        )

    def menu_button(self, title, icon, route):
        return ft.ListTile(
            leading=ft.Icon(icon, color="white"),
            title=ft.Text(title, color="white"),
            on_click=lambda e: self.page.go(route)
        )