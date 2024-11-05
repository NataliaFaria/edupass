import flet as ft
from database import Database

class InstitutionRegistrationPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.clean()
        self.page.title = "Cadastro - Instituição"
        self.database = Database()

        self.create_registration_page()

    def create_registration_page(self):
        name_field = ft.TextField(label="Nome da Instituição")
        email_field = ft.TextField(label="Email")
        password_field = ft.TextField(label="Senha", password=True)

        def navigate_to_home(e):
            self.page.go("/")

        def register(e):
            name = name_field.value
            email = email_field.value
            password = password_field.value
            
            if self.database.register_institution(name, email, password):
                self.page.go("/institution_login")  # Navegar para a página de login após cadastro
            else:
                self.page.add(ft.Text("Email já cadastrado!", color=ft.colors.RED))

        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Cadastro - Instituição", size=30),
                    name_field,
                    email_field,
                    password_field,
                    ft.ElevatedButton("Cadastrar", on_click=register),
                    ft.TextButton("Já tem uma conta? Login", on_click=lambda e: self.page.go("/institution_login")),
                    ft.TextButton("Voltar para Home", on_click=navigate_to_home)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )
