import customtkinter as ctk
from interface._base import _topbar_base
from database.database import listar_notificacoes

class NotificacoesContent:

    def __init__(self, parent, id_paciente):
        self.parent = parent
        self.id_paciente = id_paciente

        _topbar_base(parent, "Notificações")
        self.build_ui()

    def build_ui(self):
        box = ctk.CTkFrame(self.parent, fg_color="#F4F6FB")
        box.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(box, text="Notificações",
                     font=("Segoe UI", 24, "bold"),
                     text_color="#0B2A4A").pack(anchor="w", pady=(0, 10))

        body = ctk.CTkScrollableFrame(box, fg_color="white", corner_radius=12)
        body.pack(fill="both", expand=True)

        notificacoes = listar_notificacoes(self.id_paciente)

        if not notificacoes:
            ctk.CTkLabel(body, text="Nenhuma notificação encontrada.",
                         font=("Segoe UI", 14), text_color="#667085").pack(pady=20)
            return

        for titulo, mensagem, data in notificacoes:
            card = ctk.CTkFrame(body, fg_color="#F4F6FB", corner_radius=12)
            card.pack(fill="x", pady=10, padx=15)

            ctk.CTkLabel(card, text=titulo,
                         font=("Segoe UI", 14, "bold"),
                         text_color="#0B2A4A").pack(anchor="w", padx=12, pady=(12, 0))

            ctk.CTkLabel(card, text=mensagem,
                         font=("Segoe UI", 13),
                         text_color="#475467",
                         wraplength=420,
                         justify="left").pack(anchor="w", padx=12, pady=(8, 0))

            ctk.CTkLabel(card, text=data,
                         font=("Segoe UI", 12),
                         text_color="#64748B").pack(anchor="e", padx=12, pady=(8, 12))
