import customtkinter as ctk
import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(root_dir)
sys.path.insert(0, root_dir)

from interface.pacientes_dash.dashboard import DashboardPacienteContent

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Teste Dashboard Paciente")
        self.geometry("1200x700")
        self.configure(fg_color="#F4F6FB")

        id_paciente = 1
        DashboardPacienteContent(self, id_paciente)

if __name__ == "__main__":
    app = App()
    app.mainloop()
