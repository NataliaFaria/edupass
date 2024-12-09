import unittest
from unittest.mock import MagicMock
from components.student_card import StudentCardPage
import flet as ft

class TestStudentCardPage(unittest.TestCase):
    def setUp(self):
        """Configura o ambiente de teste com os mocks necessários."""
        self.mock_db = MagicMock()
        self.mock_page = MagicMock(spec=ft.Page)
        self.mock_dashboard = MagicMock()

        # Mock dos métodos do banco
        self.mock_db.get_student_by_id.return_value = {
            "id": 1,
            "name": "Aluno Teste",
            "email": "aluno@teste.com"
        }
        self.mock_db.get_documents_for_student.return_value = [
            (1, "RG", "doc_rg.pdf", "2024-01-01", "2024-12-31", "validado", "Aprovado"),
            (2, "CPF", "doc_cpf.pdf", "2024-01-01", "2024-12-31", "validado", "Aprovado")
        ]

        # Instância da página com mocks
        self.student_card_page = StudentCardPage(
            page=self.mock_page,
            student_id=1,
            dashboard_page=self.mock_dashboard
        )
        self.student_card_page.db = self.mock_db  # Substitui o banco de dados pelo mock


    def test_get_student_status_approved(self):
        """Teste para verificar o status do aluno como 'Aprovado'."""
        status = self.student_card_page.get_student_status(1)
        self.assertEqual(
            status, 
            "Aprovado", 
            f"Erro: O status esperado para o aluno com ID 1 deveria ser 'Aprovado', mas foi '{status}'."
        )
        print("✔ Status do aluno: Aprovado - Sucesso!")

    def test_get_student_status_rejected(self):
        """Teste para verificar o status do aluno como 'Reprovado' quando os documentos são reprovados."""
        self.mock_db.get_documents_for_student.return_value = [
            (1, "RG", "doc_rg.pdf", "2024-01-01", "2024-12-31", "validado", "Reprovado")
        ]
        status = self.student_card_page.get_student_status(1)
        self.assertEqual(
            status, 
            "Reprovado", 
            f"Erro: O status esperado para o aluno com ID 1 deveria ser 'Reprovado', mas foi '{status}'."
        )
        print("✔ Status do aluno: Reprovado - Sucesso!")

    def test_generate_qr_code_base64(self):
        """Teste para verificar a geração do QR Code em base64."""
        student_data = {
            "id": 1,
            "name": "Aluno Teste",
            "email": "aluno@teste.com"
        }
        qr_code_base64 = self.student_card_page.generate_qr_code_base64(student_data, "Aprovado")
        self.assertTrue(
            isinstance(qr_code_base64, str),
            "Erro: O código QR gerado não é uma string."
        )
        self.assertTrue(
            len(qr_code_base64) > 0, 
            "Erro: O código QR gerado está vazio."
        )
        print("✔ Geração do código QR: Sucesso!")

    def test_show_student_card(self):
        """Teste para verificar se a carteirinha do aluno é exibida corretamente."""
        self.student_card_page.show_student_card()
        
        # Verifica se o método add foi chamado, garantindo que algo foi adicionado à página
        self.mock_page.add.assert_called()
        self.assertEqual(
            self.mock_page.update.call_count, 
            2, 
            f"Erro: O método update não foi chamado o número correto de vezes. Esperado 2, mas foi chamado {self.mock_page.update.call_count}."
        )
        print("✔ Exibição da carteirinha do aluno: Sucesso!")

if __name__ == "__main__":
    unittest.main()
