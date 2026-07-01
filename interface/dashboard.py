import customtkinter as ctk
from interface.dashboard_base import DashboardBase
from database.database import consultas_hoje, consultar_prioridade, consultar_agenda_medicos


class DashboardAdmin(DashboardBase):

<<<<<<< HEAD
        self.title("HAN - Hospital Agostinho Neto")
        self.state("zoomed")
        self.configure(fg_color="#F4F6FB")

        self.ui()

    # =========================
    # UI PRINCIPAL
    # =========================
    def ui(self):

        self.container = ctk.CTkFrame(self, fg_color="#F4F6FB")
        self.container.pack(fill="both", expand=True)

        self.sidebar_ui()
        self.main_ui()

    # =========================
    # SIDEBAR
    # =========================
    def sidebar_ui(self):

        self.sidebar = ctk.CTkFrame(
            self.container,
            width=240,
            fg_color="#0B2A4A"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = ctk.CTkImage(Image.open("assets/logo.png"), size=(40, 40))

        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(25, 35), padx=20, fill="x")

        ctk.CTkLabel(logo_frame, image=logo, text="").grid(row=0, column=0, rowspan=2, padx=10)

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

        # ICONS
        def icon(path):
            return ctk.CTkImage(Image.open(path), size=(20, 20))

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
            ctk.CTkButton(
                self.sidebar,
                text=text,
                image=ic,
                compound="left",
                fg_color="transparent",
                text_color="white",
                anchor="w",
                hover_color="#11457B",
                height=45,
                command=lambda nome=text: self.abrir_menu(nome)
            ).pack(fill="x", padx=15, pady=3)

        ctk.CTkButton(
            self.sidebar,
            text="Terminar Sessão",
            image=icon("assets/sair.png"),
            compound="left",
            fg_color="transparent",
            text_color="#FF6B6B",
            hover_color="#2A3F5F",
            anchor="w",
            height=45,
            command=self.terminar_sessao
        ).pack(side="bottom", fill="x", padx=15, pady=20)
        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color="#35506E"
        ).pack(side="bottom", fill="x", padx=15, pady=(0, 10))
    def terminar_sessao(self):

        confirmar = messagebox.askyesno(
            "Terminar Sessão",
            "Deseja realmente terminar a sessão?"
        )

        if confirmar:
            self.destroy()

            import customtkinter as ctk
            from interface.login import Login

            root = ctk.CTk()

            Login(root)

            root.mainloop()
    
    def abrir_menu(self, menu):

        self.destroy()

        if menu == "Médicos":
            from interface.medicos import Medicos

            Medicos().mainloop()

            app.mainloop()
        if menu == "Pacientes":
            from interface.pacientes import Pacientes
            Pacientes().mainloop()   
        
        elif menu == "Marcações":
            from interface.Agendamento import Marcacao
            Marcacao().mainloop() 
        elif menu == "Reagendamento":
            from interface.reagendamento import Reagendamento
            Reagendamento().mainloop() 
        elif menu == "Cancelamento":
            from interface.cancelamento import Cancelamento
            Cancelamento().mainloop() 
        elif menu == "Triagem":
            from interface.triagem import Triagem
            Triagem().mainloop() 
        elif menu == "Prioridades":
            from interface.prioridades import Prioridades
            Prioridades().mainloop() 
        elif menu == "Relatórios":
            from interface.relatorios import Relatorios
            Relatorios().mainloop() 
        elif menu == "Definições":
            from interface.definicao import Definicao
            Definicao().mainloop() 
                
    
    
    
    # =========================
    # MAIN AREA
    # =========================
    def main_ui(self):

        self.main = ctk.CTkFrame(self.container, fg_color="#F4F6FB")
        self.main.pack(side="left", fill="both", expand=True)

        self.topbar()
        self.cards()
        self.center_area()

    # =========================
    # TOPBAR
    # =========================
    def topbar(self):

        topbar = ctk.CTkFrame(self.main, fg_color="#F4F6FB", height=60)
        topbar.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            topbar,
            text="Painel Principal",
            font=("Segoe UI", 22, "bold"),
            text_color="#0B2A4A"
        ).pack(side="left",padx=20)
        linha = ctk.CTkFrame(
            self.main,
            height=1,
            fg_color="#D8DEE9",
            corner_radius=0
        )

        linha.pack(
            fill="x",
            pady=(5, 0)
        )

        avatar = ctk.CTkImage(
        Image.open("assets/perfil.png"),
        size=(42,42)
        )

        user = ctk.CTkFrame(topbar, fg_color="transparent")
        user.pack(side="right")

        ctk.CTkLabel(
            user,
            image=avatar,
            text=""
        ).pack(side="left", padx=10)

        texto = ctk.CTkFrame(user, fg_color="transparent")
        texto.pack(side="left")

        ctk.CTkLabel(
            texto,
            text="Administrador",
            font=("Segoe UI",15,"bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            texto,
            text="Administrador",
            text_color="gray"
        ).pack(anchor="w")
=======
    def __init__(self, parent):
        super().__init__(parent, "Painel Administrativo")
>>>>>>> e6c7e2e51d53b791fbb4f265798f0f6350352252

    # =========================
    # CARDS
    # =========================
    def get_cards_data(self):
        return [
            ("Consultas Hoje", "48", "#2E86C1"),
            ("Médicos", "12", "#28B463"),
            ("Urgências", "18", "#E74C3C"),
            ("Tempo Médio", "32 min", "#F39C12")
        ]

    # =========================
    # TABLE
    # =========================
    def table_title(self):
        return "Consultas de Hoje"

    def table_columns(self):
        return ["Paciente", "Médico", "Hora", "Prioridade", "Estado"]

    def table_widths(self):
        return [120, 120, 80, 100, 100]

    def get_table_data(self):
        return consultas_hoje()

    # =========================
    # MIDDLE
    # =========================
    def middle_title(self):
        return "Consultas por Prioridade"

    def get_middle_data(self):
        return consultar_prioridade()

    def render_middle_item(self, box, item):
        prioridade, total = item

        row = ctk.CTkFrame(box, fg_color="#F4F6FB")
        row.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(row, text=prioridade,
                     width=120, font=("Segoe UI", 13, "bold")).pack(side="left", padx=10)

        ctk.CTkLabel(row, text=f"{total} consultas").pack(side="left")

    # =========================
    # RIGHT
    # =========================
    def right_title(self):
        return "Agenda dos Médicos"

    def get_right_data(self):
        return consultar_agenda_medicos()

    def render_right_item(self, box, item):
        nome, especialidade, horario = item

        card = ctk.CTkFrame(box, fg_color="#F4F6FB", corner_radius=8)
        card.pack(fill="x", padx=15, pady=6)

        ctk.CTkLabel(card, text=nome,
                     font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=10)

        ctk.CTkLabel(card, text=especialidade,
                     text_color="gray").pack(anchor="w", padx=10)

        ctk.CTkLabel(card, text=horario,
                     text_color="#2E86C1").pack(anchor="w", padx=10, pady=(0, 8))