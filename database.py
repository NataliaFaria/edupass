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

    def close(self):
        self.conn.close()
