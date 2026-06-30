import customtkinter as ctk
from interface.dashboard import DashboardAdmin
from database.database import listars_consultas_geral


class DashboardContent(ctk.CTkFrame):

    def __init__(self, parent, sessao):
        super().__init__(parent)
        self.sessao = sessao
        self.pack(fill="both", expand=True)

        self.build()

    def build(self):

        # =========================
        # HEADER
        # =========================
        header = ctk.CTkFrame(self, fg_color="#F5F7FB")
        header.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            header,
            text=f"Bem-vindo Dr(a). {self.sessao['nome']}",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        # =========================
        # TABELA CONSULTAS DO DIA
        # =========================
        self.table = ctk.CTkScrollableFrame(self)
        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_consultas()

    def load_consultas(self):

        for w in self.table.winfo_children():
            w.destroy()

        consultas = listar_consultas_geral()

        for c in consultas:

            consulta_id, paciente, medico, data, hora, estado = c

            card = ctk.CTkFrame(self.table, fg_color="#FFFFFF", corner_radius=10)
            card.pack(fill="x", pady=8)

            # INFO
            ctk.CTkLabel(
                card,
                text=f"Paciente: {paciente} | {hora}",
                font=("Segoe UI", 14, "bold")
            ).pack(anchor="w", padx=10, pady=5)

            ctk.CTkLabel(
                card,
                text=f"Estado: {estado}",
                text_color="gray"
            ).pack(anchor="w", padx=10)

            # BOTÕES
            actions = ctk.CTkFrame(card, fg_color="transparent")
            actions.pack(anchor="w", padx=10, pady=10)

            ctk.CTkButton(
                actions,
                text="Aceitar",
                fg_color="#28B463",
                width=100
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                actions,
                text="Registar",
                fg_color="#2E86C1",
                width=100
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                actions,
                text="Concluir",
                fg_color="#F39C12",
                width=100
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                actions,
                text="Histórico",
                fg_color="#6B7280",
                width=100
            ).pack(side="left", padx=5)
        nome, especialidade, horario = item

        card = ctk.CTkFrame(box, fg_color="#F4F6FB", corner_radius=8)
        card.pack(fill="x", padx=15, pady=6)

        ctk.CTkLabel(
            card,
            text=nome,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=10, pady=(8, 0))

        ctk.CTkLabel(
            card,
            text=especialidade,
            text_color="gray"
        ).pack(anchor="w", padx=10)

        ctk.CTkLabel(
            card,
            text=horario,
            text_color="#2E86C1"
        ).pack(anchor="w", padx=10, pady=(0, 8))