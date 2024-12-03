import flet as ft
from database import Database


class InstitutionRegistrationPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.clean()
        self.page.title = "Cadastro - Instituição"
        self.database = Database()

        self.create_registration_page()

    def create_registration_page(self):
        # Campos do formulário
        name_field = ft.TextField(label="Nome da Instituição")
        address_field = ft.TextField(label="Endereço")
        shift_field = ft.TextField(label="Turno (Ex: Matutino, Vespertino, Noturno)")
        email_field = ft.TextField(label="Email")
        password_field = ft.TextField(label="Senha", password=True)

        def navigate_to_home(e):
            """Navegar para a página inicial."""
            self.page.go("/")

        def is_valid_email(email):
            """Valida se o e-mail é válido."""
            import re
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return re.match(pattern, email) is not None

        def register(e):
            """Realiza o registro da instituição."""
            # Resetar mensagens de erro
            name_field.error_text = None
            address_field.error_text = None
            shift_field.error_text = None
            email_field.error_text = None
            password_field.error_text = None

            # Obter os valores dos campos
            name = name_field.value.strip()
            address = address_field.value.strip()
            shift = shift_field.value.strip()
            email = email_field.value.strip()
            password = password_field.value.strip()

            # Validações
            is_valid = True
            if not name:
                name_field.error_text = "O nome da instituição é obrigatório."
                is_valid = False
            if not address:
                address_field.error_text = "O endereço é obrigatório."
                is_valid = False
            if not shift:
                shift_field.error_text = "O turno é obrigatório."
                is_valid = False
            if not email or not is_valid_email(email):
                email_field.error_text = "Email inválido."
                is_valid = False
            if not password:
                password_field.error_text = "A senha é obrigatória."
                is_valid = False

            # Atualizar os campos com mensagens de erro
            name_field.update()
            address_field.update()
            shift_field.update()
            email_field.update()
            password_field.update()

            if not is_valid:
                return  # Parar o registro se houver erros

            # Tentar cadastrar a instituição no banco de dados
            if self.database.register_institution(name, address, shift, email, password):
                self.page.go("/institution_login")  # Navegar para a página de login após o cadastro
            else:
                self.page.add(ft.Text("Email já cadastrado!", color=ft.colors.RED))

        # Adicionar componentes ao layout
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Cadastro - Instituição", size=30),
                    name_field,
                    address_field,
                    shift_field,
                    email_field,
                    password_field,
                    ft.ElevatedButton("Cadastrar", on_click=register),
                    ft.TextButton("Já tem uma conta? Login", on_click=lambda e: self.page.go("/institution_login")),
                    ft.TextButton("Voltar para Home", on_click=navigate_to_home),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )
