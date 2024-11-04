import flet as ft

class ProfilePage:
    def build(self, page):
        def save_profile(event):
            # Lógica para salvar o perfil
            print("Perfil salvo com sucesso!")

        return ft.Column(
            controls=[
                ft.Text("Perfil do Usuário", size=24, weight="bold"),
                ft.TextField(label="Nome completo"),
                ft.TextField(label="E-mail"),
                ft.TextField(label="Data de nascimento"),
                ft.TextField(label="CPF"),
                ft.TextField(label="Telefone"),
                ft.ElevatedButton("Salvar", on_click=save_profile)
            ],
            alignment="center",
            horizontal_alignment="center",
        )
