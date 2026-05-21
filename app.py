import flet as ft

from theme import get_theme
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.convenios_view import ConveniosView


class App:

    def __init__(self, page: ft.Page):
        self.page = page

    def initialize(self):
        self.page.title = "Sistema de Convênios"
        self.page.theme = get_theme()
        self.page.window_width = 1440
        self.page.window_height = 900
        self.page.padding = 0
        self.page.bgcolor = "#F5F7FA"
        self.page.theme_mode = ft.ThemeMode.LIGHT

        self.page.on_route_change = self.route_change

        self.page.go("/login")

    def route_change(self, route):
        self.page.views.clear()

        if self.page.route == "/login":
            self.page.views.append(LoginView(self.page))

        elif self.page.route == "/dashboard":
            self.page.views.append(DashboardView(self.page))

        elif self.page.route == "/convenios":
            self.page.views.append(ConveniosView(self.page))

        self.page.update()