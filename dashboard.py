import flet as ft

def dashboard_page(page: ft.Page, user_type: str):
    page.clean()
    page.title = "Painel de Controle"

    if user_type == "institution":
        content = ft.Column(
            controls=[
                ft.Text("Bem-vindo ao painel da Instituição!", size=30),
                ft.TextButton("Gerenciar Alunos", on_click=lambda e: page.add(ft.Text("Funcionalidade de Gerenciamento de Alunos"))),
                ft.TextButton("Visualizar Relatórios", on_click=lambda e: page.add(ft.Text("Funcionalidade de Relatórios"))),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    else:  # user_type == "student"
        content = ft.Column(
            controls=[
                ft.Text("Bem-vindo ao painel do Aluno!", size=30),
                ft.TextButton("Meus Cursos", on_click=lambda e: page.add(ft.Text("Lista de Cursos Inscritos"))),
                ft.TextButton("Meu Progresso", on_click=lambda e: page.add(ft.Text("Progresso do Aluno"))),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

    # logout (precisa ser ajustado)
    home_button = ft.TextButton("Logout", on_click=lambda e: page.go("/"))

    # Adicionando os controles ao page
    page.add(
        ft.Column(
            controls=[content, home_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )
