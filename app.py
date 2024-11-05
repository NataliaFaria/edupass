import flet as ft
from pages.institution_login import InstitutionLoginPage
from pages.student_login import StudentLoginPage
from pages.institution_registration import InstitutionRegistrationPage
from pages.student_registration import StudentRegistrationPage
from database import Database

class EduPassApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "EduPass"
        self.current_student_id = None  # Atributo para armazenar o ID do aluno logado
        self.db = Database()  # Inicializa o banco de dados
        self.initial_page()

        # Configurando as rotas
        self.page.on_route_change = self.route_change

    def route_change(self, e):
        if e.route == "/":
            self.initial_page()
        elif e.route == "/institution_login":
            InstitutionLoginPage(self.page)
        elif e.route == "/student_login":
            StudentLoginPage(self.page, on_login=self.handle_student_login)  # Passa a função de login
        elif e.route == "/institution_registration":
            InstitutionRegistrationPage(self.page)
        elif e.route == "/student_registration":
            StudentRegistrationPage(self.page)

    def handle_student_login(self, email, password):
        student = self.db.login_student(email, password)
        if student:
            self.current_student_id = student[0]  # Acesse o ID do aluno a partir da tupla
            print(f"Login bem-sucedido! ID do aluno: {self.current_student_id}")  # Debug
            return student  # Retorne o aluno
        print("Login falhou!")  # Debug
        return None  # Retorne None se falhar


    def initial_page(self):
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Bem-vindo ao EduPass!", size=30),
                    ft.ElevatedButton("Sou instituição", on_click=lambda e: self.page.go("/institution_login")),
                    ft.ElevatedButton("Sou aluno", on_click=lambda e: self.page.go("/student_login")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def get_logged_student_id(self):
        return self.current_student_id  # Retorna o ID do aluno logado

# Executando o aplicativo
ft.app(target=EduPassApp)
