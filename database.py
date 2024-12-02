import sqlite3
import bcrypt

class Database:
    def __init__(self, db_name='edupass.db'):
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        """Cria as tabelas no banco de dados, se não existirem"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        
        cursor.execute('''CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            shift TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')

        
        cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            institution_id INTEGER,
            duration TEXT NOT NULL, 
            FOREIGN KEY (institution_id) REFERENCES institutions(id)
        )''')

        
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            dob TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            password TEXT NOT NULL,
            institution_id INTEGER,  
            course_id INTEGER,  
            FOREIGN KEY (institution_id) REFERENCES institutions(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )''')

        
        cursor.execute('''CREATE TABLE IF NOT EXISTS student_courses (
            student_id INTEGER,
            course_id INTEGER,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            institution_id INTEGER,
            file_path TEXT NOT NULL,
            description TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Pendente',
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (institution_id) REFERENCES institutions(id)
        )''')

        connection.commit()
        connection.close()

    def register_institution(self, name, address, shift, email, password):
        """Registra uma nova instituição no banco de dados com senha criptografada"""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            cursor.execute(
                '''INSERT INTO institutions (name, address, shift, email, password) 
                VALUES (?, ?, ?, ?, ?)''',
                (name, address, shift, email, hashed_password)
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
                VALUES (?, ?, ?)''',  
                (name, institution_id, duration)
            )
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            connection.close()


    def register_student(self, name, email, dob, cpf, phone, address, password, institution_id, course_id):
        """Registra um novo aluno com senha criptografada"""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            cursor.execute(
                '''INSERT INTO students (name, email, dob, cpf, phone, address, password, institution_id, course_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (name, email, dob, cpf, phone, address, hashed_password, institution_id, course_id)
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
        """Verifica o login da instituição com senha criptografada"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id, password FROM institutions WHERE email = ?''', (email,))
        result = cursor.fetchone()
        connection.close()
        if result and bcrypt.checkpw(password.encode('utf-8'), result[1]):
            return result[0]  # Retorna o ID da instituição
        return None

    def login_student(self, email, password):
        """Verifica o login do aluno com senha criptografada"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id, password FROM students WHERE email = ?''', (email,))
        result = cursor.fetchone()
        connection.close()
        if result and bcrypt.checkpw(password.encode('utf-8'), result[1]):
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
    
    def get_student_by_id(self, student_id):
        """Obtém os dados de um aluno pelo ID"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id, name, email, dob, cpf, phone, address FROM students WHERE id = ?''', (student_id,))
        result = cursor.fetchone()
        connection.close()

        if result:
            return {
                "id": result[0],
                "name": result[1],
                "email": result[2],
                "dob": result[3],
                "cpf": result[4],
                "phone": result[5],
                "address": result[6]
            }
        return None



    def get_courses_by_institution(self, institution_id):
        """Retorna os cursos cadastrados por uma instituição"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        print(f"Consultando cursos para a instituição com ID: {institution_id}")
        
        cursor.execute(
            '''SELECT id, name, duration FROM courses WHERE institution_id = ?''',
            (institution_id,)
        )
        courses = cursor.fetchall()
        connection.close()
        
        print(f"Consultando cursos para o ID {institution_id}. Cursos retornados: {courses}")
        if not courses:
            print(f"Nenhum curso encontrado para o ID {institution_id}. Verifique os dados no banco.")
            
        return [
            {"id": course[0], "name": course[1], "duration": course[2]}
            for course in courses
        ]



    
    def delete_course(self, course_id):
        
        sql = "DELETE FROM courses WHERE id = ?"
        
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (course_id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Erro ao excluir curso: {e}")
            return False 
        
    def update_course(self, course_id, name, description, duration):
        
        sql = """
            UPDATE courses
            SET name = ?, description = ?, duration = ?
            WHERE id = ?
        """
        
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (name, description, duration, course_id))
            self.db.commit()
            return True 
        except Exception as e:
            print(f"Erro ao atualizar curso: {e}")
            return False 
    
    def get_all_institutions(self):
        """Obtém todas as instituições cadastradas"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id, name FROM institutions''')
        institutions = cursor.fetchall()
        connection.close()
        return [{"id": institution[0], "name": institution[1]} for institution in institutions]

    def upload_document(self, student_id, institution_id, file_path, description):
        print(institution_id)
        """Realiza o upload de um novo documento para o aluno"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            cursor.execute(
                '''INSERT INTO documents (student_id, institution_id, file_path, description) 
                VALUES (?, ?, ?, ?)''',
                (student_id, institution_id, file_path, description)
            )
            connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Erro ao registrar documento: {e}")
            return False
        finally:
            connection.close()

    def get_documents_for_institution(self, institution_id):
        """Recupera os documentos enviados para a instituição"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM documents WHERE institution_id = ?''', (institution_id,))
        documents = cursor.fetchall()
        connection.close()
        return documents
    
    def get_students_by_institution(self, institution_id):
        """Retorna os alunos cadastrados em uma instituição e seus documentos."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            '''
            SELECT s.id, s.name, s.email, d.file_path, d.description, d.status
            FROM students s
            LEFT JOIN documents d ON s.id = d.student_id
            WHERE s.institution_id = ?
            ''', 
            (institution_id,)
        )
        students = cursor.fetchall()
        connection.close()
        return [
            {
                "student_id": student[0],
                "name": student[1],
                "email": student[2],
                "file_path": student[3],
                "description": student[4],
                "status": student[5]
            }
            for student in students
        ]

    def update_document_status(self, document_id, status):
        """Atualiza o status de um documento."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            '''
            UPDATE documents
            SET status = ?
            WHERE id = ?
            ''', 
            (status, document_id)
        )
        connection.commit()
        connection.close()
        return cursor.rowcount > 0
    
    def get_institution_id(self, student_id):
        """Obtém o institution_id com base no student_id"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        try:
            cursor.execute('''SELECT institution_id FROM students WHERE id = ?''', (student_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        except sqlite3.Error as e:
            print(f"Erro ao buscar institution_id: {e}")
            return None
        finally:
            connection.close()
    
    def get_documents_for_student(self, student_id):
        """Recupera os documentos enviados para um aluno específico"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM documents WHERE student_id = ?''', (student_id,))
        documents = cursor.fetchall()
        connection.close()
        return documents

