import flet as ft
from database import register_institution

def institution_registration_page(page: ft.Page):
    page.clean()
    page.title = "Cadastro - Instituição"
    
    # Função para voltar para a página inicial
    def navigate_to_home(e):
        page.go("/")

    def register(e):
        name = name_field.value
        email = email_field.value
        password = password_field.value
        
        if register_institution(name, email, password):
            page.go("/institution_login")  # Navegar para a página de login após cadastro
        else:
            page.add(ft.Text("Email já cadastrado!", color=ft.colors.RED))

    # Layout da página de cadastro da instituição
    name_field = ft.TextField(label="Nome da Instituição")
    email_field = ft.TextField(label="Email")
    password_field = ft.TextField(label="Senha", password=True)

    page.add(
        ft.Column(
            controls=[
                ft.Text("Cadastro - Instituição", size=30),
                name_field,
                email_field,
                password_field,
                ft.ElevatedButton("Cadastrar", on_click=register),
                ft.TextButton("Já tem uma conta? Login", on_click=lambda e: page.go("/institution_login")),
                ft.TextButton("Voltar para Home", on_click=navigate_to_home)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )
