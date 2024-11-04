# pages/login_page.py

import flet as ft
from database import Database

class LoginPage(ft.UserControl):
    def __init__(self, page, on_login_success, go_to_register_page):
        super().__init__()
        self.page = page
        self.on_login_success = on_login_success
        self.go_to_register_page = go_to_register_page
        self.db = Database()

    def login(self, e):
        email = self.email_field.value
        password = self.password_field.value
        user_id = self.db.verify_login(email, password)

        if user_id:
            self.on_login_success(user_id)
        else:
            self.message.value = "Email ou senha incorretos!"
        self.update()

    def build(self):
        self.email_field = ft.TextField(label="E-mail", width=300)
        self.password_field = ft.TextField(label="Senha", password=True, width=300)
        self.message = ft.Text()

        return ft.Column(
            [
                ft.Text("Bem-vindo ao EduPass", size=24, weight="bold"),
                self.email_field,
                self.password_field,
                ft.ElevatedButton("Login", on_click=self.login),
                self.message,
                ft.TextButton("Não tem conta? Cadastre-se", on_click=lambda _: self.go_to_register_page())
            ],
            alignment="center",
            horizontal_alignment="center"
        )
