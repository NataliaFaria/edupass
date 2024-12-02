import flet as ft
from database import Database

class DocumentStatusPage:
    def __init__(self, page: ft.Page, student_id: int, dashboard_page):
        self.page = page
        self.student_id = student_id
        self.dashboard_page = dashboard_page
        self.database = Database()
        self.create_document_status_page()

    def create_document_status_page(self):
        self.page.clean()
        self.page.title = "Status dos Documentos"

        # Obter os documentos enviados pelo aluno
        documents = self.database.get_documents_for_student(self.student_id)

        if not documents:
            # Caso não haja documentos enviados
            self.page.add(
                ft.Column(
                    controls=[
                        ft.Text("Nenhum documento enviado.", size=20, color="red"),
                        ft.TextButton("Voltar ao Painel", on_click=lambda e: self.dashboard_page.create_dashboard()),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            return

        # Criar lista de documentos com status
        document_list = ft.ListView(
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.icons.DESCRIPTION),
                    title=ft.Text(f"Documento: {document[4]}"), 
                    subtitle=ft.Text(f"Status: {document[6]}"),
                    trailing=ft.TextButton(
                        "Baixar", 
                        on_click=lambda e, doc_path=document[3]: self.download_document(doc_path)
                    ),
                )
                for document in documents
            ],
            spacing=10,
        )

        # Adicionar à página
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Status dos Documentos", size=30),
                    document_list,
                    ft.TextButton("Voltar ao Painel", on_click=lambda e: self.dashboard_page.create_dashboard()),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def download_document(self, doc_path):
        """Simula o download do documento ao abrir o arquivo em um navegador"""
        self.page.add(ft.ExternalLink(text="Abrir Documento", url=doc_path))
