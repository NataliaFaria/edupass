import flet as ft
from institution_login import institution_login_page
from student_login import student_login_page
from institution_registration import institution_registration_page
from student_registration import student_registration_page

def main(page: ft.Page):
    page.title = "EduPass"

    # Configurando as rotas
    def route_change(e):
        if e.route == "/":
            initial_page()
        elif e.route == "/institution_login":
            institution_login_page(page)
        elif e.route == "/student_login":
            student_login_page(page)
        elif e.route == "/institution_registration":
            institution_registration_page(page)
        elif e.route == "/student_registration":
            student_registration_page(page)

    page.on_route_change = route_change

    # Página inicial
    def initial_page():
        page.clean()
        page.add(
            ft.Column(
                controls=[
                    ft.Text("Bem-vindo ao EduPass!", size=30),
                    ft.ElevatedButton("Sou instituição", on_click=lambda e: page.go("/institution_login")),
                    ft.ElevatedButton("Sou aluno", on_click=lambda e: page.go("/student_login")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    initial_page()

# Executando o aplicativo
ft.app(target=main)
