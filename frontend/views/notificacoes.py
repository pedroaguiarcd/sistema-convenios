# frontend/views/notificacoes.py

import flet as ft
import requests


API_URL = "http://localhost:5000/notificacoes"


def notificacoes_view(page: ft.Page):
    lista = ft.Column(spacing=10)

    def carregar_notificacoes():
        lista.controls.clear()

        response = requests.get(API_URL)
        notificacoes = response.json()

        for n in notificacoes:
            cor = ft.colors.RED_100 if not n["lida"] else ft.colors.GREY_200

            lista.controls.append(
                ft.Container(
                    bgcolor=cor,
                    padding=15,
                    border_radius=10,
                    content=ft.Column([
                        ft.Text(n["titulo"], weight=ft.FontWeight.BOLD),
                        ft.Text(n["mensagem"]),
                        ft.Text("Não lida" if not n["lida"] else "Lida"),
                    ])
                )
            )

        page.update()

    carregar_notificacoes()

    return ft.View(
        route="/notificacoes",
        controls=[
            ft.Text("Notificações", size=28, weight=ft.FontWeight.BOLD),
            lista
        ]
    )