import customtkinter as ctk
from interface._base import _topbar_base

class CancelarContent:

    def __init__(self, parent, id_paciente, sessao=None):
        self.parent = parent
        self.id_paciente = id_paciente
        self.sessao = sessao

        _topbar_base(parent, "Cancelar Consulta", sessao)
        self.build_ui()

    def build_ui(self):
        box = ctk.CTkFrame(self.parent, fg_color="#F4F6FB")
        box.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(box, text="Cancelar Consulta",
                     font=("Segoe UI", 24, "bold"),
                     text_color="#0B2A4A").pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(box, text="Esta tela está pronta para ser conectada à lógica de cancelamento de consultas.",
                     font=("Segoe UI", 14),
                     text_color="#667085",
                     wraplength=620,
                     justify="left").pack(anchor="w", pady=(0, 20), padx=5)

        ctk.CTkButton(box, text="Cancelar Consulta Atual",
                      fg_color="#DC2626", hover_color="#B91C1C",
                      font=("Segoe UI", 14, "bold"),
                      corner_radius=10,
                      command=lambda: None).pack(padx=5, pady=10)
