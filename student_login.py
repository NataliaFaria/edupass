import flet as ft
from database import login_student
from dashboard import dashboard_page

def student_login_page(page: ft.Page):
    page.clean()
    page.title = "Login - Aluno"

    def navigate_to_student_registration(e):
        page.go("/student_registration")
    
    def navigate_to_home(e):
        page.go("/")

    def login(e):
        email = email_field.value
        password = password_field.value
        if login_student(email, password):
            # Redirecionar para o painel de controle do aluno
            dashboard_page(page, user_type="student")
        else:
            page.add(ft.Text("Email ou senha incorretos!", color=ft.colors.RED))

    email_field = ft.TextField(label="Email")
    password_field = ft.TextField(label="Senha", password=True)

    page.add(
        ft.Column(
            controls=[
                ft.Text("Login - Aluno", size=30),
                email_field,
                password_field,
                ft.ElevatedButton("Entrar", on_click=login),
                ft.TextButton("Cadastrar aluno", on_click=navigate_to_student_registration),
                ft.TextButton("Voltar para Home", on_click=navigate_to_home)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )
