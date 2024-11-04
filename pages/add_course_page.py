import flet as ft
from database import Database

class AddCoursePage(ft.UserControl):
    def __init__(self, page, user_id):
        super().__init__()
        self.page = page
        self.user_id = user_id
        self.db = Database()

    def add_course(self, e):
        nome = self.name_field.value
        instituicao_id = self.institution_field.value
        turno = self.turno_field.value

        self.db.cursor.execute("INSERT INTO courses (nome, instituicao_id, turno) VALUES (?, ?, ?)",
                                (nome, instituicao_id, turno))
        self.db.conn.commit()
        self.message.value = "Curso adicionado com sucesso!"
        self.update()

    def build(self):
        self.name_field = ft.TextField(label="Nome do Curso")
        self.institution_field = ft.TextField(label="ID da Instituição")
        self.turno_field = ft.TextField(label="Turno")
        self.message = ft.Text()

        return ft.Column(
            controls=[
                ft.Text("Adicionar Curso", size=24, weight="bold"),
                self.name_field,
                self.institution_field,
                self.turno_field,
                ft.ElevatedButton("Adicionar", on_click=self.add_course),
                self.message,
            ],
            alignment="center",
            horizontal_alignment="center",
        )
