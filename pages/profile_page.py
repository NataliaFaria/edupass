# pages/profile_page.py

import flet as ft
from database import Database
from pages.login_page import LoginPage
from components.digital_card import DigitalCard 

class ProfilePage(ft.UserControl):
    def __init__(self, page, user_id):
        super().__init__()
        self.page = page
        self.user_id = user_id
        self.db = Database()

    def build(self):
        student_info = self.db.get_student_info(self.user_id)
        return ft.Column(
            controls=[
                ft.Text(f"Perfil de {student_info[0]}", size=24, weight="bold"),
                ft.Text(f"Nome: {student_info[0]}"),
                ft.Text(f"CPF: {student_info[1]}"),
                ft.Text(f"E-mail: {student_info[2]}"),
                ft.Text(f"Celular: {student_info[3]}"),
                ft.ElevatedButton("Ver Carteirinha Digital", on_click=self.go_to_digital_card),
                # ft.ElevatedButton("Verificar Documentos", on_click=self.verify_documents),
                ft.ElevatedButton("Sair", on_click=self.logout),
            ],
            alignment="center",
            horizontal_alignment="center"
        )

    # def verify_documents(self, e):
    #     # Simulação de verificação de documentos
    #     self.message.value = "Documentos enviados para verificação."
    #     self.update()

    def go_to_digital_card(self, e):
        self.page.controls.clear()
        self.page.add(DigitalCard(self.page, self.user_id))
        self.page.update()

    def logout(self, e):
        self.page.controls.clear()
        self.page.add(LoginPage(self.page, on_login_success, go_to_register_page))
        self.page.update()
