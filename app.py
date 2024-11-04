# app.py

import flet as ft
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.profile_page import ProfilePage
from database import Database

def main(page: ft.Page):
    page.title = "EduPass - Carteira Escolar"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    db = Database()

    def go_to_login_page():
        page.controls.clear()
        page.add(LoginPage(page, on_login_success, go_to_register_page))
        page.update()

    def go_to_register_page():
        page.controls.clear()
        page.add(RegisterPage(page, go_to_login_page))
        page.update()

    def on_login_success(user_id):
        page.controls.clear()
        page.add(ProfilePage(page, user_id))  # Carrega a ProfilePage após o login
        page.update()

    go_to_login_page()

ft.app(target=main)
