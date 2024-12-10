import flet as ft
import os
from database import Database
import shutil

class DocumentUploadPage:
    def __init__(self, page: ft.Page, student_id: int, dashboard_page: object):
        self.page = page
        self.student_id = student_id
        # self.institution_id = institution_id
        self.dashboard = dashboard_page
        self.database = Database()
        self.create_upload_page()

    def create_upload_page(self):
        self.page.clean()
        self.page.title = "Upload de Documentos"

        file_picker_label = ft.Text("Escolha o arquivo para upload", size=20)

        self.file_picker = ft.FilePicker(on_result=self.handle_file_pick)
        self.page.overlay.append(self.file_picker)

        description_field = ft.TextField(label="Descrição do Documento", multiline=True)

        # Função para upload do documento
        def upload_document(e):
            # Validar se o aluno e o arquivo estão presentes
            if not hasattr(self, 'selected_file') or not self.selected_file:
                self.page.add(ft.Text("Por favor, selecione um arquivo para upload.", color="red"))
                return
            if not description_field.value:
                self.page.add(ft.Text("Por favor, insira uma descrição para o documento.", color="red"))
                return

            #caminho do arquivo
            file_path = f"uploads/{self.selected_file.name}"

            # Verifica se o diretório "uploads" existe, se não, cria
            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            # Copiar o arquivo do caminho temporário para o diretório de uploads
            try:
                shutil.copy(self.selected_file.path, file_path)
            except Exception as e:
                self.page.add(ft.Text(f"Erro ao salvar o arquivo: {str(e)}", color="red"))
                return
            
            institution_id = self.database.get_institution_id(self.student_id)
            print(institution_id)

            # Registrar o documento no banco de dados
            if self.database.upload_document(self.student_id, institution_id, file_path, description_field.value):
                self.page.add(ft.Text("Documento enviado com sucesso!", color="green"))
            else:
                self.page.add(ft.Text("Erro ao enviar documento.", color="red"))

        # Botão para fazer o upload
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Upload de Documentos", size=30),
                    file_picker_label,  
                    description_field, 
                    ft.ElevatedButton("Escolher Arquivo", on_click=lambda _: self.file_picker.pick_files()),
                    ft.ElevatedButton("Enviar Documento", on_click=upload_document),
                    ft.TextButton("Voltar ao Painel", on_click=self.go_back),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

        # Atualizar a página para garantir que todos os controles sejam renderizados
        self.page.update()

    def go_back(self, e):
        
        self.dashboard.create_dashboard()
        self.page.update()


    def handle_file_pick(self, e):
        """Função chamada após selecionar o arquivo"""
        if e.files:
            self.selected_file = e.files[0]
            self.page.add(ft.Text(f"Arquivo selecionado: {self.selected_file.name}", color="green"))
        else:
            self.selected_file = None
            self.page.add(ft.Text("Nenhum arquivo selecionado", color="red"))
        
        # Atualizar a página para garantir que o texto seja renderizado após a seleção
        self.page.update()
