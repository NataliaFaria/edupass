import flet as ft
from database import Database
from .dashboard import DashboardPage

class StudentLoginPage:
    def __init__(self, page: ft.Page, on_login=None):
        self.page = page
        self.on_login = on_login  # Armazena a função de login
        self.database = Database()  # Inicializa o banco de dados
        self.page.title = "Login - Aluno"
        self.page.clean()
        self.create_login_page()

    def create_login_page(self):
        # Cria referências para os campos de entrada
        self.email_field_ref = ft.Ref()
        self.password_field_ref = ft.Ref()

        email_input = ft.TextField(label="Email", width=300, ref=self.email_field_ref)
        password_input = ft.TextField(label="Senha", width=300, password=True, ref=self.password_field_ref)

        def navigate_to_student_registration(e):
            self.page.go("/student_registration")

        def navigate_to_home(e):
            self.page.go("/")

        def login(e):
            # Acessa os valores dos campos usando o método ref
            email = self.email_field_ref.current.value
            password = self.password_field_ref.current.value
            
            # Verifica se a função de login foi passada
            if self.on_login:
                # Chama a função de login passada
                student = self.on_login(email, password)  # Mude aqui para armazenar o retorno
                
                if student:  # Se a autenticação for bem-sucedida
                    DashboardPage(self.page, user_type="student", student_id=student[0])  # Passa o ID do aluno
                else:
                    self.page.add(ft.Text("Email ou senha incorretos!", color=ft.colors.RED))
            else:
                # Caso não tenha a função de login, faz a verificação diretamente no banco
                student = self.database.login_student(email, password)  # Modificado para retornar o aluno

                if student:
                    DashboardPage(self.page, user_type="student", student_id=student[0])  # Acesse o ID corretamente
                else:
                    self.page.add(ft.Text("Email ou senha incorretos!", color=ft.colors.RED))

        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Login - Aluno", size=30),
                    email_input,
                    password_input,
                    ft.ElevatedButton("Entrar", on_click=login),
                    ft.TextButton("Cadastrar aluno", on_click=navigate_to_student_registration),
                    ft.TextButton("Voltar para Home", on_click=navigate_to_home)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )
