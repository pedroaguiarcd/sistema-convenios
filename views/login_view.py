
import flet as ft




class LoginView(ft.View):

    def __init__(self, page: ft.Page):

        super().__init__(
            route="/login"
        )
        self.route = "/login"

        self.email = ft.TextField(
            label="Email institucional",
            width=400,
            prefix_icon=ft.Icons.EMAIL
        )

        self.password = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            width=400,
            prefix_icon=ft.Icons.LOCK
        )

        self.controls = [
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=ft.Card(
                    elevation=12,
                    content=ft.Container(
                        width=500,
                        padding=40,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(
                                    ft.Icons.ACCOUNT_BALANCE,
                                    size=80,
                                    color="#1E3A8A"
                                ),

                                ft.Text(
                                    "Sistema de Convênios",
                                    size=32,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    "Acesso institucional",
                                    color="grey"
                                ),

                                self.email,
                                self.password,

                                ft.ElevatedButton(
                                    "Entrar",
                                    width=400,
                                    height=50,
                                    style=ft.ButtonStyle(
                                        bgcolor="#2563EB",
                                        color="white",
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    ),
                                    on_click=self.login
                                )
                            ]
                        )
                    )
                )
            )
        ]

    def login(self, e):

        if self.email.value == "usuario" and self.password.value == "123":
            self.page.go("/dashboard")
        else:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Credenciais inválidas")
            )
            self.page.snack_bar.open = True
            self.page.update()