import customtkinter as ctk
from interface._base import _topbar_base
from database.database import listar_consultas_paciente

class MinhasConsultasContent:

    def __init__(self, parent, id_paciente):
        self.parent = parent
        self.id_paciente = id_paciente

        _topbar_base(parent, "Minhas Consultas")
        self.build_ui()

    def build_ui(self):
        box = ctk.CTkFrame(self.parent, fg_color="#F4F6FB")
        box.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(box, text="Minhas Consultas",
                     font=("Segoe UI", 24, "bold"),
                     text_color="#0B2A4A").pack(anchor="w", pady=(0, 10))

        body = ctk.CTkScrollableFrame(box, fg_color="white", corner_radius=12)
        body.pack(fill="both", expand=True)

        consultas = listar_consultas_paciente(self.id_paciente)

        if not consultas:
            ctk.CTkLabel(body, text="Sem consultas agendadas.",
                         font=("Segoe UI", 14), text_color="#667085").pack(pady=20)
            return

        header = ctk.CTkFrame(body, fg_color="#F4F6FB")
        header.pack(fill="x", pady=(0, 10))

        for texto, largura in [
            ("Médico", 160),
            ("Especialidade", 140),
            ("Data", 100),
            ("Hora", 80),
            ("Estado", 120),
        ]:
            ctk.CTkLabel(header, text=texto, width=largura,
                         anchor="w", font=("Segoe UI", 12, "bold"),
                         text_color="#475467").pack(side="left", padx=(0, 5))

        for nome, especialidade, data, hora, estado in consultas:
            row = ctk.CTkFrame(body, fg_color="white", corner_radius=10)
            row.pack(fill="x", pady=4, padx=10)
            row.pack_propagate(False)

            for valor, largura in [
                (nome, 160),
                (especialidade, 140),
                (data, 100),
                (hora, 80),
                (estado, 120),
            ]:
                ctk.CTkLabel(row, text=str(valor), width=largura,
                             anchor="w", font=("Segoe UI", 12),
                             text_color="#334155").pack(side="left", padx=(0, 5), pady=12)
