import customtkinter as ctk
from interface._base import _topbar_base

from database.database import (
    proxima_consulta,
    total_consultas,
    contar_notificacoes,
    estado_triagem,
    listar_consultas_paciente,
    listar_notificacoes,
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
        frame.pack(fill="x", padx=20, pady=(30, 20))
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

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
                     font=("Segoe UI", 16)).pack(anchor="w")

        ctk.CTkLabel(interno, text=valor,
                     text_color="white",
                     font=("Segoe UI", 26, "bold")).pack(anchor="w", pady=(15, 0))

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
        self.acoes_ui(centro)

    # =========================
    # CONSULTAS
    # =========================
    def consultas_ui(self, parent):
        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        box.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10), pady=(0, 0))

        ctk.CTkLabel(box, text="Minhas Consultas",
                     font=("Segoe UI", 20, "bold"),
                     text_color="#0B2A4A").pack(anchor="w", padx=20, pady=(20, 10))

        body = ctk.CTkScrollableFrame(box, fg_color="transparent", corner_radius=0)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        consultas = listar_consultas_paciente(self.id_paciente)

        if not consultas:
            ctk.CTkLabel(body, text="Nenhuma consulta agendada.",
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
            row = ctk.CTkFrame(body, fg_color="#FFFFFF", corner_radius=10)
            row.pack(fill="x", pady=4)
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

    # =========================
    # NOTIFICAÇÕES
    # =========================
    def notificacoes_ui(self, parent):
        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        box.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 10))

        ctk.CTkLabel(box, text="Notificações",
                     font=("Segoe UI", 20, "bold"),
                     text_color="#0B2A4A").pack(anchor="w", padx=20, pady=(20, 10))

        body = ctk.CTkScrollableFrame(box, fg_color="transparent", corner_radius=0)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        notificacoes = listar_notificacoes(self.id_paciente)

        if not notificacoes:
            ctk.CTkLabel(body, text="Sem notificações novas.",
                         font=("Segoe UI", 14), text_color="#667085").pack(pady=20)
            return

        for titulo, mensagem, data in notificacoes:
            card = ctk.CTkFrame(body, fg_color="#F4F6FB", corner_radius=12)
            card.pack(fill="x", pady=8)

            ctk.CTkLabel(card, text=titulo,
                         font=("Segoe UI", 14, "bold"),
                         text_color="#0B2A4A").pack(anchor="w", padx=12, pady=(12, 0))

            ctk.CTkLabel(card, text=mensagem,
                         font=("Segoe UI", 13),
                         text_color="#475467",
                         wraplength=260,
                         justify="left").pack(anchor="w", padx=12, pady=(8, 0))

            ctk.CTkLabel(card, text=data,
                         font=("Segoe UI", 12),
                         text_color="#64748B").pack(anchor="e", padx=12, pady=(8, 12))

    # =========================
    # AÇÕES RÁPIDAS
    # =========================
    def acoes_ui(self, parent):
        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        box.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(0, 0))

        ctk.CTkLabel(box, text="Ações Rápidas",
                     font=("Segoe UI", 20, "bold"),
                     text_color="#0B2A4A").pack(anchor="w", padx=20, pady=(20, 15))

        botoes = [
            ("📅 Marcar Consulta", "#2563EB"),
            ("📋 Minhas Consultas", "#16A34A"),
            ("🔄 Reagendar", "#F59E0B"),
            ("❌ Cancelar Consulta", "#DC2626"),
            ("👤 Meu Perfil", "#6366F1"),
        ]

        for texto, cor in botoes:
            ctk.CTkButton(
                box,
                text=texto,
                height=45,
                fg_color=cor,
                font=("Segoe UI", 14, "bold"),
                corner_radius=8,
                command=lambda t=texto: None
            ).pack(fill="x", padx=20, pady=8)
