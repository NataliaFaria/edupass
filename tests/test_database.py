import unittest
import os
import sys
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Configura o ambiente de teste com um banco de dados temporário."""
        self.test_db_name = 'test_edupass.db'
        self.db = Database(self.test_db_name)

    def tearDown(self):
        """Remove o banco de dados temporário após os testes."""
        if os.path.exists(self.test_db_name):
            os.remove(self.test_db_name)

    def test_register_institution(self):
        """Teste para verificar o registro de uma instituição."""
        result = self.db.register_institution(
            name="Instituto de Teste",
            address="Rua Teste, 123",
            shift="Manhã",
            email="teste@instituto.com",
            password="senha123"
        )
        self.assertTrue(result, "Erro: A instituição não foi registrada corretamente.")
        print("✔ Registro de instituição: Sucesso!")

    def test_login_institution(self):
        """Teste para autenticação de uma instituição."""
        self.db.register_institution(
            name="Instituto de Teste",
            address="Rua Teste, 123",
            shift="Manhã",
            email="teste@instituto.com",
            password="senha123"
        )
        institution_id = self.db.login_institution("teste@instituto.com", "senha123")
        self.assertIsNotNone(
            institution_id,
            "Erro: Falha no login da instituição com email 'teste@instituto.com'."
        )
        print(f"✔ Login da instituição com email 'teste@instituto.com': Sucesso!")

    def test_register_course(self):
        """Teste para verificar o registro de um curso."""
        self.db.register_institution(
            name="Instituto de Teste",
            address="Rua Teste, 123",
            shift="Manhã",
            email="curso@instituto.com",
            password="senha123"
        )
        institution_id = self.db.get_institution_id_by_email("curso@instituto.com")
        result = self.db.register_course("Curso de Teste", institution_id, "6 meses")
        self.assertTrue(
            result,
            f"Erro: O curso 'Curso de Teste' não foi registrado para a instituição ID {institution_id}."
        )
        print(f"✔ Registro do curso 'Curso de Teste' para a instituição ID {institution_id}: Sucesso!")

    def test_register_and_login_student(self):
        """Teste para registrar e autenticar um aluno."""
        self.db.register_institution(
            name="Instituto de Teste",
            address="Rua Teste, 123",
            shift="Manhã",
            email="teste@instituto.com",
            password="senha123"
        )
        institution_id = self.db.get_institution_id_by_email("teste@instituto.com")
        course_id = self.db.register_course("Curso de Teste", institution_id, "6 meses")
        
        result = self.db.register_student(
            name="Aluno Teste",
            email="aluno@teste.com",
            dob="2000-01-01",
            cpf="12345678900",
            phone="999999999",
            address="Rua Aluno, 123",
            password="senhaAluno",
            institution_id=institution_id,
            course_id=1
        )
        self.assertTrue(
            result,
            f"Erro: O aluno 'Aluno Teste' não foi registrado no curso ID {course_id}."
        )
        print("✔ Registro do aluno 'Aluno Teste': Sucesso!")

        student_id = self.db.login_student("aluno@teste.com", "senhaAluno")
        self.assertIsNotNone(
            student_id,
            "Erro: Falha no login do aluno com email 'aluno@teste.com'."
        )
        print(f"✔ Login do aluno com email 'aluno@teste.com': Sucesso!")

    def test_update_course(self):
        """Teste para atualização de um curso."""
        self.db.register_institution(
            name="Instituto de Teste",
            address="Rua Teste, 123",
            shift="Manhã",
            email="curso@instituto.com",
            password="senha123"
        )
        institution_id = self.db.get_institution_id_by_email("curso@instituto.com")
        self.db.register_course("Curso Original", institution_id, "6 meses")
        course_id = 1  # Como estamos testando em um banco temporário, será o primeiro curso

        result = self.db.update_course(course_id, "Curso Atualizado", "1 ano")
        self.assertTrue(
            result,
            f"Erro: O curso ID {course_id} não foi atualizado para 'Curso Atualizado' com duração '1 ano'."
        )
        print(f"✔ Atualização do curso ID {course_id}: Sucesso!")

    def test_delete_course(self):
        """Teste para exclusão de um curso."""
        self.db.register_institution(
            name="Instituto de Teste",
            address="Rua Teste, 123",
            shift="Manhã",
            email="curso@instituto.com",
            password="senha123"
        )
        institution_id = self.db.get_institution_id_by_email("curso@instituto.com")
        self.db.register_course("Curso para Deletar", institution_id, "6 meses")
        course_id = 1

        result = self.db.delete_course(course_id)
        self.assertTrue(
            result,
            f"Erro: O curso ID {course_id} não foi deletado."
        )
        print(f"✔ Exclusão do curso ID {course_id}: Sucesso!")

if __name__ == "__main__":
    unittest.main()
