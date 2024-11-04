import sqlite3
import hashlib

class Database:
    def __init__(self, db_name="eduPass.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT,
                                cpf TEXT UNIQUE,
                                email TEXT UNIQUE,
                                celular TEXT,
                                password TEXT
                              )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS institutions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT UNIQUE,
                                endereco TEXT,
                                turno TEXT,
                                cursos TEXT
                              )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT,
                                instituicao_id INTEGER,
                                turno TEXT,
                                FOREIGN KEY(instituicao_id) REFERENCES institutions(id)
                              )''')
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_student(self, nome, cpf, email, celular, password):
        hashed_password = self.hash_password(password)
        try:
            self.cursor.execute("INSERT INTO students (nome, cpf, email, celular, password) VALUES (?, ?, ?, ?, ?)", 
                                (nome, cpf, email, celular, hashed_password))
            self.conn.commit()
            return True, "Usuário registrado com sucesso!"
        except sqlite3.IntegrityError as e:
            return False, "Erro: CPF ou e-mail já cadastrado."

    def verify_login(self, email, password):
        hashed_password = self.hash_password(password)
        self.cursor.execute("SELECT id FROM students WHERE email = ? AND password = ?", (email, hashed_password))
        user = self.cursor.fetchone()
        return user[0] if user else None
    

    def get_student_info(self, student_id):
        self.cursor.execute("SELECT nome, cpf, email, celular FROM students WHERE id = ?", (student_id,))
        return self.cursor.fetchone()
    
    def create_institution_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS institutions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT UNIQUE
                              )''')
        self.conn.commit()

    def add_institution(self, name):
        try:
            self.cursor.execute("INSERT INTO institutions (name) VALUES (?)", (name,))
            self.conn.commit()
            return True, "Instituição cadastrada com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Erro: Instituição já cadastrada."

    def add_course(self, name, institution_id):
        try:
            self.cursor.execute("INSERT INTO courses (name, institution_id) VALUES (?, ?)", (name, institution_id))
            self.conn.commit()
            return True, "Curso adicionado com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Erro: Curso já cadastrado ou instituição inválida."

    def get_institutions(self):
        self.cursor.execute("SELECT id, name FROM institutions")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
