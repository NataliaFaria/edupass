import flet as ft
import qrcode
import base64
from io import BytesIO
from database import Database

class StudentCardPage:
    def __init__(self, page: ft.Page, student_id: int, dashboard_page: object):
        self.page = page
        self.student_id = student_id
        self.dashboard = dashboard_page
        self.db = Database()
        self.show_student_card()

    def go_back(self, e):
        # Retorna ao painel de controle
        self.dashboard.create_dashboard()  # Chama o método do DashboardPage
        self.page.update()

    def generate_qr_code_base64(self, student_data, status):
        """Gera um QR Code com os dados do aluno e retorna em formato base64"""
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr_data = f"ID: {student_data['id']}\nNome: {student_data['name']}\nE-mail: {student_data['email']}\nStatus: {status}"
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")

        # Converte a imagem para bytes
        byte_stream = BytesIO()
        img.save(byte_stream, format="PNG")
        byte_stream.seek(0)

        # Codifica a imagem para base64
        base64_image = base64.b64encode(byte_stream.getvalue()).decode("utf-8")
        return base64_image

    def get_student_status(self, student_id):
        """Verifica os documentos do estudante e determina o status"""
        documents = self.db.get_documents_for_student(student_id)  # Assume que a função retorna os documentos do estudante
        if documents:
            for doc in documents:
                # Acessando o status pelo índice correto da tupla
                status = doc[6]  # O status está no índice 6, conforme a estrutura que você passou
                if status == "Reprovado" or status == "Pendente":  # Se algum documento for reprovado, o status será reprovado
                    return "Reprovado"
            return "Aprovado"  # Se todos os documentos estiverem aprovados
        else:
            return "Reprovado"


    def show_student_card(self):
        student_data = self.db.get_student_by_id(self.student_id)  # Obtém os dados do aluno
        
        self.page.clean()  # Limpa a página atual

        if student_data:
            # Verifica o status do aluno baseado nos documentos
            status = self.get_student_status(self.student_id)

            # Gera o QR Code com o status
            qr_code_base64 = self.generate_qr_code_base64(student_data, status)

            # Criando um container com os dados e QR Code
            self.page.add(
                ft.Column(
                    controls=[
                        ft.Text("Sua Carteirinha", size=30),
                        ft.Text(f"ID: {student_data['id']}", size=24),
                        ft.Text(f"Nome: {student_data['name']}", size=24),
                        ft.Text(f"E-mail: {student_data['email']}", size=24),
                        ft.Text(f"Status: {status}", size=24),  # Exibe o status
                        ft.Image(
                            src_base64=qr_code_base64,  # Exibe a imagem base64 diretamente
                            width=200,
                            height=200,
                        ),
                        ft.TextButton("Voltar para o Painel", on_click=self.go_back),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                )
            )
        else:
            self.page.add(ft.Text("Aluno não encontrado.", color="red"))

        self.page.update()  # Atualiza a página para refletir as mudanças
