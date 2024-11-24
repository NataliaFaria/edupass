import flet as ft
from database import Database

class CourseRegistrationPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.clean()
        self.page.title = "Cadastro de Cursos"
        self.database = Database()

        self.create_course_registration_page()

    def create_course_registration_page(self):
        # Campos do formulário (agora como atributos para poder ser usados dentro de métodos)
        self.course_name_field = ft.TextField(label="Nome do Curso")
        self.course_description_field = ft.TextField(label="Descrição do Curso")
        self.course_duration_field = ft.TextField(label="Duração (ex: 6 meses)")

        # Mensagem de sucesso ou erro
        self.success_message = ft.Text("", size=20, color=ft.colors.GREEN)
        self.error_message = ft.Text("", size=20, color=ft.colors.RED)

        def navigate_to_dashboard(e):
            # Voltar para o painel de controle da instituição
            print("Dashboard")
            self.page.go("/dashboard")
            self.page.update()


        def register_course(e):
            # Obter os valores dos campos
            course_name = self.course_name_field.value
            course_description = self.course_description_field.value
            course_duration = self.course_duration_field.value
            
            # Assumindo que o institution_id é obtido de algum lugar, por exemplo:
            institution_id = 1  # Exemplo de ID fixo de instituição. Ajuste conforme necessário.

            # Validação simples dos campos
            if not course_name or not course_description or not course_duration:
                self.success_message.value = ""  # Limpar mensagem de sucesso
                self.error_message.value = "Todos os campos devem ser preenchidos!"
                self.page.update()
                return

            # Tentar registrar o curso no banco de dados
            if self.database.register_course(course_name, institution_id, course_duration):
                # Limpar os campos após o sucesso
                self.course_name_field.value = ""
                self.course_description_field.value = ""
                self.course_duration_field.value = ""
                
                # Mostrar mensagem de sucesso
                self.success_message.value = "Curso cadastrado com sucesso!"
                self.error_message.value = ""  # Limpar a mensagem de erro
            else:
                # Caso haja erro no cadastro, exibir a mensagem de erro
                self.success_message.value = ""  # Limpar a mensagem de sucesso
                self.error_message.value = "Erro ao cadastrar curso!"

            # Atualizar a página com as novas mensagens
            self.page.update()

        # Adicionar componentes ao layout
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Cadastro de Curso", size=30),
                    self.course_name_field,
                    self.course_description_field,
                    self.course_duration_field,
                    self.success_message,  # Adicionar a mensagem de sucesso ao layout
                    self.error_message,  # Adicionar a mensagem de erro ao layout
                    ft.ElevatedButton("Cadastrar Curso", on_click=register_course),
                    ft.TextButton("Voltar para o Painel", on_click=navigate_to_dashboard),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )
