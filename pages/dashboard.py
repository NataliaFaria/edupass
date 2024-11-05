import flet as ft
from database import Database
from components.student_card import StudentCardPage

class DashboardPage:
    def __init__(self, page: ft.Page, user_type: str, student_id: int = None):
        self.page = page
        self.user_type = user_type
        self.student_id = student_id
        self.create_dashboard()

    def create_dashboard(self):
        self.page.clean()
        self.page.title = "Painel de Controle"

        if self.user_type == "institution":
            content = ft.Column(
                controls=[
                    ft.Text("Bem-vindo ao painel da Instituição!", size=30),
                    ft.TextButton("Gerenciar Alunos", on_click=lambda e: self.page.add(ft.Text("Funcionalidade de Gerenciamento de Alunos"))),
                    ft.TextButton("Visualizar Relatórios", on_click=lambda e: self.page.add(ft.Text("Funcionalidade de Relatórios"))),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        else:  # user_type == "student"
            content = ft.Column(
                controls=[
                    ft.Text("Bem-vindo ao painel do Aluno!", size=30),
                    ft.TextButton("Meus Cursos", on_click=lambda e: self.page.add(ft.Text("Lista de Cursos Inscritos"))),
                    ft.TextButton("Meu Progresso", on_click=lambda e: self.page.add(ft.Text("Progresso do Aluno"))),
                    ft.TextButton("Status", on_click=lambda e: self.page.add(ft.Text("Status"))),
                    ft.TextButton("Ver Minha Carteirinha", on_click=self.show_student_card),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )

        home_button = ft.TextButton("Logout", on_click=lambda e: self.page.go("/"))

        self.page.add(
            ft.Column(
                controls=[content, home_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def show_student_card(self, e):
        if self.student_id is not None:
            StudentCardPage(self.page, self.student_id)
        else:
            self.page.add(ft.Text("ID do aluno não disponível.", color="red"))
