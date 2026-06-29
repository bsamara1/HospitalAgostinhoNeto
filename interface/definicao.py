import customtkinter as ctk
from interface._base import _topbar_base


class DefinicaoContent:

    def __init__(self, parent):
        self.parent = parent
        _topbar_base(parent, "Definições")
        self.main_ui()

    def main_ui(self):
        scroll = ctk.CTkScrollableFrame(self.parent, fg_color="#F4F6FB")
        scroll.pack(fill="both", expand=True, padx=40, pady=20)

        ctk.CTkLabel(scroll, text="Meu Perfil", font=("Segoe UI", 28, "bold"), text_color="#0B2A4A").pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(scroll, text="Gerir informações da sua conta.", font=("Segoe UI", 14), text_color="gray").pack(anchor="w", pady=(0, 30))

        cards = ctk.CTkFrame(scroll, fg_color="transparent")
        cards.pack(fill="x", expand=True, pady=15)

        card_info = ctk.CTkFrame(cards, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E4EC")
        card_info.pack(side="left", fill="both", expand=True, padx=(0, 20), ipady=20)

        ctk.CTkLabel(card_info, text="Informações Pessoais", font=("Segoe UI", 18, "bold"), text_color="#0B2A4A").pack(anchor="w", padx=25, pady=(20, 15))
        self._input(card_info, "Nome Completo", "Administrador")
        self._input(card_info, "Email", "admin@han.cv")
        self._input(card_info, "Tipo de Utilizador", "Administrador")
        self._input(card_info, "Telefone", "+238 000 00 00")
        ctk.CTkButton(card_info, text="Editar Informações", fg_color="#2563EB", hover_color="#1E4FD8", height=45, font=("Segoe UI", 14, "bold")).pack(fill="x", padx=25, pady=(20, 0))

        card_pass = ctk.CTkFrame(cards, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E4EC")
        card_pass.pack(side="left", fill="both", expand=True, ipady=20)

        ctk.CTkLabel(card_pass, text="Alterar Palavra-passe", font=("Segoe UI", 18, "bold"), text_color="#0B2A4A").pack(anchor="w", padx=25, pady=(20, 15))
        self._input(card_pass, "Palavra-passe Atual", "", is_password=True)
        self._input(card_pass, "Nova Palavra-passe", "", is_password=True)
        self._input(card_pass, "Confirmar Nova Palavra-passe", "", is_password=True)
        ctk.CTkLabel(card_pass, text="", height=45).pack()
        ctk.CTkButton(card_pass, text="Alterar Palavra-passe", fg_color="#2563EB", hover_color="#1E4FD8", height=45, font=("Segoe UI", 14, "bold")).pack(fill="x", padx=25, pady=(20, 0))

    def _input(self, parent, label, valor, is_password=False):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=25, pady=8)
        ctk.CTkLabel(frame, text=label, font=("Segoe UI", 13, "bold"), text_color="#475467").pack(anchor="w")
        entry = ctk.CTkEntry(frame, height=45, corner_radius=8, fg_color="#F9FAFB", border_color="#D0D5DD", text_color="black", show="*" if is_password else "")
        entry.insert(0, valor)
        entry.pack(fill="x", pady=(5, 0))
