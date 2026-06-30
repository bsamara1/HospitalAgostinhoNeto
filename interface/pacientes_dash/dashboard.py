import customtkinter as ctk
from interface._base import _topbar_base

from database.database import (
    proxima_consulta,
    total_consultas,
    contar_notificacoes,
    estado_triagem,
)


class DashboardPacienteContent:

    def __init__(self, parent, id_paciente):
        self.parent = parent
        self.id_paciente = id_paciente

        _topbar_base(parent, "Dashboard do Paciente")

        self.cards()
        self.center_area()

    # =========================
    # CARDS
    # =========================
    def cards(self):

        frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(30,20))

        frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.card(frame, 0, "Próxima Consulta",
                  proxima_consulta(self.id_paciente), "#2563EB")

        self.card(frame, 1, "Consultas Marcadas",
                  str(total_consultas(self.id_paciente)), "#16A34A")

        self.card(frame, 2, "Notificações",
                  str(contar_notificacoes(self.id_paciente)), "#F59E0B")

        self.card(frame, 3, "Estado Triagem",
                  estado_triagem(self.id_paciente), "#DC2626")

    def card(self, parent, col, titulo, valor, cor):

        card = ctk.CTkFrame(parent, fg_color=cor, corner_radius=18, height=170)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        card.grid_propagate(False)

        interno = ctk.CTkFrame(card, fg_color="transparent")
        interno.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(interno, text=titulo,
                     text_color="white",
                     font=("Segoe UI",16)).pack(anchor="w")

        ctk.CTkLabel(interno, text=valor,
                     text_color="white",
                     font=("Segoe UI",26,"bold")).pack(anchor="w", pady=(15,0))

    # =========================
    # CENTER
    # =========================
    def center_area(self):

        centro = ctk.CTkFrame(self.parent, fg_color="transparent")
        centro.pack(fill="both", expand=True, padx=20, pady=15)

        centro.grid_columnconfigure(0, weight=3)
        centro.grid_columnconfigure(1, weight=1)

        centro.grid_rowconfigure(0, weight=1)
        centro.grid_rowconfigure(1, weight=1)

        self.consultas_ui(centro)
        self.notificacoes_ui(centro)
        self.acoes_ui(centro)   # ✔ agora correto

    # =========================
    # CONSULTAS
    # =========================
    def consultas_ui(self, parent):
        ...
        # (mantém o teu código igual)

    # =========================
    # NOTIFICAÇÕES
    # =========================
    def notificacoes_ui(self, parent):
        ...
        # (mantém o teu código igual)

    # =========================
    # AÇÕES RÁPIDAS (CORRIGIDO!)
    # =========================
    def acoes_ui(self, parent):

        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        box.grid(row=1, column=1, sticky="nsew", padx=(10,0))

        ctk.CTkLabel(box, text="Ações Rápidas",
                     font=("Segoe UI",20,"bold"),
                     text_color="#0B2A4A").pack(anchor="w", padx=20, pady=(20,15))

        botoes = [
            ("📅 Marcar Consulta", "#2563EB"),
            ("📋 Minhas Consultas", "#16A34A"),
            ("🔄 Reagendar", "#F59E0B"),
            ("❌ Cancelar Consulta", "#DC2626"),
            ("👤 Meu Perfil", "#6366F1")
        ]

        for texto, cor in botoes:
            ctk.CTkButton(
                box,
                text=texto,
                height=45,
                fg_color=cor,
                font=("Segoe UI",14,"bold"),
                corner_radius=8
            ).pack(fill="x", padx=20, pady=8)