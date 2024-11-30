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
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')

        # Criar tabela de cursos
        cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            institution_id INTEGER,
            duration TEXT NOT NULL, 
            FOREIGN KEY (institution_id) REFERENCES institutions(id)
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

        # Tabela de relacionamento entre alunos e cursos
        cursor.execute('''CREATE TABLE IF NOT EXISTS student_courses (
            student_id INTEGER,
            course_id INTEGER,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )''')

        connection.commit()
        connection.close()

    def register_institution(self, name, address, shift, email, password):
        """Registra uma nova instituição no banco de dados"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            cursor.execute(
                '''INSERT INTO institutions (name, address, shift, email, password) 
                VALUES (?, ?, ?, ?, ?)''',
                (name, address, shift, email, password)
            )
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            connection.close()

    def register_course(self, name, institution_id, duration):
        """Registra um curso de uma instituição"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            cursor.execute(
                '''INSERT INTO courses (name, institution_id, duration) 
                VALUES (?, ?, ?)''',  # Corrigido para incluir o campo 'duration'
                (name, institution_id, duration)  # Passando todos os parâmetros
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

    def register_student_in_course(self, student_id, course_id):
        """Inscreve um aluno em um curso"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            cursor.execute(
                '''INSERT INTO student_courses (student_id, course_id) 
                VALUES (?, ?)''',
                (student_id, course_id)
            )
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            connection.close()

    def login_institution(self, email, password):
        """Verifica se o login da instituição é válido e retorna o ID"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id, password FROM institutions WHERE email = ?''', (email,))
        result = cursor.fetchone()
        connection.close()
        if result and result[1] == password:
            return result[0]  # Retorna o ID da instituição
        return None


    def login_student(self, email, password):
        """Verifica se o login do aluno é válido e retorna os dados do aluno"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id, password FROM students WHERE email = ?''', (email,))
        result = cursor.fetchone()
        connection.close()

        if result and result[1] == password:
            return result
        return None

    def get_institution_id_by_email(self, email):
        """Obtém o ID da instituição pelo e-mail"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id FROM institutions WHERE email = ?''', (email,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]  # Retorna o ID da instituição
        return None


    def get_courses_by_institution(self, institution_id):
        """Retorna os cursos cadastrados por uma instituição"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            '''SELECT id, name, duration FROM courses WHERE institution_id = ?''',
            (institution_id,)
        )
        courses = cursor.fetchall()
        connection.close()
        return [
            {"id": course[0], "name": course[1], "duration": course[2]}
            for course in courses
        ]

