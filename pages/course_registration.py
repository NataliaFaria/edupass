import flet as ft
from database import Database

class CourseRegistrationPage:
    def __init__(self, page: ft.Page, dashboard_page: object, institution_id: int):
        self.page = page
        self.dashboard = dashboard_page
        self.page.clean()
        self.page.title = "Cadastro de Cursos"
        self.database = Database()
        self.institution_id = institution_id

        self.create_course_registration_page()

    def create_course_registration_page(self):
        # Campos de entrada
        self.course_name_field = ft.TextField(label="Nome do Curso")
        self.course_description_field = ft.TextField(label="Descrição do Curso")
        self.course_duration_field = ft.TextField(label="Duração (ex: 6 meses)")

        # Mensagens de feedback
        self.success_message = ft.Text("", size=20, color=ft.colors.GREEN)
        self.error_message = ft.Text("", size=20, color=ft.colors.RED)

        # Função para voltar ao painel de controle
        def go_back(e):
            self.dashboard.create_dashboard()
            self.page.update()

        # Função para registrar curso
        def register_course(e):
            course_name = self.course_name_field.value
            course_description = self.course_description_field.value
            course_duration = self.course_duration_field.value

            if not course_name or not course_description or not course_duration:
                self.success_message.value = ""
                self.error_message.value = "Todos os campos devem ser preenchidos!"
                self.page.update()
                return

            # Usa o ID da instituição logada
            if self.database.register_course(course_name, self.institution_id, course_duration):
                self.course_name_field.value = ""
                self.course_description_field.value = ""
                self.course_duration_field.value = ""
                self.success_message.value = "Curso cadastrado com sucesso!"
                self.error_message.value = ""
            else:
                self.success_message.value = ""
                self.error_message.value = "Erro ao cadastrar curso!"
            
            self.page.update()

        # Adicionar componentes ao layout
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Cadastro de Curso", size=30),
                    self.course_name_field,
                    self.course_description_field,
                    self.course_duration_field,
                    self.success_message,
                    self.error_message,
                    ft.ElevatedButton("Cadastrar Curso", on_click=register_course),
                    ft.TextButton("Voltar para o Painel", on_click=go_back),  # Botão de voltar
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )
