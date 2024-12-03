import flet as ft
import sqlite3
from database import Database
import re


class StudentRegistrationPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.clean()
        self.page.title = "Cadastro - Aluno"
        self.database = Database()

        self.create_registration_page()

    def create_registration_page(self):
        # Campos adicionais para o formulário
        name_field = ft.TextField(label="Nome do Aluno")
        email_field = ft.TextField(label="Email")
        dob_field = ft.TextField(label="Data de Nascimento (DD/MM/AAAA)")
        cpf_field = ft.TextField(label="CPF")
        phone_field = ft.TextField(label="Telefone")
        address_field = ft.TextField(label="Endereço Residencial")
        password_field = ft.TextField(label="Senha", password=True)

        # Campos de instituição e curso
        institution_dropdown = ft.Dropdown(label="Instituição")
        course_dropdown = ft.Dropdown(label="Curso")

        def load_institutions():
            """Carrega as instituições cadastradas ao iniciar"""
            institutions = self.database.get_all_institutions()
            institution_dropdown.options = [ft.dropdown.Option(inst["id"], inst["name"]) for inst in institutions]
            institution_dropdown.update()

        def load_courses(e):
            """Atualiza os cursos disponíveis ao selecionar uma instituição"""
            institution_id = institution_dropdown.value
            if institution_id:
                courses = self.database.get_courses_by_institution(institution_id)
                if courses:
                    course_dropdown.options = [
                        ft.dropdown.Option(course["id"], course["name"]) for course in courses
                    ]
                    course_dropdown.update()
                else:
                    course_dropdown.options = []  # Limpar os cursos se não encontrar nenhum
                    course_dropdown.update()

        def navigate_to_home(e):
            """Navega para a página inicial"""
            self.page.go("/")

        def is_valid_email(email):
            """Valida se o e-mail é válido"""
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return re.match(pattern, email) is not None

        def is_valid_cpf(cpf):
            """Valida se o CPF tem 11 dígitos e formato correto"""
            return cpf.isdigit() and len(cpf) == 11

        def is_valid_date(date):
            """Valida se a data está no formato DD/MM/AAAA"""
            try:
                day, month, year = map(int, date.split("/"))
                return 1 <= day <= 31 and 1 <= month <= 12 and year > 1900
            except ValueError:
                return False

        def register(e):
            """Realiza o registro do aluno"""
            # Resetando mensagens de erro
            name_field.error_text = None
            email_field.error_text = None
            dob_field.error_text = None
            cpf_field.error_text = None
            phone_field.error_text = None
            address_field.error_text = None
            password_field.error_text = None
            institution_dropdown.error_text = None
            course_dropdown.error_text = None

            # Obter valores dos campos
            name = name_field.value.strip()
            email = email_field.value.strip()
            dob = dob_field.value.strip()
            cpf = cpf_field.value.strip()
            phone = phone_field.value.strip()
            address = address_field.value.strip()
            password = password_field.value.strip()
            institution_id = institution_dropdown.value
            course_id = course_dropdown.value

            # Validações
            is_valid = True
            if not name:
                name_field.error_text = "Nome é obrigatório."
                is_valid = False
            if not email or not is_valid_email(email):
                email_field.error_text = "Email inválido."
                is_valid = False
            if not dob or not is_valid_date(dob):
                dob_field.error_text = "Data de nascimento inválida (DD/MM/AAAA)."
                is_valid = False
            if not cpf or not is_valid_cpf(cpf):
                cpf_field.error_text = "CPF inválido (11 dígitos numéricos)."
                is_valid = False
            if not phone:
                phone_field.error_text = "Telefone é obrigatório."
                is_valid = False
            if not address:
                address_field.error_text = "Endereço é obrigatório."
                is_valid = False
            if not password:
                password_field.error_text = "Senha é obrigatória."
                is_valid = False
            if not institution_id:
                institution_dropdown.error_text = "Selecione uma instituição."
                is_valid = False
            if not course_id:
                course_dropdown.error_text = "Selecione um curso."
                is_valid = False

            # Atualizar os campos com mensagens de erro
            name_field.update()
            email_field.update()
            dob_field.update()
            cpf_field.update()
            phone_field.update()
            address_field.update()
            password_field.update()
            institution_dropdown.update()
            course_dropdown.update()

            if not is_valid:
                return  # Parar o registro se houver erros

            # Chamar o método de registro no banco de dados
            if self.database.register_student(name, email, dob, cpf, phone, address, password, institution_id, course_id):
                self.page.go("/student_login")
            else:
                self.page.add(ft.Text("Email ou CPF já cadastrado!", color=ft.colors.RED))

        # Adicionar campos ao formulário
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Cadastro - Aluno", size=30),
                    name_field,
                    email_field,
                    dob_field,
                    cpf_field,
                    phone_field,
                    address_field,
                    password_field,
                    institution_dropdown,
                    course_dropdown,
                    ft.ElevatedButton("Cadastrar", on_click=register),
                    ft.TextButton("Já tem uma conta? Login", on_click=lambda e: self.page.go("/student_login")),
                    ft.TextButton("Voltar para Home", on_click=navigate_to_home)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

        # Carregar as instituições e atualizar o dropdown
        load_institutions()

        # Atualizar cursos quando uma instituição for selecionada
        institution_dropdown.on_change = load_courses
