import flet as ft
import threading
from services import api
from styles.theme import (
    SURFACE, SURFACE_2, BORDER, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    ACCENT, SUCCESS, WARNING, DANGER, DARK_BG, status_badge, STATUS_COLORS,
    section_title, card
)

TIPOS = ["Estágio", "Técnico", "Graduação", "Pós-Graduação", "Pesquisa", "Extensão", "Outro"]
STATUS_OPTIONS = ["", "Vigente", "Próximo do vencimento", "Vencido"]


class ConveniosPage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self._convenios = []
        self._filter_status = ""
        self._filter_empresa = ""
        self._filter_tipo = ""

    def build(self):
        self._list_container = ft.Column(spacing=0)
        self._loading_ring = ft.Container(
            content=ft.ProgressRing(color=ACCENT, width=30, height=30),
            alignment=ft.alignment.center,
            padding=40,
        )

        filter_row = ft.Row([
            ft.TextField(
                hint_text="Buscar empresa...",
                on_change=self._on_filter_empresa,
                bgcolor=SURFACE_2,
                border_color=BORDER,
                color=TEXT_PRIMARY,
                hint_style=ft.TextStyle(color=TEXT_MUTED),
                height=42,
                text_size=13,
                expand=True,
                prefix_icon=ft.icons.SEARCH,
            ),
            ft.Dropdown(
                hint_text="Status",
                options=[ft.dropdown.Option(s or "Todos", s or "Todos") for s in STATUS_OPTIONS],
                on_change=self._on_filter_status,
                bgcolor=SURFACE_2,
                border_color=BORDER,
                color=TEXT_PRIMARY,
                width=180,
                height=42,
                text_size=13,
            ),
            ft.Dropdown(
                hint_text="Tipo",
                options=[ft.dropdown.Option("", "Todos")] + [ft.dropdown.Option(t, t) for t in TIPOS],
                on_change=self._on_filter_tipo,
                bgcolor=SURFACE_2,
                border_color=BORDER,
                color=TEXT_PRIMARY,
                width=160,
                height=42,
                text_size=13,
            ),
            ft.ElevatedButton(
                "Novo Convênio",
                icon=ft.icons.ADD,
                on_click=lambda e: self._open_form(None),
                bgcolor=ACCENT,
                color="#FFFFFF",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            ),
        ], spacing=12)

        self._main = ft.Column([
            ft.Row([section_title("Convênios", "Gestão e cadastro de convênios")]),
            filter_row,
            ft.Divider(height=1, color=BORDER),
            self._loading_ring,
            self._list_container,
        ], spacing=20, scroll=ft.ScrollMode.AUTO, expand=True)

        threading.Thread(target=self._load, daemon=True).start()
        return self._main

    def _load(self):
        resp = api.listar_convenios(
            status=self._filter_status or None,
            empresa=self._filter_empresa or None,
            tipo=self._filter_tipo or None,
        )
        self._convenios = resp.get("data", [])
        if self.page:
            self.page.run_thread(self._render_list)

    def _render_list(self):
        self._loading_ring.visible = False
        self._list_container.controls = []

        if not self._convenios:
            self._list_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.INBOX, color=TEXT_MUTED, size=40),
                        ft.Text("Nenhum convênio encontrado.", color=TEXT_SECONDARY),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    padding=60,
                )
            )
        else:
            header = ft.Container(
                content=ft.Row([
                    ft.Text("Empresa / Responsável", size=11, color=TEXT_MUTED, weight=ft.FontWeight.W_600, expand=3),
                    ft.Text("Tipo", size=11, color=TEXT_MUTED, expand=2),
                    ft.Text("Vencimento", size=11, color=TEXT_MUTED, expand=2),
                    ft.Text("Dias", size=11, color=TEXT_MUTED, expand=1),
                    ft.Text("Status", size=11, color=TEXT_MUTED, expand=2),
                    ft.Text("Ações", size=11, color=TEXT_MUTED, expand=1),
                ]),
                padding=ft.padding.symmetric(horizontal=16, vertical=10),
                bgcolor=SURFACE_2,
                border_radius=ft.border_radius.only(top_left=8, top_right=8),
                border=ft.border.only(bottom=ft.BorderSide(1, BORDER)),
            )
            self._list_container.controls.append(header)

            for i, c in enumerate(self._convenios):
                self._list_container.controls.append(self._row(c, i))

        self.update()

    def _row(self, c, idx):
        dias = c.get("dias_restantes", 0)
        status = c.get("status", "")
        dias_color = DANGER if dias < 0 else (WARNING if dias <= 30 else SUCCESS)
        dias_str = str(dias) if dias >= 0 else f"−{abs(dias)}"
        bg = SURFACE_2 if idx % 2 == 0 else "transparent"

        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(c.get("nome_empresa", ""), size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                    ft.Text(c.get("responsavel", ""), size=11, color=TEXT_MUTED),
                ], expand=3, spacing=2),
                ft.Text(c.get("tipo_convenio", ""), size=12, color=TEXT_SECONDARY, expand=2),
                ft.Text(
                    (c.get("data_vencimento") or "")[:10],
                    size=12, color=TEXT_SECONDARY, expand=2
                ),
                ft.Text(dias_str, size=12, color=dias_color, weight=ft.FontWeight.W_600, expand=1),
                ft.Container(content=status_badge(status), expand=2),
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.EDIT_OUTLINED, icon_color=ACCENT, icon_size=16,
                        tooltip="Editar",
                        on_click=lambda e, cid=c["id"]: self._open_form(cid),
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE_OUTLINE, icon_color=DANGER, icon_size=16,
                        tooltip="Excluir",
                        on_click=lambda e, cid=c["id"]: self._confirm_delete(cid),
                    ),
                ], spacing=0, expand=1),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=16, vertical=10),
            bgcolor=bg,
        )

    def _open_form(self, convenio_id):
        existing = None
        if convenio_id:
            resp = api.buscar_convenio(convenio_id)
            existing = resp.get("data")

        fields = {
            "nome_empresa": ft.TextField(label="Nome da Empresa *", value=existing.get("nome_empresa", "") if existing else "",
                                          bgcolor=SURFACE_2, border_color=BORDER, color=TEXT_PRIMARY, label_style=ft.TextStyle(color=TEXT_SECONDARY)),
            "cnpj": ft.TextField(label="CNPJ *", value=existing.get("cnpj", "") if existing else "",
                                  bgcolor=SURFACE_2, border_color=BORDER, color=TEXT_PRIMARY, label_style=ft.TextStyle(color=TEXT_SECONDARY)),
            "tipo_convenio": ft.Dropdown(
                label="Tipo *",
                options=[ft.dropdown.Option(t) for t in TIPOS],
                value=existing.get("tipo_convenio") if existing else None,
                bgcolor=SURFACE_2, border_color=BORDER, color=TEXT_PRIMARY,
                label_style=ft.TextStyle(color=TEXT_SECONDARY),
            ),
            "data_inicio": ft.TextField(label="Data Início * (AAAA-MM-DD)", value=existing.get("data_inicio", "")[:10] if existing else "",
                                         bgcolor=SURFACE_2, border_color=BORDER, color=TEXT_PRIMARY, label_style=ft.TextStyle(color=TEXT_SECONDARY)),
            "data_vencimento": ft.TextField(label="Data Vencimento * (AAAA-MM-DD)", value=existing.get("data_vencimento", "")[:10] if existing else "",
                                              bgcolor=SURFACE_2, border_color=BORDER, color=TEXT_PRIMARY, label_style=ft.TextStyle(color=TEXT_SECONDARY)),
            "responsavel": ft.TextField(label="Responsável *", value=existing.get("responsavel", "") if existing else "",
                                         bgcolor=SURFACE_2, border_color=BORDER, color=TEXT_PRIMARY, label_style=ft.TextStyle(color=TEXT_SECONDARY)),
            "email_empresa": ft.TextField(label="E-mail da Empresa", value=existing.get("email_empresa", "") if existing else "",
                                           bgcolor=SURFACE_2, border_color=BORDER, color=TEXT_PRIMARY, label_style=ft.TextStyle(color=TEXT_SECONDARY)),
            "observacoes": ft.TextField(label="Observações", value=existing.get("observacoes", "") if existing else "",
                                         multiline=True, min_lines=3, bgcolor=SURFACE_2, border_color=BORDER,
                                         color=TEXT_PRIMARY, label_style=ft.TextStyle(color=TEXT_SECONDARY)),
        }

        error_text = ft.Text("", color=DANGER, size=12)

        def save(e):
            data = {k: f.value for k, f in fields.items()}
            try:
                if convenio_id:
                    api.atualizar_convenio(convenio_id, data)
                else:
                    api.criar_convenio(data)
                self.page.close(dlg)
                threading.Thread(target=self._load, daemon=True).start()
            except Exception as ex:
                error_text.value = str(ex)
                self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Editar Convênio" if convenio_id else "Novo Convênio", color=TEXT_PRIMARY, size=16, weight=ft.FontWeight.W_700),
            bgcolor=SURFACE,
            content=ft.Container(
                content=ft.Column(
                    [fields[k] for k in fields] + [error_text],
                    spacing=12, scroll=ft.ScrollMode.AUTO,
                ),
                width=480,
                height=520,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(dlg),
                               style=ft.ButtonStyle(color=TEXT_SECONDARY)),
                ft.ElevatedButton("Salvar", on_click=save, bgcolor=ACCENT, color="#FFFFFF",
                                   style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))),
            ],
        )
        self.page.open(dlg)

    def _confirm_delete(self, cid):
        def do_delete(e):
            api.deletar_convenio(cid)
            self.page.close(dlg)
            threading.Thread(target=self._load, daemon=True).start()

        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar exclusão", color=TEXT_PRIMARY),
            bgcolor=SURFACE,
            content=ft.Text("Deseja remover este convênio? A ação não pode ser desfeita.", color=TEXT_SECONDARY),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(dlg),
                               style=ft.ButtonStyle(color=TEXT_SECONDARY)),
                ft.ElevatedButton("Excluir", on_click=do_delete, bgcolor=DANGER, color="#FFFFFF",
                                   style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))),
            ],
        )
        self.page.open(dlg)

    def _on_filter_empresa(self, e):
        self._filter_empresa = e.control.value
        threading.Thread(target=self._load, daemon=True).start()

    def _on_filter_status(self, e):
        v = e.control.value
        self._filter_status = "" if v in ("Todos", None) else v
        threading.Thread(target=self._load, daemon=True).start()

    def _on_filter_tipo(self, e):
        v = e.control.value
        self._filter_tipo = "" if v in ("Todos", "", None) else v
        threading.Thread(target=self._load, daemon=True).start()
