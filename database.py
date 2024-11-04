import sqlite3

def create_database():
    connection = sqlite3.connect('edupass.db')
    cursor = connection.cursor()

    # Criar tabela de instituições
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Criar tabela de alunos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

def register_institution(name, email, password):
    connection = sqlite3.connect('edupass.db')
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO institutions (name, email, password)
            VALUES (?, ?, ?)
        ''', (name, email, password))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()

def register_student(name, email, password):
    connection = sqlite3.connect('edupass.db')
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO students (name, email, password)
            VALUES (?, ?, ?)
        ''', (name, email, password))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()

def login_institution(email, password):
    connection = sqlite3.connect('edupass.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM institutions WHERE email = ? AND password = ?
    ''', (email, password))
    result = cursor.fetchone()
    connection.close()
    return result is not None

def login_student(email, password):
    connection = sqlite3.connect('edupass.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM students WHERE email = ? AND password = ?
    ''', (email, password))
    result = cursor.fetchone()
    connection.close()
    return result is not None

create_database()
