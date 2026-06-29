import customtkinter as ctk
from database.database import consultas_hoje, consultar_prioridade, consultar_agenda_medicos
from interface._base import _topbar_base


class DashboardContent:

    def __init__(self, parent):
        self.parent = parent
        _topbar_base(parent, "Painel Principal")
        self.cards()
        self.center_area()

    def cards(self):
        frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(30, 20))
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        def card(col, title, value, color):
            c = ctk.CTkFrame(frame, fg_color=color, corner_radius=18, width=260, height=180)
            c.grid(row=0, column=col, padx=12, sticky="nsew")
            c.grid_propagate(False)
            inner = ctk.CTkFrame(c, fg_color="transparent")
            inner.pack(expand=True, fill="both", padx=20, pady=20)
            ctk.CTkLabel(inner, text=title, text_color="white", font=("Segoe UI", 15)).pack(anchor="w", padx=20, pady=(20, 5))
            ctk.CTkLabel(inner, text=value, text_color="white", font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=20)

        card(0, "Consultas Hoje", "48", "#2E86C1")
        card(1, "Médicos", "12", "#28B463")
        card(2, "Urgências", "18", "#E74C3C")
        card(3, "Tempo Médio", "32 min", "#F39C12")

    def center_area(self):
        center = ctk.CTkFrame(self.parent, fg_color="transparent")
        center.pack(fill="both", expand=True, padx=20, pady=15)
        center.grid_columnconfigure(0, weight=2)
        center.grid_columnconfigure(1, weight=1)
        center.grid_columnconfigure(2, weight=1)
        center.grid_rowconfigure(0, weight=1)
        self.table_ui(center)
        self.prioridade_ui(center)
        self.agenda_ui(center)

    def table_ui(self, parent):
        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        box.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(box, text="Consultas de Hoje", font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=10)
        header = ctk.CTkFrame(box, fg_color="transparent")
        header.pack(fill="x", padx=20)
        for c in ["Paciente", "Médico", "Hora", "Prioridade", "Estado"]:
            ctk.CTkLabel(header, text=c, width=120, anchor="w").pack(side="left")
        for p, m, h, pr, st in consultas_hoje():
            row = ctk.CTkFrame(box, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=3)
            for val, w in [(p, 120), (m, 120), (h, 80), (pr, 100), (st, 100)]:
                ctk.CTkLabel(row, text=val, width=w, anchor="w").pack(side="left")

    def prioridade_ui(self, parent):
        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        box.grid(row=0, column=1, sticky="nsew", padx=10)
        ctk.CTkLabel(box, text="Consultas por Prioridade", font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=10)
        for prioridade, total in consultar_prioridade():
            row = ctk.CTkFrame(box, fg_color="#F4F6FB")
            row.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(row, text=prioridade, width=120, anchor="w", font=("Segoe UI", 13, "bold")).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"{total} consultas", anchor="w").pack(side="left")
        ctk.CTkLabel(box, text="").pack(pady=5)

    def agenda_ui(self, parent):
        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        box.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(box, text="Agenda dos Médicos", font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=10)
        for nome, especialidade, horario in consultar_agenda_medicos():
            card = ctk.CTkFrame(box, fg_color="#F4F6FB", corner_radius=8)
            card.pack(fill="x", padx=15, pady=6)
            ctk.CTkLabel(card, text=nome, font=("Segoe UI", 13, "bold"), anchor="w").pack(anchor="w", padx=10, pady=(8, 0))
            ctk.CTkLabel(card, text=especialidade, text_color="gray").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=horario, text_color="#2E86C1").pack(anchor="w", padx=10, pady=(0, 8))
