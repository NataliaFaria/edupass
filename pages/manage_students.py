import flet as ft
from database import Database

class ManageStudentsPage:
    def __init__(self, page: ft.Page, institution_id: int):
        self.page = page
        self.institution_id = institution_id
        self.database = Database()
        self.create_institution_dashboard()

    def create_institution_dashboard(self):
        self.page.clean()
        self.page.title = "Visão da Instituição"

        # Obter a lista de alunos da instituição com documentos associados
        students = self.database.get_students_by_institution(self.institution_id)

        # Remover duplicatas com base no 'student_id'
        unique_students = {}
        for student in students:
            unique_students[student["student_id"]] = student  # 'student_id' como chave única

        # Agora 'unique_students' contém apenas alunos únicos
        unique_students_list = list(unique_students.values())

        if not unique_students_list:
            self.page.add(
                ft.Column(
                    controls=[
                        ft.Text("Nenhum aluno com documentos nesta instituição.", size=20, color="red"),
                        ft.TextButton("Voltar ao Painel Principal", on_click=self.go_back),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            return

        # Criar os cards dos alunos
        student_cards = [
            ft.GestureDetector(
                on_tap=lambda e, s_id=student["student_id"]: self.go_to_manage_documents(s_id),
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(f"Nome: {student['name']}", size=20, weight="bold"),
                                ft.Text(f"Status: {student['status']}"),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10,
                        ),
                        padding=20,
                    ),
                ),
            )
            for student in unique_students_list  # Usando a lista filtrada
        ]

        # Adicionar os cards à página usando Row para disposição horizontal
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Alunos com Documentos", size=30, weight="bold"),
                    ft.Row(
                        controls=student_cards,  # Alinha os cards horizontalmente
                        spacing=10, 
                        wrap=True,  # Distribui os cards na linha
                    ),
                    ft.TextButton("Voltar ao Painel Principal", on_click=self.go_back),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def go_back(self, e):
        self.page.go("/dashboard")

    def go_to_manage_documents(self, student_id):
        """Abre a página de gerenciamento de documentos do aluno"""
        from .manage_document import ManageDocumentPage  # Importação local
        ManageDocumentPage(self.page, student_id, self)
