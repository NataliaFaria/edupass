import flet as ft
from database import login_institution
from dashboard import dashboard_page

def institution_login_page(page: ft.Page):
    page.clean()
    page.title = "Login - Instituição"

    def navigate_to_institution_registration(e):
        page.go("/institution_registration")
    
    def navigate_to_home(e):
        page.go("/")

    def login(e):
        email = email_field.value
        password = password_field.value
        if login_institution(email, password):
            # Redirecionar para o painel de controle da instituição
            dashboard_page(page, user_type="institution")
        else:
            page.add(ft.Text("Email ou senha incorretos!", color=ft.colors.RED))

    email_field = ft.TextField(label="Email")
    password_field = ft.TextField(label="Senha", password=True)

    page.add(
        ft.Column(
            controls=[
                ft.Text("Login - Instituição", size=30),
                email_field,
                password_field,
                ft.ElevatedButton("Entrar", on_click=login),
                ft.TextButton("Cadastrar instituição", on_click=navigate_to_institution_registration),
                ft.TextButton("Voltar para Home", on_click=navigate_to_home)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )
