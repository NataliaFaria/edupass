import flet as ft
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

        def navigate_to_home(e):
            self.page.go("/")

        def register(e):
            # Obter valores dos campos
            name = name_field.value
            email = email_field.value
            dob = dob_field.value
            cpf = cpf_field.value
            phone = phone_field.value
            address = address_field.value
            password = password_field.value

            # Chamar o método de registro no banco de dados
            if self.database.register_student(name, email, dob, cpf, phone, address, password):
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
                    ft.ElevatedButton("Cadastrar", on_click=register),
                    ft.TextButton("Já tem uma conta? Login", on_click=lambda e: self.page.go("/student_login")),
                    ft.TextButton("Voltar para Home", on_click=navigate_to_home)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )
