import flet as ft
from flet import Text, Container, Page
from database import Database

class StudentCardPage:
    def __init__(self, page: Page, student_id: int):
        self.page = page
        self.student_id = student_id
        self.db = Database()
        self.show_student_card()

    def show_student_card(self):
        student_data = self.db.get_student_by_id(self.student_id)  # Obtenha os dados do aluno

        self.page.clean()  # Limpa a página atual

        if student_data:
            # Criando um container simples com texto
            self.page.add(
                ft.Column(
                    controls=[
                        ft.Text("Sua Carteirinha", size=30),
                        ft.Text( f"ID: {student_data.id}", size=24),
                        ft.Text( f"Nome: {student_data.name}", size=24),
                        ft.Text( f"E-mail: {student_data.email}", size=24),
                        # ft.Container(
                        #     content=ft.Text( {student_data.name}, size=24),
                        #     padding=20,
                        #     border_radius=10,
                        #     alignment="center"
                        # )
                    ],
                    # alignment=ft.MainAxisAlignment.CENTER,
                    # spacing=20,
                )
            )
        else:
            self.page.add(ft.Text("Aluno não encontrado.", color="red"))

        self.page.update()  # Atualiza a página para refletir as mudanças
