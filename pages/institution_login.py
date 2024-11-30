import flet as ft
from database import Database
from .dashboard import DashboardPage

class InstitutionLoginPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.clean()
        self.page.title = "Login - Instituição"
        self.database = Database()

        self.create_login_page()

    def create_login_page(self):
        email_field = ft.TextField(label="Email")
        password_field = ft.TextField(label="Senha", password=True)

        def navigate_to_institution_registration(e):
            self.page.go("/institution_registration")
        
        def navigate_to_home(e):
            self.page.go("/")

        def login(e):
            email = email_field.value
            password = password_field.value
            if self.database.login_institution(email, password):
                # Obter o ID da instituição após o login
                institution_id = self.database.get_institution_id_by_email(email)

                if institution_id:
                    # Redirecionar para o painel de controle da instituição, passando o ID
                    DashboardPage(self.page, user_type="institution", institution_id=institution_id)
                else:
                    self.page.add(ft.Text("Instituição não encontrada.", color=ft.colors.RED))
            else:
                self.page.add(ft.Text("Email ou senha incorretos!", color=ft.colors.RED))

        self.page.add(
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
