
import flet as ft


PRIMARY = "#194f65"
PRIMARY_2 = "#34788d"
ORANGE = "#f19b4c"
BG = "#f4f7fb"
DARK = "#0f172a"
SUBTEXT = "#6b7280"
DANGER = "#dc2626"


class LoginView(ft.View):

    def __init__(self, page: ft.Page):
        super().__init__(
            route="/login",
            bgcolor=BG,
            padding=0,
            spacing=0,
        )

        self.page_ref = page

        self.usuario = ft.TextField(
            label="Usuário",
            hint_text="Digite seu usuário",
            prefix_icon=ft.Icons.PERSON,
            border_radius=12,
            height=55,
        )

        self.senha = ft.TextField(
            label="Senha",
            hint_text="Digite sua senha",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            border_radius=12,
            height=55,
        )

        self.erro = ft.Container(
            visible=False,
            padding=ft.Padding(14, 12, 14, 12),
            border_radius=12,
            bgcolor="#fee2e2",
            border=ft.border.Border(
                left=ft.BorderSide(4, DANGER)
            ),
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Icon(ft.Icons.ERROR_ROUNDED, color=DANGER),
                    ft.Text(
                        "Usuário ou senha inválidos.",
                        color=DANGER,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
            ),
        )

        self.controls = [
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=self.login_card(),
            )
        ]

    def login_card(self):
        return ft.Container(
            width=1050,
            height=620,
            bgcolor="white",
            border_radius=28,
            shadow=ft.BoxShadow(
                blur_radius=30,
                spread_radius=2,
                color="#00000020",
                offset=ft.Offset(0, 8),
            ),
            content=ft.Row(
                spacing=0,
                controls=[
                    self.left_panel(),
                    self.right_panel(),
                ],
            ),
        )

    def left_panel(self):
        return ft.Container(
            width=500,
            height=620,
            padding=ft.Padding(40, 40, 40, 40),
            border_radius=28,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[
                    "#0b3f56",
                    PRIMARY,
                    PRIMARY_2,
                ],
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=25,
                controls=[
                    ft.Image(
                        src="../assets/logo_.png",
                        width=260,
                        height=260,
                        fit="contain",
                    ),
                    ft.Text(
                        "ConvMonitor",
                        size=42,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                    ),
                    ft.Text(
                        "Gestão inteligente de convênios\ne parcerias institucionais",
                        size=17,
                        color="#e5e7eb",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    def right_panel(self):
        return ft.Container(
            expand=True,
            padding=ft.Padding(70, 60, 70, 60),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=22,
                controls=[
                    ft.Text(
                        "Bem-vindo!",
                        size=38,
                        weight=ft.FontWeight.BOLD,
                        color=DARK,
                    ),
                    ft.Text(
                        "Acesse sua conta para continuar",
                        size=16,
                        color=SUBTEXT,
                    ),
                    self.erro,
                    self.usuario,
                    self.senha,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Checkbox(
                                label="Lembrar-me",
                                value=True,
                                active_color=PRIMARY,
                            ),
                            ft.TextButton(
                                "Esqueci minha senha",
                                style=ft.ButtonStyle(
                                    color=PRIMARY,
                                ),
                            ),
                        ],
                    ),
                    ft.ElevatedButton(
                        "Entrar",
                        height=52,
                        width=420,
                        bgcolor=PRIMARY,
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                        ),
                        on_click=self.login,
                    ),
                ],
            ),
        )

    def login(self, e):
        usuario = self.usuario.value
        senha = self.senha.value

        # Login provisório. Depois trocar por chamada ao backend.
        if usuario == "admin" and senha == "123":
            self.erro.visible = False
            self.page_ref.go("/dashboard")
        else:
            self.erro.visible = True
            self.page_ref.update()


def main(page: ft.Page):
    page.title = "ConvMonitor"
    page.bgcolor = BG
    page.theme_mode = ft.ThemeMode.LIGHT

    page.views.append(LoginView(page))
    page.update()


ft.app(target=main)