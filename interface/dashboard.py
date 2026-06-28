import customtkinter as ctk
from PIL import Image
from database import consultas_hoje, consultar_prioridade,consultar_agenda_medicos


class Dashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

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
                height=45
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
            height=45
        ).pack(side="bottom", fill="x", padx=15, pady=20)
        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color="#35506E"
        ).pack(side="bottom", fill="x", padx=15, pady=(0, 10))


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

    # =========================
    # CARDS
    # =========================
    def cards(self):

        frame = ctk.CTkFrame(self.main, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(30,20))

        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        def card(col, title, value, color):
            c = ctk.CTkFrame(
                frame,
                fg_color=color,
                corner_radius=18,
                width=260,
                height=180
            )

            c.grid(
                row=0,
                column=col,
                padx=12,
                sticky="nsew"
            )

            c.grid_propagate(False)
            inner = ctk.CTkFrame(c, fg_color="transparent")
            inner.pack(expand=True, fill="both", padx=20, pady=20)

            ctk.CTkLabel(inner, text=title, text_color="white", font=("Segoe UI", 15)).pack(anchor="w", padx=20, pady=(20,5))
            ctk.CTkLabel(
                inner,
                text=value,
                text_color="white",
                font=("Segoe UI", 22, "bold")
            ).pack(anchor="w", padx=20)

        card(0, "Consultas Hoje", "48", "#2E86C1")
        card(1, "Médicos", "12", "#28B463")
        card(2, "Urgências", "18", "#E74C3C")
        card(3, "Tempo Médio", "32 min", "#F39C12")

  
   # CENTRO (TABELA + PRIORIDADES)
    
    def center_area(self):

        center = ctk.CTkFrame(self.main, fg_color="transparent")
        center.pack(fill="both", expand=True, padx=20, pady=15)

        center.grid_columnconfigure(0, weight=2)
        center.grid_columnconfigure(1, weight=1)
        center.grid_columnconfigure(2, weight=1)

        center.grid_rowconfigure(0, weight=1)

        self.table_ui(center)
        self.prioridade_ui(center)
        self.agenda_ui(center)

    # =========================
    # TABELA CONSULTAS
    # =========================
    def table_ui(self, parent):

        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        box.grid(row=0, column=0, sticky="nsew", padx=(0,10))

        ctk.CTkLabel(
            box,
            text="Consultas de Hoje",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=20, pady=10)

        header = ctk.CTkFrame(box, fg_color="transparent")
        header.pack(fill="x", padx=20)

        cols = ["Paciente", "Médico", "Hora", "Prioridade", "Estado"]

        for c in cols:
            ctk.CTkLabel(header, text=c, width=120, anchor="w").pack(side="left")

        dados = consultas_hoje()

        for p, m, h, pr, st in dados:

            row = ctk.CTkFrame(box, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=3)

            for val, w in [(p,120),(m,120),(h,80),(pr,100),(st,100)]:
                ctk.CTkLabel(row, text=val, width=w, anchor="w").pack(side="left")

    # =========================
    # PRIORIDADES
    # =========================
    def prioridade_ui(self, parent):

        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        box.grid(row=0, column=1, sticky="nsew", padx=10)

        ctk.CTkLabel(
            box,
            text="Consultas por Prioridade",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=20, pady=10)

        dados = consultar_prioridade()

        for prioridade, total in dados:

            row = ctk.CTkFrame(box, fg_color="#F4F6FB")
            row.pack(fill="x", padx=15, pady=5)

            ctk.CTkLabel(
                row,
                text=prioridade,
                width=120,
                anchor="w",
                font=("Segoe UI", 13, "bold")
            ).pack(side="left", padx=10)

            ctk.CTkLabel(
                row,
                text=f"{total} consultas",
                anchor="w"
            ).pack(side="left")
            
        ctk.CTkLabel(box, text="").pack(pady=5)
        
    def agenda_ui(self, parent):

        box = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=10
        )

        box.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(10,0)
        )

        ctk.CTkLabel(
            box,
            text="Agenda dos Médicos",
            font=("Segoe UI",18,"bold")
        ).pack(anchor="w", padx=20, pady=10)

        agenda = consultar_agenda_medicos()

        for nome, especialidade, horario in agenda:

            card = ctk.CTkFrame(
                box,
                fg_color="#F4F6FB",
                corner_radius=8
            )
            card.pack(fill="x", padx=15, pady=6)

            ctk.CTkLabel(
                card,
                text=nome,
                font=("Segoe UI",13,"bold"),
                anchor="w"
            ).pack(anchor="w", padx=10, pady=(8,0))

            ctk.CTkLabel(
                card,
                text=especialidade,
                text_color="gray"
            ).pack(anchor="w", padx=10)

            ctk.CTkLabel(
                card,
                text=horario,
                text_color="#2E86C1"
            ).pack(anchor="w", padx=10, pady=(0,8))






# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()