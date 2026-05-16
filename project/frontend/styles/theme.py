import flet as ft

# ─── Paleta ────────────────────────────────────────────────
DARK_BG        = "#0D1117"
SURFACE        = "#161B22"
SURFACE_2      = "#1C2128"
BORDER         = "#30363D"
ACCENT         = "#58A6FF"
ACCENT_GLOW    = "#1F6FEB"
SUCCESS        = "#3FB950"
WARNING        = "#D29922"
DANGER         = "#F85149"
TEXT_PRIMARY   = "#E6EDF3"
TEXT_SECONDARY = "#8B949E"
TEXT_MUTED     = "#484F58"

# Status colors
STATUS_COLORS = {
    "Vigente":               SUCCESS,
    "Próximo do vencimento": WARNING,
    "Vencido":               DANGER,
}

STATUS_BG = {
    "Vigente":               "#0D2E1A",
    "Próximo do vencimento": "#2E1F00",
    "Vencido":               "#2E0D0D",
}

# ─── Typography ────────────────────────────────────────────
FONT_TITLE  = "Segoe UI"
FONT_BODY   = "Segoe UI"

# ─── Spacing ───────────────────────────────────────────────
RADIUS = 10
GAP    = 16
PAD    = 20


def badge(text: str, color: str, bg: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(text, size=11, color=color, weight=ft.FontWeight.W_600),
        bgcolor=bg,
        border_radius=20,
        padding=ft.padding.symmetric(horizontal=10, vertical=4),
        border=ft.border.all(1, color),
    )


def status_badge(status: str) -> ft.Container:
    color = STATUS_COLORS.get(status, TEXT_SECONDARY)
    bg = STATUS_BG.get(status, SURFACE_2)
    return badge(status, color, bg)


def card(content, padding=PAD, bgcolor=SURFACE, border_color=BORDER, **kwargs) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=bgcolor,
        border_radius=RADIUS,
        padding=padding,
        border=ft.border.all(1, border_color),
        **kwargs,
    )


def section_title(text: str, subtitle: str = None) -> ft.Column:
    children = [
        ft.Text(text, size=20, weight=ft.FontWeight.W_700, color=TEXT_PRIMARY)
    ]
    if subtitle:
        children.append(ft.Text(subtitle, size=13, color=TEXT_SECONDARY))
    return ft.Column(children, spacing=2)
