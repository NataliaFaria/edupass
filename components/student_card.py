import flet as ft
from database import Database

class StudentCardPage:
    def __init__(self, page: ft.Page, student_id: int, dashboard_page: object):
        self.page = page
        self.student_id = student_id
        self.dashboard = dashboard_page  # Guardar a instância do DashboardPage
        self.db = Database()
        self.show_student_card()

    def go_back(self, e):
        # Retorna ao painel de controle
        self.dashboard.create_dashboard()  # Chama o método do DashboardPage
        self.page.update()

    def show_student_card(self):
        student_data = self.db.get_student_by_id(self.student_id)  # Obtém os dados do aluno

        self.page.clean()  # Limpa a página atual

        if student_data:
            # Criando um container simples com texto
            self.page.add(
                ft.Column(
                    controls=[
                        ft.Text("Sua Carteirinha", size=30),
                        ft.Text(f"ID: {student_data['id']}", size=24),
                        ft.Text(f"Nome: {student_data['name']}", size=24),
                        ft.Text(f"E-mail: {student_data['email']}", size=24),
                        ft.TextButton("Voltar", on_click=self.go_back),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                )
            )
        else:
            self.page.add(ft.Text("Aluno não encontrado.", color="red"))

        self.page.update()  # Atualiza a página para refletir as mudanças
