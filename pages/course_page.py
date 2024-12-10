import flet as ft

class CoursesPage:
    def __init__(self, page: ft.Page, dashboard_page, database):
        self.page = page
        self.dashboard_page = dashboard_page
        self.database = database
        self.institution_id = dashboard_page.institution_id
        self.course_name_field = None
        self.course_duration_field = None
        self.create_course_page()

    def create_course_page(self, e=None):
        """Cria a página com a lista de cursos existentes e opções de registro"""
        self.page.clean()
        
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Cursos Cadastrados", size=30),
                    self.create_course_list(),
                    # ft.ElevatedButton("Registrar Novo Curso", on_click=self.show_course_registration_form),
                    ft.TextButton("Voltar", on_click=self.go_back),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def create_course_list(self):
        """Cria a lista de cursos cadastrados pela instituição"""
        courses = self.database.get_courses_by_institution(self.institution_id)
        
        if not courses:
            return ft.Text("Nenhum curso cadastrado no momento.", size=20, italic=True, color=ft.colors.GREY)

        course_controls = []
        for course in courses:
            course_controls.append(
                ft.Row(
                    controls=[
                        ft.Text(course["name"], size=20),
                        ft.Text(course["duration"], size=16),
                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, course_id=course["id"]: self.show_edit_course_form(course_id)),
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, course_id=course["id"]: self.confirm_delete_course(course_id)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                )
            )

        return ft.Column(controls=course_controls)

    # def show_course_registration_form(self, e):
    #     """Exibe o formulário de registro de um novo curso"""
    #     self.page.clean()

    #     self.course_name_field = ft.TextField(label="Nome do Curso", autofocus=True)
    #     self.course_duration_field = ft.TextField(label="Duração do Curso")

    #     self.page.add(
    #         ft.Column(
    #             controls=[
    #                 ft.Text("Registrar Novo Curso", size=30),
    #                 self.course_name_field,
    #                 self.course_duration_field,
    #                 ft.ElevatedButton("Salvar Curso", on_click=self.register_course),
    #                 ft.TextButton("Voltar", on_click=self.create_course_page),
    #             ],
    #             alignment=ft.MainAxisAlignment.CENTER,
    #             spacing=20,
    #         )
    #     )

    def register_course(self, e):
        """Método para registrar um novo curso no banco de dados"""
        name = self.course_name_field.value
        duration = self.course_duration_field.value

        if self.database.register_course(name, "", self.institution_id, duration):
            self.create_course_page()  # Recarrega a página com os dados atualizados
        else:
            pass

    def show_edit_course_form(self, course_id):
        """Exibe o formulário de edição de um curso existente"""
        course = self.database.get_course_by_id(course_id)

        self.page.clean()

        self.course_name_field = ft.TextField(label="Nome do Curso", value=course["name"], autofocus=True)
        self.course_duration_field = ft.TextField(label="Duração do Curso", value=course["duration"])

        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Editar Curso", size=30),
                    self.course_name_field,
                    self.course_duration_field,
                    ft.ElevatedButton("Salvar Alterações", on_click=lambda e: self.save_course_edits(course_id)),
                    ft.TextButton("Voltar", on_click=self.create_course_page),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def save_course_edits(self, course_id):
        """Salva as alterações feitas em um curso"""
        name = self.course_name_field.value
        duration = self.course_duration_field.value

        if self.database.update_course(course_id, name, duration):
            self.create_course_page()  # Atualiza a lista de cursos
        else:
            pass

    def confirm_delete_course(self, course_id):
        """Confirma a exclusão de um curso"""
        self.page.clean()

        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Tem certeza que deseja excluir este curso?", size=20),
                    ft.ElevatedButton("Sim, Excluir", on_click=lambda e: self.delete_course(course_id)),
                    ft.ElevatedButton("Não, Voltar", on_click=self.create_course_page),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def delete_course(self, course_id):
        """Exclui um curso do banco de dados"""
        if self.database.delete_course(course_id):
            self.create_course_page()  # Atualiza a lista de cursos após exclusão
        else:
            pass

    def go_back(self, e):
        """Volta para o painel da instituição"""
        from .dashboard import DashboardPage
        DashboardPage(self.page, user_type="institution", institution_id=self.institution_id)
