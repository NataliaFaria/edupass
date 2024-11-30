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
                        ft.TextButton("Voltar para o Painel", on_click=self.go_back),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            return

        # Montar a lista de cursos com botões de editar e excluir
        course_list = ft.ListView(
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.icons.BOOK),
                    title=ft.Text(course["name"]),
                    subtitle=ft.Text(f"Duração: {course['duration']}"),
                    trailing=ft.Row(
                        controls=[
                            ft.IconButton(ft.icons.EDIT, on_click=lambda e, course=course: self.edit_course(e, course)),
                            ft.IconButton(ft.icons.DELETE, on_click=lambda e, course=course: self.delete_course(e, course)),
                        ],
                        alignment=ft.MainAxisAlignment.END,  # Alinha os botões à direita
                        spacing=20,  # Espaçamento entre os botões
                    ),
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

    def edit_course(self, e, course):
        """Exibe o formulário para editar o curso selecionado"""
        # Campos de edição com valores preenchidos
        self.course_name_field = ft.TextField(label="Nome do Curso", value=course["name"])
        self.course_description_field = ft.TextField(label="Descrição do Curso", value=course["description"])
        self.course_duration_field = ft.TextField(label="Duração (ex: 6 meses)", value=course["duration"])

        self.success_message = ft.Text("", size=20, color=ft.colors.GREEN)
        self.error_message = ft.Text("", size=20, color=ft.colors.RED)

        # Função para salvar as alterações
        def save_changes(e):
            updated_name = self.course_name_field.value
            updated_description = self.course_description_field.value
            updated_duration = self.course_duration_field.value

            # Validar os campos
            if not updated_name or not updated_description or not updated_duration:
                self.success_message.value = ""
                self.error_message.value = "Todos os campos devem ser preenchidos!"
                self.page.update()
                return

            # Atualizar o curso no banco de dados
            if self.database.update_course(course["id"], updated_name, updated_description, updated_duration):
                self.success_message.value = "Curso atualizado com sucesso!"
                self.error_message.value = ""
                self.show_courses()  # Atualizar a lista de cursos
            else:
                self.success_message.value = ""
                self.error_message.value = "Erro ao atualizar o curso!"

            self.page.update()

        # Função para voltar à página de cursos
        def go_back(e):
            self.show_courses()

        # Exibir o formulário de edição
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Editar Curso", size=30),
                    self.course_name_field,
                    self.course_description_field,
                    self.course_duration_field,
                    self.success_message,
                    self.error_message,
                    ft.ElevatedButton("Salvar Alterações", on_click=save_changes),
                    ft.TextButton("Voltar", on_click=go_back),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def delete_course(self, e, course):
        """Exclui o curso após confirmação"""
        # Função de confirmação de exclusão
        def confirm_delete(e):
            if self.database.delete_course(course["id"]):
                self.show_courses()  # Atualizar a lista de cursos após exclusão
            else:
                # Mostrar mensagem de erro
                self.page.add(ft.Text("Erro ao excluir o curso.", color=ft.colors.RED))

        def cancel_delete(e):
            self.page.clean()
            self.show_courses()  # Voltar à lista de cursos

        # Exibir a confirmação de exclusão
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text(f"Tem certeza que deseja excluir o curso '{course['name']}'?", size=20),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton("Confirmar", on_click=confirm_delete),
                            ft.ElevatedButton("Cancelar", on_click=cancel_delete),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

    def go_back(self, e):
        """Retorna à página anterior"""
        self.page.go("/dashboard")  # Ajuste o caminho conforme sua aplicação
