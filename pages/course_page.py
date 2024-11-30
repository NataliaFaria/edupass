import flet as ft

class CoursesPage:
    def __init__(self, page: ft.Page, database, institution_id):
        self.page = page
        self.database = database
        self.institution_id = institution_id
        self.show_courses()

    def show_courses(self):
        # Buscar os cursos da instituição
        courses = self.database.get_courses_by_institution(self.institution_id)

        # Verificar se existem cursos cadastrados
        if not courses:
            self.page.clean()
            self.page.add(
                ft.Column(
                    controls=[
                        ft.Text("Nenhum curso cadastrado.", size=20, color="red"),
                        ft.TextButton("Voltar", on_click=self.go_back),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            return

        # Montar a lista de cursos
        course_list = ft.ListView(
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.icons.BOOK),
                    title=ft.Text(course["name"]),
                    subtitle=ft.Text(f"Duração: {course['duration']}"),
                )
                for course in courses
            ],
            spacing=10,
        )

        # Adicionar a lista à página
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Cursos Cadastrados", size=30),
                    course_list,
                    ft.TextButton("Voltar", on_click=self.go_back),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

    def go_back(self, e):
        """Retorna à página anterior"""
        self.page.go("/dashboard")  # Ajuste o caminho conforme sua aplicação
