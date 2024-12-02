import flet as ft
from database import Database

class ManageDocumentPage:
    def __init__(self, page: ft.Page, student_id: int, dashboard_page):
        self.page = page
        self.student_id = student_id
        self.dashboard_page = dashboard_page
        self.database = Database()
        self.create_manage_documents_page()

    def create_manage_documents_page(self):
        self.page.clean()
        self.page.title = "Gerenciar Documentos"

        # Obter documentos do aluno
        documents = self.database.get_documents_for_student(self.student_id)

        if not documents:
            self.page.add(
                ft.Column(
                    controls=[
                        ft.Text("Nenhum documento encontrado para este aluno.", size=20, color="red"),
                        ft.TextButton("Voltar", on_click=lambda e: self.dashboard_page.create_institution_dashboard()),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            return

        # Gerar lista de documentos com opções de download e alteração de status
        document_list = ft.ListView(
            controls=[
                ft.Column(
                    controls=[
                        ft.ListTile(
                            # title=ft.Text(f"Documento ID: {doc[0]}"),
                            # subtitle=ft.Text(f"Status: {doc[2]}"),
                            trailing=ft.Row(
                                controls=[
                                    ft.TextButton(
                                        "Baixar Documento",
                                        on_click=lambda e, doc_path=doc[3]: self.download_document(doc_path),
                                    ),
                                    ft.Dropdown(
                                        label="Status",
                                        options=[
                                            ft.dropdown.Option("Aprovado"),
                                            ft.dropdown.Option("Reprovado"),
                                        ],
                                        value=doc[2],
                                        on_change=lambda e, doc_id=doc[0]: self.update_status(
                                            e.control.value, doc_id
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                        ft.Divider(),
                    ]
                )
                for doc in documents
            ],
            spacing=10,
        )

        # Adicionar à página
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Documentos do Aluno", size=30),
                    document_list,
                    ft.TextButton("Voltar", on_click=lambda e: self.dashboard_page.create_institution_dashboard()),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def download_document(self, file_path):
        """Cria um link para baixar o documento"""
        self.page.add(ft.ExternalLink(text="Abrir Documento", url=file_path))

    def update_status(self, status, document_id):
        """Atualiza o status de um documento"""
        success = self.database.update_document_status(document_id, status)
        if success:
            self.page.add(ft.Text(f"Status atualizado para {status}.", color="green"))
        else:
            self.page.add(ft.Text(f"Erro ao atualizar status.", color="red"))
