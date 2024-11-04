import flet as ft
from database import Database

class InstitutionRegisterPage(ft.UserControl):
    def __init__(self, page, go_to_login_page):
        super().__init__()
        self.page = page
        self.go_to_login_page = go_to_login_page
        self.db = Database()

    def register_institution(self, e):
        nome = self.name_field.value
        endereco = self.endereco_field.value
        turno = self.turno_field.value
        cursos = self.cursos_field.value

        try:
            self.db.cursor.execute("INSERT INTO institutions (nome, endereco, turno, cursos) VALUES (?, ?, ?, ?)",
                                    (nome, endereco, turno, cursos))
            self.db.conn.commit()
            self.message.value = "Instituição cadastrada com sucesso!"
        except sqlite3.IntegrityError:
            self.message.value = "Erro: Instituição já cadastrada."
        
        self.update()

    def build(self):
        self.name_field = ft.TextField(label="Nome da Instituição")
        self.endereco_field = ft.TextField(label="Endereço")
        self.turno_field = ft.TextField(label="Turno")
        self.cursos_field = ft.TextField(label="Cursos ofertados (separados por vírgula)")
        self.message = ft.Text()

        return ft.Column(
            controls=[
                ft.Text("Cadastro de Instituição", size=24, weight="bold"),
                self.name_field,
                self.endereco_field,
                self.turno_field,
                self.cursos_field,
                ft.ElevatedButton("Cadastrar", on_click=self.register_institution),
                self.message,
                ft.TextButton("Voltar ao Login", on_click=lambda _: self.go_to_login_page())
            ],
            alignment="center",
            horizontal_alignment="center",
        )
