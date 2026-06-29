import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

class Definicao(ctk.CTk):

    # Modificado para receber opcionalmente os dados do utilizador logado
    def __init__(self, usuario=None):
        super().__init__()
        
        # Guardamos os dados numa variável interna da classe
        self.usuario = usuario if usuario else {
            "id": 0, "nome": "Administrar", "username": "teste", 
            "perfil": "Administrador", "email": "teste@han.cv", "telefone": "+238 000 00 00"
        }

        self.title("HAN - Definições de Perfil")
        self.after(10, lambda: self.state("zoomed"))
        self.configure(fg_color="#F4F6FB")

        self.ui()

    def ui(self):
        self.container = ctk.CTkFrame(self, fg_color="#F4F6FB")
        self.container.pack(fill="both", expand=True)

        self.sidebar_ui()
        self.main_ui()

    def sidebar_ui(self):
        self.sidebar = ctk.CTkFrame(self.container, width=240, fg_color="#0B2A4A")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        try:
            logo_img = Image.open("assets/logo.png")
            logo = ctk.CTkImage(logo_img, size=(40, 40))
            logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            logo_frame.pack(pady=(25, 35), padx=20, fill="x")
            ctk.CTkLabel(logo_frame, image=logo, text="").grid(row=0, column=0, rowspan=2, padx=10)
            ctk.CTkLabel(logo_frame, text="HAN", font=("Segoe UI", 20, "bold"), text_color="white").grid(row=0, column=1, sticky="w")
            ctk.CTkLabel(logo_frame, text="Hospital Agostinho Neto", font=("Segoe UI", 12), text_color="#D6E4F0").grid(row=1, column=1, sticky="w")
        except: pass

        def icon(path):
            try: return ctk.CTkImage(Image.open(path), size=(20, 20))
            except: return None

        menu = [
            ("Painel Principal", icon("assets/casa.png")),
            ("Pacientes", icon("assets/utilizadores.png")),
            ("Médicos", icon("assets/perfil.png")),
            ("Marcações", icon("assets/agendar.png")),
            ("Reagendamento", icon("assets/reagendar.png")),
            ("Cancelamento", icon("assets/cancelar.png")),
            ("Triagem", icon("assets/triagem.png")),
            ("Prioridades", icon("assets/prioridade.png")),
            ("Relatórios", icon("assets/relatorio.png")),
            ("Definições", icon("assets/definicao.png")),
        ]

        for text, ic in menu:
            bg_btn = "#2563EB" if text == "Definições" else "transparent"
            ctk.CTkButton(
                self.sidebar, text=text, image=ic, compound="left",
                fg_color=bg_btn, text_color="white", anchor="w",
                hover_color="#11457B", height=45,
                command=lambda n=text: self.abrir_menu(n)
            ).pack(fill="x", padx=15, pady=3)

        ctk.CTkButton(
            self.sidebar, text="Terminar Sessão", image=icon("assets/sair.png"),
            compound="left", fg_color="transparent", text_color="#FF6B6B",
            hover_color="#2A3F5F", anchor="w", height=45, command=self.terminar_sessao
        ).pack(side="bottom", fill="x", padx=15, pady=20)
        ctk.CTkFrame(self.sidebar,height=1,fg_color="#35506E").pack(side="bottom",fill="x",padx=15,pady=(0,10))

    def main_ui(self):
        self.main_scroll = ctk.CTkScrollableFrame(self.container, fg_color="#F4F6FB")
        self.main_scroll.pack(side="left", fill="both", expand=True, padx=40, pady=20)

        self.titulo_perfil = ctk.CTkLabel(
            self.main_scroll, text="Meu Perfil", 
            font=("Segoe UI", 28, "bold"), text_color="#0B2A4A"
        )
        self.titulo_perfil.pack(anchor="w", pady=(10, 0))

        self.sub_perfil = ctk.CTkLabel(
            self.main_scroll, text="Gerir informações da sua conta.", 
            font=("Segoe UI", 14), text_color="gray"
        )
        self.sub_perfil.pack(anchor="w", pady=(0, 30))

        self.cards_container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.cards_container.pack(fill="x", expand=True, pady=15)

        # --- CARD ESQUERDA: INFORMAÇÕES PESSOAIS ---
        self.card_info = ctk.CTkFrame(self.cards_container, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E4EC")
        self.card_info.pack(side="left", fill="both", expand=True, padx=(0, 20), ipady=20)

        ctk.CTkLabel(self.card_info, text="Informações Pessoais", font=("Segoe UI", 18, "bold"), text_color="#0B2A4A").pack(anchor="w", padx=25, pady=(20, 15))

        # PREENCHIMENTO DINÂMICO DOS DADOS:
        self.criar_input(self.card_info, "Nome Completo", self.usuario["nome"])
        self.criar_input(self.card_info, "Email", self.usuario["email"])
        self.criar_input(self.card_info, "Tipo de Utilizador", self.usuario["perfil"])
        self.criar_input(self.card_info, "Telefone", self.usuario["telefone"])

        ctk.CTkButton(
            self.card_info, text="Editar Informações", fg_color="#2563EB", 
            hover_color="#1E4FD8", height=45, font=("Segoe UI", 14, "bold")
        ).pack(fill="x", padx=25, pady=(20, 0))

        # --- CARD DIREITA: ALTERAR PASSWORD ---
        self.card_pass = ctk.CTkFrame(self.cards_container, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E4EC")
        self.card_pass.pack(side="left", fill="both", expand=True, ipady=20)

        ctk.CTkLabel(self.card_pass, text="Alterar Palavra-passe", font=("Segoe UI", 18, "bold"), text_color="#0B2A4A").pack(anchor="w", padx=25, pady=(20, 15))

        self.criar_input(self.card_pass, "Palavra-passe Atual", "", is_password=True)
        self.criar_input(self.card_pass, "Nova Palavra-passe", "", is_password=True)
        self.criar_input(self.card_pass, "Confirmar Nova Palavra-passe", "", is_password=True)

        ctk.CTkLabel(self.card_pass, text="", height=45).pack() 

        ctk.CTkButton(
            self.card_pass, text="Alterar Palavra-passe", fg_color="#2563EB", 
            hover_color="#1E4FD8", height=45, font=("Segoe UI", 14, "bold")
        ).pack(fill="x", padx=25, pady=(20, 0))

    def criar_input(self, parent, label_text, valor_inicial, is_password=False):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=25, pady=8)

        ctk.CTkLabel(frame, text=label_text, font=("Segoe UI", 13, "bold"), text_color="#475467").pack(anchor="w")
        
        entry = ctk.CTkEntry(
            frame, height=45, corner_radius=8, fg_color="#F9FAFB",
            border_color="#D0D5DD", text_color="black",
            show="*" if is_password else ""
        )
        entry.insert(0, valor_inicial)
        entry.pack(fill="x", pady=(5, 0))

    def abrir_menu(self, menu):
        self.destroy()
        # Ao navegar para outro menu, lembre-se de passar o dicionário self.usuario adiante se as outras telas também precisarem dele
        if menu == "Pacientes":
            from interface.pacientes import Pacientes
            Pacientes(usuario=self.usuario).mainloop()
        elif menu == "Dashboard" or menu == "Painel Principal":
            from interface.dashboard import Dashboard
            Dashboard(usuario=self.usuario).mainloop()
        elif menu == "Definições":
            from interface.definicao import Definicao
            # Passa o utilizador atual para a janela de Definições
            Definicao(usuario=self.usuario).mainloop()

    def terminar_sessao(self):
        if messagebox.askyesno("Sair", "Deseja realmente terminar a sessão?"):
            self.destroy()

if __name__ == "__main__":
    app = Definicao()
    app.mainloop()