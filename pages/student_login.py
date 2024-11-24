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

    def login(self, e):  # Método de instância com o parâmetro 'e'
        # Acessa os valores dos campos de entrada diretamente
        email = self.email_field_ref.current.value.strip()
        password = self.password_field_ref.current.value.strip()

        # Valida se os campos estão preenchidos
        if not email or not password:
            self.page.add(ft.Text("Por favor, preencha todos os campos.", color=ft.colors.RED))
            return

        # Verifica se a função de login foi passada
        if self.on_login:
            # Chama a função de login personalizada
            student = self.on_login(email, password)
            if student:
                # Se o login for bem-sucedido, redireciona para o dashboard
                DashboardPage(self.page, user_type="student", student_id=student[0])
            else:
                self.page.add(ft.Text("Email ou senha incorretos!", color=ft.colors.RED))
        else:
            # Faz a verificação diretamente no banco de dados
            student = self.database.login_student(email, password)
            if student:
                # Se o login for bem-sucedido, redireciona para o dashboard
                DashboardPage(self.page, user_type="student", student_id=student[0])
            else:
                self.page.add(ft.Text("Email ou senha incorretos!", color=ft.colors.RED))

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

        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Login - Aluno", size=30),
                    email_input,
                    password_input,
                    ft.ElevatedButton("Entrar", on_click=self.login),  # Aqui, chamamos o método de instância
                    ft.TextButton("Cadastrar aluno", on_click=navigate_to_student_registration),
                    ft.TextButton("Voltar para Home", on_click=navigate_to_home)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )
