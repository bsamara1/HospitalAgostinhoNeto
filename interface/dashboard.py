import customtkinter as ctk
from PIL import Image


class Dashboard(ctk.CTk):

    def __init__(self):
        super().__init__()
        
        self.title("HAN")
        self.state("zoomed")
        self.configure(fg_color="#F4F6FB")

        self.ui()

    def ui(self):
        self.container = ctk.CTkFrame(self, fg_color="#F4F6FB")
        self.container.pack(fill="both", expand=True)
        
        # SIDEBAR

        self.sidebar = ctk.CTkFrame(
            self.container,
            width=240,
            fg_color="#0B2A4A"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="HAN",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        ).pack(pady=30)
        # ==================================================
        # ÍCONES
        # ==================================================
        self.home = ctk.CTkImage(Image.open("assets/casa.png"), size=(20, 20))
        self.icon_students = ctk.CTkImage(Image.open("assets/perfil.png"), size=(20, 20))
        self.icon_scholarship = ctk.CTkImage(Image.open("assets/bolsa.png"), size=(20, 20))
        self.icon_applications = ctk.CTkImage(Image.open("assets/candidatura.png"), size=(20, 20))
        self.icon_prolog = ctk.CTkImage(Image.open("assets/avaliacao.png"), size=(20, 20))
        self.icon_reports = ctk.CTkImage(Image.open("assets/relatorio.png"), size=(20, 20))
        self.icon_users = ctk.CTkImage(Image.open("assets/utilizadores.png"), size=(20, 20))
        self.icon_settings = ctk.CTkImage(Image.open("assets/definicao.png"), size=(20, 20))
        self.terminar = ctk.CTkImage(Image.open("assets/sair.png"), size=(20, 20))

        menu = [
            ("Painel Principal", self.home),
            ("Pacientes", self.icon_students),
            ("Marcacao de Consulta", self.icon_scholarship),
            ("Medicos", self.icon_applications),
            ("Reagendamento",self.home),
            ("Cancelamento",self.home),
            ("Prioridades", self.icon_prolog),
            ("Relatórios", self.icon_reports),
            ("Definições", self.icon_settings)
        ]
        for texto, icone in menu:
            ctk.CTkButton(
                self.sidebar,
                text=texto,
                image=icone,
                compound="left",
                fg_color="transparent",
                text_color="white",
                anchor="w",
                hover_color="#11457B",
                height=45
            ).pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="Terminar Sessão",
            image=self.terminar,
            compound="left",
            anchor="w",
            fg_color="transparent",
            text_color="#FF6B6B",
            hover_color="#2A3F5F",
            height=45
        ).pack(side="bottom", fill="x", padx=15, pady=20)

        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color="#35506E"
        ).pack(side="bottom", fill="x", padx=15, pady=(0, 10))

        # ÁREA PRINCIPAL
        # ==================================================
        self.main = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )
        self.main.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ==================================================
        # TOPBAR
        # ==================================================
        topbar = ctk.CTkFrame(
            self.main,
            fg_color="#F4F6FB",
            height=80
        )
        topbar.pack(fill="x")

        title_frame = ctk.CTkFrame(topbar, fg_color="transparent")
        title_frame.pack(side="left", padx=20)

        ctk.CTkLabel(
            title_frame,
            text="Painel Principal",
            font=("Segoe UI", 22, "bold"),
            text_color="#0B2A4A"
        ).pack(anchor="w")
        # =========================
        # CARDS DE ESTATÍSTICAS
        # =========================
        cards_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        cards_frame.pack(fill="x", pady=15)

        def card(title, value, color):
            frame = ctk.CTkFrame(cards_frame, fg_color=color, width=200, height=100)
            frame.pack(side="left", padx=10)
            frame.pack_propagate(False)

            ctk.CTkLabel(frame, text=title, text_color="white", font=("Segoe UI", 13)).pack(pady=(15, 0))
            ctk.CTkLabel(frame, text=value, text_color="white", font=("Segoe UI", 22, "bold")).pack()

        card("Consultas Hoje", "48", "#2E86C1")
        card("Médicos Disponíveis", "12", "#28B463")
        card("Urgências", "18", "#E74C3C")
        card("Tempo Médio", "32 min", "#F39C12")

        user_frame = ctk.CTkFrame(topbar, fg_color="transparent")
        user_frame.pack(side="right", padx=20)

        ctk.CTkLabel(
            user_frame,
            text="Administrador",
            text_color="#0B2A4A"
        ).pack()

       
if __name__ == "__main__":

        dashboard = Dashboard()

        dashboard.mainloop()