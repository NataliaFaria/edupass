import sqlite3

class Database:
    def __init__(self, db_name='edupass.db'):
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        """Cria as tabelas no banco de dados, se não existirem"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Criar tabela de instituições
        cursor.execute('''CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            shift TEXT NOT NULL,
            courses TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')

        # Criar tabela de alunos
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            dob TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            password TEXT NOT NULL
        )''')

        connection.commit()
        connection.close()

    def register_institution(self, name, address, shift, courses, email, password):
        """Registra uma nova instituição no banco de dados"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            cursor.execute(
                '''INSERT INTO institutions (name, address, shift, courses, email, password) 
                VALUES (?, ?, ?, ?, ?, ?)''',
                (name, address, shift, courses, email, password)
            )
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            connection.close()

    def register_student(self, name, email, dob, cpf, phone, address, password):
        """Registra um novo aluno no banco de dados"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            cursor.execute(
                '''INSERT INTO students (name, email, dob, cpf, phone, address, password) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (name, email, dob, cpf, phone, address, password)
            )
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            connection.close()

    def login_institution(self, email, password):
        """Verifica se o login da instituição é válido"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT password FROM institutions WHERE email = ?''', (email,))
        result = cursor.fetchone()
        connection.close()
        if result and result[0] == password:  # Compara a senha diretamente
            return True
        return False

    def login_student(self, email, password):
        """Verifica se o login do aluno é válido e retorna os dados do aluno"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id, password FROM students WHERE email = ?''', (email,))
        result = cursor.fetchone()  # Retorna a tupla (id, senha) ou None
        connection.close()

        if result and result[1] == password:  # Compara a senha diretamente
            return result  # Retorna a tupla (id, senha) do aluno
        return None

    def get_student_by_id(self, student_id):
        """Obtém os dados do aluno pelo ID"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id, name, email, dob, cpf, phone, address FROM students WHERE id = ?''', (student_id,))
        student_data = cursor.fetchone()  # Retorna uma tupla ou None
        connection.close()

        if student_data:
            # Retorna os dados do aluno como um dicionário
            return {
                'id': student_data[0],
                'name': student_data[1],
                'email': student_data[2],
                'dob': student_data[3],
                'cpf': student_data[4],
                'phone': student_data[5],
                'address': student_data[6]
            }
        return None
