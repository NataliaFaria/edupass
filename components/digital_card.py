import flet as ft  # Certifique-se de que esta linha está presente
from database import Database

class DigitalCard(ft.UserControl):
    def __init__(self, page, user_id):
        super().__init__()
        self.page = page
        self.user_id = user_id
        self.db = Database()

    def build(self):
        student_info = self.db.get_student_info(self.user_id)
        return ft.Column(
            controls=[
                ft.Text(f"Carteirinha de {student_info[0]}", size=24, weight="bold"),
                ft.Text(f"Nome: {student_info[0]}"),
                ft.Text(f"CPF: {student_info[1]}"),
                ft.Text(f"E-mail: {student_info[2]}"),
                ft.Text(f"Celular: {student_info[3]}"),
                ft.Text("Esse é o seu cartão digital, apresente-o quando necessário."),
                ft.ElevatedButton("Voltar ao Perfil", on_click=self.go_to_profile),
                ft.ElevatedButton("Sair", on_click=self.logout),
            ],
            alignment="center",
            horizontal_alignment="center"
        )

    def go_to_profile(self, e):
        from pages.profile_page import ProfilePage  # Importação atrasada
        self.page.controls.clear()
        self.page.add(ProfilePage(self.page, self.user_id))
        self.page.update()

    def logout(self, e):
        from pages.login_page import LoginPage  # Importação atrasada
        self.page.controls.clear()
        self.page.add(LoginPage(self.page, on_login_success, go_to_register_page))
        self.page.update()
