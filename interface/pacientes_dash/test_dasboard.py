import customtkinter as ctk
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interface.pacientes_dash.dashboard import DashboardPacienteContent  # ajusta o nome do ficheiro real


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Teste Dashboard Paciente")
        self.geometry("1200x700")

        # fundo
        self.configure(fg_color="#F4F6FB")

        # 🔥 ID de teste (tem de existir na tabela pacientes)
        id_paciente = 1

        DashboardPacienteContent(self, id_paciente)


# executar app
if __name__ == "__main__":
    app = App()
    app.mainloop()