import flet as ft
from components.student_card import StudentCardPage
from .course_registration import CourseRegistrationPage
from database import Database

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
                    ft.TextButton("Cadastrar Curso", on_click=self.navigate_to_course_registration),  # Novo botão para registrar cursos
                    ft.TextButton("Ver Cursos Cadastrados", on_click=self.show_courses),  # Novo botão para visualizar cursos
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
    
    def navigate_to_course_registration(self, e):
        # Navegar para a página de registro de cursos
        CourseRegistrationPage(self.page)

    def show_courses(self, e):
        # Simulação de visualização de cursos cadastrados
        self.page.add(ft.Text("Lista de Cursos Cadastrados (Em desenvolvimento)"))

    def show_student_card(self, e):
        if self.student_id is not None:
            # Passa a instância de DashboardPage ao StudentCardPage
            StudentCardPage(self.page, self.student_id, self)
        else:
            self.page.add(ft.Text("ID do aluno não disponível.", color="red"))
