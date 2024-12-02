import flet as ft
from components.student_card import StudentCardPage
from .course_registration import CourseRegistrationPage
from .document_upload_page import DocumentUploadPage
from .manage_students import ManageStudentsPage
from .document_status_page import DocumentStatusPage
from .manage_document import ManageDocumentPage
from .course_page import CoursesPage
from components.botao import Botao, BotaoTexto, BotaoGeneros
from database import Database

class DashboardPage:
    def __init__(self, page: ft.Page, user_type: str, student_id: int = None, institution_id: int = None):
        self.page = page
        self.user_type = user_type
        self.student_id = student_id
        self.institution_id = institution_id
        self.database = Database()

        self.create_dashboard()

    def create_dashboard(self):
        self.page.clean()
        self.page.title = "Painel de Controle"

        if self.user_type == "institution":
            content = ft.Column(
                controls=[
                    ft.Text("Bem-vindo ao painel da Instituição!", size=30),
                    Botao("Gerenciar Alunos", self.navigate_to_manage_student),
                    Botao("Cadastrar Curso", self.navigate_to_course_registration),
                    Botao("Ver Cursos Cadastrados", self.navigate_to_courses),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        else:  # user_type == "student"
            content = ft.Column(
                controls=[
                    ft.Text("Bem-vindo ao painel do Aluno!", size=30),
                    Botao("Adicionar documentos", self.navigate_to_document_upload),
                    Botao("Status", self.navigate_to_document_status),
                    Botao("Ver Minha Carteirinha", self.show_student_card),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )

        home_button = Botao("Logout", lambda e: self.page.go("/"))


        self.page.add(
            ft.Column(
                controls=[content, home_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )
    
    def navigate_to_course_registration(self, e):
        """Navega para a página de registro de cursos"""
        self.page.clean()  # Limpa a página atual antes de navegar para a próxima
        CourseRegistrationPage(self.page, self)  # Passa a instância de DashboardPage para o CourseRegistrationPage


    def navigate_to_courses(self, e):
        CoursesPage(self.page, self, self.database)


    def show_student_card(self, e):
        if self.student_id is not None:
            # Navegar para a página da carteirinha
            self.page.clean()  # Limpa a página atual antes de navegar para a próxima
            StudentCardPage(self.page, self.student_id, self)  # Passa a instância de DashboardPage para o StudentCardPage
        else:
            self.page.add(ft.Text("ID do aluno não disponível.", color="red"))

    def navigate_to_document_upload(self, e):
        """Navega para a página de upload de documentos"""
        DocumentUploadPage(self.page, self.student_id, self)

    def navigate_to_manage_student(self, e):
        ManageStudentsPage(self.page, self.institution_id)


    def navigate_to_document_status(self, e):
        """Navega para a página de status dos documentos"""
        if self.student_id:
            DocumentStatusPage(self.page, self.student_id, self)
        else:
            self.page.add(ft.Text("Erro: ID do aluno não disponível.", color="red"))
