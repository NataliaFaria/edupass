class Student:
    def __init__(self, nome, cpf, email, celular):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.celular = celular

    def __str__(self):
        return f"Nome: {self.nome}, CPF: {self.cpf}, Email: {self.email}, Celular: {self.celular}"
