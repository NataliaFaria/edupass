import flet as ft
import os
from database import Database
import shutil  # Para copiar o arquivo

class DocumentUploadPage:
    def __init__(self, page: ft.Page, student_id: int, institution_id: int):
        self.page = page
        self.student_id = student_id
        self.institution_id = institution_id
        self.database = Database()
        self.create_upload_page()

    def create_upload_page(self):
        self.page.clean()
        self.page.title = "Upload de Documentos"

        # Texto explicativo para o campo de upload de arquivo
        file_picker_label = ft.Text("Escolha o arquivo para upload", size=20)

        # Campo para selecionar o arquivo (agora está sendo adicionado na sobreposição)
        self.file_picker = ft.FilePicker(on_result=self.handle_file_pick)
        self.page.overlay.append(self.file_picker)

        # Campo para descrição do documento
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

            # Definir o caminho do arquivo
            file_path = f"uploads/{self.selected_file.name}"

            # Verificar se o diretório "uploads" existe, se não, criar
            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            # Copiar o arquivo do caminho temporário para o diretório de uploads
            try:
                shutil.copy(self.selected_file.path, file_path)
            except Exception as e:
                self.page.add(ft.Text(f"Erro ao salvar o arquivo: {str(e)}", color="red"))
                return

            # Registrar o documento no banco de dados
            if self.database.upload_document(self.student_id, self.institution_id, file_path, description_field.value):
                self.page.add(ft.Text("Documento enviado com sucesso!", color="green"))
            else:
                self.page.add(ft.Text("Erro ao enviar documento.", color="red"))

        # Botão para fazer o upload
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Upload de Documentos", size=30),
                    file_picker_label,  # Exibe o texto de instrução
                    description_field,  # Campo de descrição
                    ft.ElevatedButton("Escolher Arquivo", on_click=lambda _: self.file_picker.pick_files()),
                    ft.ElevatedButton("Enviar Documento", on_click=upload_document),
                    ft.TextButton("Voltar ao Painel", on_click=lambda e: self.page.go("/dashboard")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

        # Atualizar a página para garantir que todos os controles sejam renderizados
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
