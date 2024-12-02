import flet as ft
from database import Database

class ManageStudentsPage:
    def __init__(self, page: ft.Page, institution_id: int, dashboard_page):
        self.page = page
        self.institution_id = institution_id
        self.dashboard_page = dashboard_page
        self.database = Database()
        self.create_manage_students_page()

    def create_manage_students_page(self):
        self.page.clean()
        self.page.title = "Gerenciar Alunos"

        # Obter a lista de alunos da instituição
        students = self.database.get_students_by_institution(self.institution_id)

        if not students:
            self.page.add(
                ft.Column(
                    controls=[
                        ft.Text("Nenhum aluno cadastrado nesta instituição.", size=20, color="red"),
                        ft.TextButton("Voltar ao Painel", on_click=lambda e: self.dashboard_page.create_dashboard()),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            return

        # Gerar lista de alunos com opções de download e alteração de status
        student_list = ft.ListView(
            controls=[
                ft.Column(
                    # ft.ListTile(
                    #     title=ft.Text(student["name"]),
                    # ),
                    controls=[
                        ft.ListTile(
                            # title=ft.Text(student["name"]),
                            trailing=ft.Row(
                                controls=[
                                    ft.TextButton(
                                        "Baixar Documento",
                                        on_click=lambda e, s_id=student["student_id"]: self.download_document(s_id),
                                    ),
                                    ft.Dropdown(
                                        label="Status",
                                        options=[
                                            ft.dropdown.Option("Aprovado"),
                                            ft.dropdown.Option("Reprovado"),
                                        ],
                                        value=self.get_document_status(student["student_id"]),
                                        on_change=lambda e, student_id=student["student_id"]: self.update_status(
                                            e.control.value, student_id
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                        ft.Divider(),
                    ]
                )
                for student in students
            ],
            spacing=10,
        )

        # Adicionar à página
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Gerenciar Alunos", size=30),
                    student_list,
                    ft.TextButton("Voltar ao Painel", on_click=lambda e: self.dashboard_page.create_dashboard()),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def get_document_status(self, student_id):
        """Obtém o status do primeiro documento associado ao aluno"""
        documents = self.database.get_documents_for_student(student_id)
        if documents:
            return documents[0][2]  # Assumindo que document[2] é o status
        return None

    def download_document(self, student_id):
        """Lógica para baixar o documento do aluno específico"""
        documents = self.database.get_documents_for_student(student_id)
        if documents:
            # Assumindo que "documents" seja uma lista de tuplas, precisamos acessar o caminho do arquivo
            for document in documents:
                file_path = document[3]  # Ajuste conforme o índice correto na tupla
                # Cria um link externo para abrir o documento no navegador
                self.page.add(ft.ExternalLink(text="Abrir Documento", url=file_path))
                break  # Para abrir apenas o primeiro documento, caso haja vários
        else:
            self.page.add(ft.Text("Documento não encontrado.", color="red"))

    def update_status(self, status, student_id):
        """Atualiza o status de um documento específico de um aluno"""
        print(f"Tentando atualizar o status do aluno {student_id} para {status}...")  # Depuração
        documents = self.database.get_documents_for_student(student_id)
        if documents:
            updated = False  # Para garantir que ao menos um documento seja atualizado
            for document in documents:
                print(f"Verificando documento {document[0]} com status {document[2]}...")  # Depuração
                # Aqui, assumimos que document[0] é o ID do documento e document[2] é o status
                if document[2] != status:  # Verifica se o status é diferente
                    success = self.database.update_document_status(document[0], status)
                    if success:
                        self.page.add(ft.Text(f"Status do documento {document[0]} atualizado para {status}.", color="green"))
                        updated = True
                    else:
                        self.page.add(ft.Text(f"Erro ao atualizar status do documento {document[0]}.", color="red"))
            if not updated:
                self.page.add(ft.Text("Nenhum status foi alterado. Todos os documentos já estão com esse status.", color="orange"))
        else:
            self.page.add(ft.Text("Nenhum documento encontrado para este aluno.", color="red"))
