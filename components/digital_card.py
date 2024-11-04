import flet as ft

class DigitalCard(ft.UserControl):
    def __init__(self, student_info):
        super().__init__()
        self.student_info = student_info

    def build(self):
        return ft.Column([
            ft.Text(f"Nome: {self.student_info['nome']}"),
            ft.Text(f"Curso: {self.student_info['curso']}"),
            ft.QRCode(self.student_info['qr_data']),
            ft.Button("Exportar Carteirinha")
        ])
