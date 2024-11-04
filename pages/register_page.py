import flet as ft
from database import Database

class RegisterPage(ft.UserControl):
    def __init__(self, page, go_to_login_page):
        super().__init__()
        self.page = page
        self.go_to_login_page = go_to_login_page
        self.db = Database()

    def register(self, e):
        nome = self.name_field.value
        cpf = self.cpf_field.value
        email = self.email_field.value
        celular = self.celular_field.value
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value

        if password != confirm_password:
            self.message.value = "As senhas não coincidem."
        else:
            success, msg = self.db.add_student(nome, cpf, email, celular, password)
            self.message.value = msg
            if success:
                self.go_to_login_page()
        self.update()

    def build(self):
        self.name_field = ft.TextField(label="Nome completo")
        self.cpf_field = ft.TextField(label="CPF")
        self.email_field = ft.TextField(label="E-mail")
        self.celular_field = ft.TextField(label="Celular")
        self.password_field = ft.TextField(label="Senha", password=True)
        self.confirm_password_field = ft.TextField(label="Confirmar senha", password=True)
        self.message = ft.Text()

        return ft.Column(
            controls=[
                ft.Text("Cadastro de Usuário", size=24, weight="bold"),
                self.name_field,
                self.cpf_field,
                self.email_field,
                self.celular_field,
                self.password_field,
                self.confirm_password_field,
                ft.ElevatedButton("Cadastrar", on_click=self.register),
                self.message,
                ft.TextButton("Já possui uma conta? Faça login", on_click=lambda _: self.go_to_login_page())
            ],
            alignment="center",
            horizontal_alignment="center",
        )