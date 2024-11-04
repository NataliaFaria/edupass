import flet as ft
from database import register_student

def student_registration_page(page: ft.Page):
    page.clean()
    page.title = "Cadastro - Aluno"
    
    # Função para voltar para a página inicial
    def navigate_to_home(e):
        page.go("/")

    def register(e):
        name = name_field.value
        email = email_field.value
        password = password_field.value
        
        if register_student(name, email, password):
            page.go("/student_login")  # Navegar para a página de login após cadastro
        else:
            page.add(ft.Text("Email já cadastrado!", color=ft.colors.RED))

    # Layout da página de cadastro do aluno
    name_field = ft.TextField(label="Nome")
    email_field = ft.TextField(label="Email")
    password_field = ft.TextField(label="Senha", password=True)

    page.add(
        ft.Column(
            controls=[
                ft.Text("Cadastro - Aluno", size=30),
                name_field,
                email_field,
                password_field,
                ft.ElevatedButton("Cadastrar", on_click=register),
                ft.TextButton("Já tem uma conta? Login", on_click=lambda e: page.go("/student_login")),
                ft.TextButton("Voltar para Home", on_click=navigate_to_home)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )
