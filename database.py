import sqlite3
from models.student import Student  # Certifique-se de que a classe Student está definida corretamente

class Database:
    def __init__(self, db_name='edupass.db'):
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Criar tabela de instituições
        cursor.execute('''CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')

        # Criar tabela de alunos
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')

        connection.commit()
        connection.close()

    def register_institution(self, name, email, password):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            cursor.execute('''INSERT INTO institutions (name, email, password) VALUES (?, ?, ?)''', (name, email, password))
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            connection.close()

    def register_student(self, name, email, password):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            cursor.execute('''INSERT INTO students (name, email, password) VALUES (?, ?, ?)''', (name, email, password))
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            connection.close()

    def login_institution(self, email, password):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM institutions WHERE email = ? AND password = ?''', (email, password))
        result = cursor.fetchone()
        connection.close()
        return result is not None

    def login_student(self, email, password):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM students WHERE email = ? AND password = ?''', (email, password))
        result = cursor.fetchone()
        connection.close()
        return result  # Retorna a tupla ou None

    def get_student_by_id(self, student_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id, name, email FROM students WHERE id = ?''', (student_id,))
        row = cursor.fetchone()
        connection.close()
        if row:
            return Student(*row)
        return None
