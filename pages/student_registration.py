import flet as ft
import sqlite3
from database import Database


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
            # print(institutions)
            institution_dropdown.options = [ft.dropdown.Option(inst["id"], inst["name"]) for inst in institutions]
            institution_dropdown.update()

        def load_courses(e):
            """Atualiza os cursos disponíveis ao selecionar uma instituição"""
            institution_id = institution_dropdown.value
            # print(f"Instituição selecionada: {institution_id}")
            if institution_id:
                courses = self.database.get_courses_by_institution(institution_id)
                # print(f"Cursos encontrados: {courses}")
                if courses:
                    course_dropdown.options = [ft.dropdown.Option(course["id"], course["name"]) for course in courses]  # Corrigido: Usando o 'id' do curso
                    course_dropdown.update()
                else:
                    # print("Nenhum curso encontrado para esta instituição.")
                    # Mostrar uma mensagem ou tomar alguma ação caso não existam cursos
                    course_dropdown.options = []  # Limpar os cursos se não encontrar nenhum
                    course_dropdown.update()



        def navigate_to_home(e):
            """Navega para a página inicial"""
            self.page.go("/")

        def register(e):
            """Realiza o registro do aluno"""
            # Obter valores dos campos
            name = name_field.value
            email = email_field.value
            dob = dob_field.value
            cpf = cpf_field.value
            phone = phone_field.value
            address = address_field.value
            password = password_field.value
            institution_id = institution_dropdown.value
            course_id = course_dropdown.value

            # Chamar o método de registro no banco de dados
            if self.database.register_student(name, email, dob, cpf, phone, address, password, institution_id, course_id):
                # print("Aluno registrado com sucesso!") 
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
