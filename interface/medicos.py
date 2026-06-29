import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from database import conectar, consultar_agenda_medicos  # Importa as funções corrigidas do seu database

class Medicos(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HAN - Hospital Agostinho Neto")
        
        # Em vez de chamar direto, agendamos para rodar logo após a janela abrir:
        self.after(10, lambda: self.state("zoomed"))

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
        self.sidebar = ctk.CTkFrame(self.container, width=240, fg_color="#0B2A4A")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = ctk.CTkImage(Image.open("assets/logo.png"), size=(40, 40))
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(25, 35), padx=20, fill="x")

        ctk.CTkLabel(logo_frame, image=logo, text="").grid(row=0, column=0, rowspan=2, padx=10)
        ctk.CTkLabel(logo_frame, text="HAN", font=("Segoe UI", 20, "bold"), text_color="white").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(logo_frame, text="Hospital Agostinho Neto", font=("Segoe UI", 13), text_color="#D6E4F0").grid(row=1, column=1, sticky="w")

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
                self.sidebar, text=text, image=ic, compound="left",
                fg_color="transparent", text_color="white", anchor="w",
                hover_color="#11457B", height=45,
                command=lambda nome=text: self.abrir_menu(nome)
            ).pack(fill="x", padx=15, pady=3)

        ctk.CTkButton(
            self.sidebar, text="Terminar Sessão", image=icon("assets/sair.png"),
            compound="left", fg_color="transparent", text_color="#FF6B6B",
            hover_color="#2A3F5F", anchor="w", height=45, command=self.terminar_sessao
        ).pack(side="bottom", fill="x", padx=15, pady=20)

    def terminar_sessao(self):
        confirmar = messagebox.askyesno("Terminar Sessão", "Deseja realmente terminar a sessão?")
        if confirmar:
            self.destroy()
            from interface.login import Login
            root = ctk.CTk()
            Login(root)
            root.mainloop()        

    def abrir_menu(self, menu):
        if menu == "Médicos" and self.__class__.__name__ in ["Medicos", "medicos"]:
            return

        self.destroy()
        if menu in ["Dashboard", "Painel Principal"]:
            from interface.dashboard import Dashboard
            Dashboard().mainloop()
        elif menu == "Pacientes":
            from interface.pacientes import Pacientes
            Pacientes().mainloop()   
        elif menu == "Médicos":
            from interface.medicos import Medicos
            Medicos().mainloop()
        elif menu == "Marcações":
            from interface.marcacao import Marcacao
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
        self.lista_medicos_ui()

    # =========================
    # TOPBAR
    # =========================
    def topbar(self):
        topbar = ctk.CTkFrame(self.main, fg_color="#F4F6FB", height=60)
        topbar.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(topbar, text="Equipa Médica", font=("Segoe UI", 22, "bold"), text_color="#0B2A4A").pack(side="left", padx=20)
        
        linha = ctk.CTkFrame(self.main, height=1, fg_color="#D8DEE9", corner_radius=0)
        linha.pack(fill="x", pady=(5, 0))

        avatar = ctk.CTkImage(Image.open("assets/perfil.png"), size=(42, 42))
        user = ctk.CTkFrame(topbar, fg_color="transparent")
        user.pack(side="right")

        ctk.CTkLabel(user, image=avatar, text="").pack(side="left", padx=10)
        texto = ctk.CTkFrame(user, fg_color="transparent")
        texto.pack(side="left")

        ctk.CTkLabel(texto, text="Administrador", font=("Segoe UI", 15, "bold")).pack(anchor="w")
        ctk.CTkLabel(texto, text="Administrador", text_color="gray").pack(anchor="w")

    # =========================
    # LISTA DE MÉDICOS (Scrollable)
    # =========================
    def lista_medicos_ui(self):
        scroll_frame = ctk.CTkScrollableFrame(
            self.main, fg_color="transparent",
            label_text="Médicos Registados no Sistema",
            label_font=("Segoe UI", 16, "bold"), label_text_color="#0B2A4A"
        )
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Carrega os dados utilizando a função do seu arquivo database.py
        try:
            lista_medicos = consultar_agenda_medicos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler os médicos da base de dados: {e}")
            lista_medicos = []

        doc_icon = ctk.CTkImage(Image.open("assets/perfil.png"), size=(35, 35))

        for index, med in enumerate(lista_medicos):
            # No seu database, a query devolve: nome, especialidade, horario
            med_nome, med_especialidade, med_horario = med

            card = ctk.CTkFrame(scroll_frame, fg_color="white", height=65, corner_radius=10)
            card.pack(fill="x", pady=6, padx=5)
            card.pack_propagate(False)

            # Ícone do Médico
            ctk.CTkLabel(card, image=doc_icon, text="").pack(side="left", padx=15)

            # Informações
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="y", pady=10)

            ctk.CTkLabel(info_frame, text=med_nome, font=("Segoe UI", 14, "bold"), text_color="#0B2A4A").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Especialidade: {med_especialidade}  |  Horário: {med_horario}", font=("Segoe UI", 11), text_color="gray").pack(anchor="w")

            # Botão de Ação Lateral
            ctk.CTkButton(
                card, text="Disponibilidade", width=120, height=32,
                fg_color="#11457B", hover_color="#0B2A4A", font=("Segoe UI", 12)
            ).pack(side="right", padx=15, pady=15)

if __name__ == "__main__":
    app = Medicos()
    app.mainloop()