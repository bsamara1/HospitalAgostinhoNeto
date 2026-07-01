import customtkinter as ctk
from PIL import Image
from tkinter import messagebox


MENUS = [
    ("Painel Principal", "assets/casa.png"),
    ("Pacientes", "assets/utilizadores.png"),
    ("Médicos", "assets/perfil.png"),
    ("Agendamento", "assets/agendar.png"),
    ("Reagendamento", "assets/reagendar.png"),
    ("Cancelamento", "assets/cancelar.png"),
    ("Triagem", "assets/triagem.png"),
    ("Prioridades", "assets/prioridade.png"),
    ("Definições", "assets/definicao.png"),
]


class MainContent:

    def __init__(self, parent, on_logout):
        self.parent = parent
        self.on_logout = on_logout

        self._menu_buttons = {}
        self._icons = []

        self._build_layout()
        self.load_screen("Painel Principal")

    # =========================
    # LAYOUT PRINCIPAL
    # =========================
    def _build_layout(self):

        self.container = ctk.CTkFrame(self.parent, fg_color="#F4F6FB")
        self.container.pack(fill="both", expand=True)

        self._build_sidebar()

        self.content_frame = ctk.CTkFrame(
            self.container,
            fg_color="#F4F6FB"
        )
        self.content_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

    # =========================
    # SIDEBAR
    # =========================
    def _build_sidebar(self):

        sidebar = ctk.CTkFrame(
            self.container,
            width=240,
            fg_color="#0B2A4A",
            corner_radius=0
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # LOGO
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(pady=(25, 35), padx=20, fill="x")

        try:
            logo = ctk.CTkImage(Image.open("assets/logo.png"), size=(40, 40))
            ctk.CTkLabel(logo_frame, image=logo, text="").grid(row=0, column=0, rowspan=2, padx=10)
            self._logo_ref = logo
        except:
            pass

        ctk.CTkLabel(
            logo_frame,
            text="HAN",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        ).grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            logo_frame,
            text="Hospital Agostinho Neto",
            font=("Segoe UI", 13),
            text_color="#D6E4F0"
        ).grid(row=1, column=1, sticky="w")

        # MENUS
        for nome, icon_path in MENUS:

            try:
                img = ctk.CTkImage(Image.open(icon_path), size=(20, 20))
                self._icons.append(img)
            except:
                img = None
                self._icons.append(None)

            btn = ctk.CTkButton(
                sidebar,
                text=nome,
                image=img,
                compound="left",
                fg_color="transparent",
                text_color="white",
                anchor="w",
                hover_color="#11457B",
                height=45,
                command=lambda n=nome: self.load_screen(n)
            )
            btn.pack(fill="x", padx=15, pady=3)

            self._menu_buttons[nome] = btn

        # BOTÃO SAIR
        ctk.CTkButton(
            sidebar,
            text="Terminar Sessão",
            fg_color="transparent",
            text_color="#FF6B6B",
            hover_color="#2A3F5F",
            anchor="w",
            height=45,
            command=self.terminar_sessao
        ).pack(side="bottom", fill="x", padx=15, pady=20)

    # =========================
    # MENU ATIVO
    # =========================
    def _set_active(self, nome):
        for n, btn in self._menu_buttons.items():
            btn.configure(fg_color="#2563EB" if n == nome else "transparent")

    # =========================
    # TROCA DE TELA (CORRIGIDO)
    # =========================
    def load_screen(self, menu_name):

        self._set_active(menu_name)

        # limpar conteúdo antigo
        for w in self.content_frame.winfo_children():
            w.destroy()

        # IMPORTS LAZY (evita crashes)
        if menu_name == "Painel Principal":
            from interface.dashboard import DashboardAdmin
            DashboardAdmin(self.content_frame)

        elif menu_name == "Pacientes":
            from interface.pacientes import PacientesContent
            PacientesContent(self.content_frame)

        elif menu_name == "Médicos":
            from interface.medicos import MedicosContent
            MedicosContent(self.content_frame)

        elif menu_name == "Agendamento":
            from interface.Agendamento import AgendamentoContent
            AgendamentoContent(self.content_frame)

        elif menu_name == "Reagendamento":
            from interface.reagendamento import ReagendamentoContent
            ReagendamentoContent(self.content_frame)

        elif menu_name == "Cancelamento":
            from interface.cancelamento import CancelamentoContent
            CancelamentoContent(self.content_frame)

        elif menu_name == "Triagem":
            from interface.triagem import TriagemContent
            TriagemContent(self.content_frame)

        elif menu_name == "Prioridades":
            from interface.prioridades import PrioridadesContent
            PrioridadesContent(self.content_frame)

        elif menu_name == "Definições":
            from interface.definicao import DefinicaoContent
            DefinicaoContent(self.content_frame)

    # =========================
    # LOGOUT
    # =========================
    def terminar_sessao(self):
        if messagebox.askyesno("Terminar Sessão", "Deseja realmente terminar a sessão?"):
            self.on_logout()