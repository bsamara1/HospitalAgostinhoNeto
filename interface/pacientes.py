import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from database.database import conectar,listar_pacientes

class Pacientes(ctk.CTk):

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

            # MENU
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
            ).pack(
                fill="x",
                padx=15,
                pady=3
            )


        # TERMINAR SESSÃO (fora do for)
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
                ).pack(
                side="bottom",
                fill="x",
                padx=15,
                pady=20
                )
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

        if menu == "Dashboard":
            from interface.dashboard import Dashboard
            Dashboard().mainloop()   
        
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
   # =========================
# MAIN
# =========================
    def main_ui(self):

        self.main = ctk.CTkFrame(
            self.container,
            fg_color="#F4F6FB"
        )
        self.main.pack(side="left", fill="both", expand=True)

        self.header()

        self.search_area()

        self.table_area()

    def abrir_form_paciente(self):

        self.janela = ctk.CTkToplevel(self)
        self.janela.title("Adicionar Paciente")
        self.janela.geometry("400x500")
        self.janela.resizable(False, False)

        self.janela.grab_set()

        ctk.CTkLabel(self.janela, text="Novo Paciente", font=("Segoe UI", 20, "bold")).pack(pady=20)

        self.nome = ctk.CTkEntry(self.janela, placeholder_text="Nome completo")
        self.nome.pack(pady=10, fill="x", padx=20)

        self.sexo = ctk.CTkComboBox(self.janela, values=["Masculino", "Feminino"])
        self.sexo.pack(pady=10, fill="x", padx=20)

        self.idade = ctk.CTkEntry(self.janela, placeholder_text="Idade")
        self.idade.pack(pady=10, fill="x", padx=20)

        self.telefone = ctk.CTkEntry(self.janela, placeholder_text="Telefone")
        self.telefone.pack(pady=10, fill="x", padx=20)

        self.bi = ctk.CTkEntry(self.janela, placeholder_text="BI")
        self.bi.pack(pady=10, fill="x", padx=20)

        self.nascimento = ctk.CTkEntry(self.janela, placeholder_text="Data nascimento (YYYY-MM-DD)")
        self.nascimento.pack(pady=10, fill="x", padx=20)

        self.morada = ctk.CTkEntry(self.janela,placeholder_text="Morada")
        self.morada.pack(pady=10, fill="x", padx=20)

        ctk.CTkButton(
            self.janela,
            text="Guardar",
            fg_color="#2563EB",
            command=self.guardar_paciente
        ).pack(pady=20)
   
    def guardar_paciente(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO pacientes(
                nome, sexo, idade,
                telefone, bi,
                nascimento, morada
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.nome.get(),
            self.sexo.get(),
            self.idade.get(),
            self.telefone.get(),
            self.bi.get(),
            self.nascimento.get(),
            self.morada.get()
        ))

        conn.commit()
        conn.close()

        self.janela.destroy()

        messagebox.showinfo(
            "Sucesso",
            "Paciente adicionado com sucesso!"
        )

        self.refresh_table()

# =========================
# CABEÇALHO
# =========================
    def header(self):

        header = ctk.CTkFrame(
            self.main,
            fg_color="#F4F6FB",
            height=90
        )
        header.pack(fill="x", padx=35, pady=(25,15))
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left,
            text="Pacientes",
            font=("Segoe UI",30,"bold"),
            text_color="#183153"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Gerir todos os pacientes registados.",
            font=("Segoe UI",14),
            text_color="#6B7280"
        ).pack(anchor="w", pady=(3,0))

        self.btn_novo = ctk.CTkButton(
            header,
            text="+ Adicionar Paciente",
            width=190,
            height=45,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1E4FD8",
            font=("Segoe UI",15,"bold"),
            command=self.abrir_form_paciente
        )

        self.btn_novo.pack(side="right")
# =========================
# PESQUISA
# =========================
    def search_area(self):

        filtros = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        filtros.pack(fill="x", padx=35, pady=(0,20))

        self.txt_pesquisa = ctk.CTkEntry(
            filtros,
            placeholder_text="🔍 Pesquisar por nome, BI ou telefone...",
            height=45,
            corner_radius=8,
            border_width=1,
            font=("Segoe UI",14)
        )
        self.txt_pesquisa.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.combo_estado = ctk.CTkComboBox(
            filtros,
            values=[
                "Todos",
                "Masculino",
                "Feminino"
            ],
            width=180,
            height=45,
            corner_radius=8
        )

        self.combo_estado.pack(
            side="left",
            padx=(15,0)
        )

        self.combo_estado.set("Todos")
 # =========================
# CARTÃO DA TABELA
# =========================

    def table_area(self):

        # CARD EXTERNO (contorno completo)
        self.card = ctk.CTkFrame(
        self.main,
        fg_color="white",
        corner_radius=12,
        border_width=1,
        border_color="#E4E7EC"
    )

        self.card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0,25)
        )

        self.content = ctk.CTkFrame(
            self.card,
            fg_color="white",
            corner_radius=12
        )

        self.content.pack(fill="both", expand=True)

        self.table_header()

        self.body = ctk.CTkScrollableFrame(
                self.content,
                fg_color="white",
                corner_radius=0
            )

        self.body.pack(
                fill="x",
                expand=False
            )

        self.table_rows()

        self.table_footer()


    # =========================
    # CABEÇALHO
    # =========================

    def table_header(self):

        header = ctk.CTkFrame(
            self.content,
            fg_color="#C9C9C9",
            height=65,
            corner_radius=0
        )

        header.pack(fill="x", pady=(0, 2))
        header.pack_propagate(False)

        colunas = [
            ("ID", 60),
            ("Nome", 200),
            ("Sexo", 90),
            ("Idade", 80),
            ("Telefone", 160),
            ("BI", 170),
            ("Morada", 170),
            ("Ações", 100)
        ]

        for texto, largura in colunas:

            ctk.CTkLabel(
                header,
                text=texto,
                width=largura,
                anchor="w",
                font=("Segoe UI", 13, "bold"),
                text_color="#475467"
            ).pack(
                side="left",
                padx=2
            )

        ctk.CTkFrame(
            self.content,
            height=1,
            fg_color="#E5E7EB"
        ).pack(fill="x")


   # =========================
# LINHAS DA TABELA
# =========================
    def table_rows(self):

        pacientes = listar_pacientes()

        larguras = [60, 200, 90, 80, 160, 170, 100]

        for i, paciente in enumerate(pacientes):

            linha = ctk.CTkFrame(
                self.body,
                fg_color="white",
                height=68
            )

            linha.pack(fill="x")
            linha.pack_propagate(False)

            # Colunas
            for valor, largura in zip(paciente, larguras):

                cel = ctk.CTkFrame(
                    linha,
                    width=largura,
                    fg_color="white"
                )

                cel.pack(
                    side="left",
                    fill="y"
                )

                cel.pack_propagate(False)

                ctk.CTkLabel(
                    cel,
                    text=str(valor),
                    anchor="w",
                    font=("Segoe UI", 13),
                    text_color="#344054"
                ).pack(
                    fill="both",
                    padx=12
                )

            # Área dos botões
            acoes = ctk.CTkFrame(
                linha,
                width=210,
                fg_color="white"
            )

            acoes.pack(
                side="left",
                fill="y"
            )

            acoes.pack_propagate(False)

            # Botão Editar
            ctk.CTkButton(
                acoes,
                text="Editar",
                width=75,
                height=34,
                corner_radius=8,
                fg_color="#2563EB",
                hover_color="#1D4ED8",
                text_color="white",
                font=("Segoe UI", 12, "bold")
            ).pack(
                side="left",
                padx=(10, 5),
                pady=10
            )

            # Botão Eliminar
            ctk.CTkButton(
                acoes,
                text="Eliminar",
                width=85,
                height=34,
                corner_radius=8,
                fg_color="#EF4444",
                hover_color="#DC2626",
                text_color="white",
                font=("Segoe UI", 12, "bold")
            ).pack(
                side="left",
                padx=5,
                pady=10
            )

            # Linha separadora
            if i < len(pacientes) - 1:

                ctk.CTkFrame(
                    self.body,
                    height=1,
                    fg_color="#F1F5F9"
                ).pack(
                    fill="x",
                    padx=15
                )

    # =========================
    # FOOTER
    # =========================
    # =========================
# FOOTER DA TABELA
# =========================
    def table_footer(self):

        # Linha superior
        ctk.CTkFrame(
            self.content,
            height=1,
            fg_color="#E5E7EB"
        ).pack(fill="x")

        footer = ctk.CTkFrame(
            self.content,
            fg_color="white",
            height=70,
            corner_radius=0
        )

        footer.pack(
            fill="x",
            side="bottom"
        )

        footer.pack_propagate(False)

        total = len(listar_pacientes())

        # Texto da esquerda
        ctk.CTkLabel(
            footer,
            text=f"Mostrando 1 a {min(10, total)} de {total} pacientes",
            font=("Segoe UI", 12),
            text_color="#667085"
        ).pack(
            side="left",
            padx=20
        )

        # Área da paginação
        paginas = ctk.CTkFrame(
            footer,
            fg_color="transparent"
        )

        paginas.pack(
            side="right",
            padx=20
        )

        # Botão <
        ctk.CTkButton(
            paginas,
            text="<",
            width=36,
            height=36,
            corner_radius=8,
            fg_color="white",
            border_width=1,
            border_color="#D0D5DD",
            text_color="#344054",
            hover_color="#F9FAFB"
        ).pack(side="left", padx=3)

        # Página 1
        ctk.CTkButton(
            paginas,
            text="1",
            width=36,
            height=36,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).pack(side="left", padx=3)

        # Página 2
        ctk.CTkButton(
            paginas,
            text="2",
            width=36,
            height=36,
            corner_radius=8,
            fg_color="white",
            border_width=1,
            border_color="#D0D5DD",
            text_color="#344054",
            hover_color="#F9FAFB"
        ).pack(side="left", padx=3)

        # Página 3
        ctk.CTkButton(
            paginas,
            text="3",
            width=36,
            height=36,
            corner_radius=8,
            fg_color="white",
            border_width=1,
            border_color="#D0D5DD",
            text_color="#344054",
            hover_color="#F9FAFB"
        ).pack(side="left", padx=3)

        # Reticências
        ctk.CTkLabel(
            paginas,
            text="...",
            font=("Segoe UI", 12),
            text_color="#667085"
        ).pack(side="left", padx=8)

        # Última página
        ctk.CTkButton(
            paginas,
            text="24",
            width=40,
            height=36,
            corner_radius=8,
            fg_color="white",
            border_width=1,
            border_color="#D0D5DD",
            text_color="#344054",
            hover_color="#F9FAFB"
        ).pack(side="left", padx=3)

        # Botão >
        ctk.CTkButton(
            paginas,
            text=">",
            width=36,
            height=36,
            corner_radius=8,
            fg_color="white",
            border_width=1,
            border_color="#D0D5DD",
            text_color="#344054",
            hover_color="#F9FAFB"
        ).pack(side="left", padx=3)


    # =========================
    # REFRESH
    # =========================
    def refresh_table(self):

        self.card.destroy()
        self.table_area()
    # =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app = Pacientes()
    app.mainloop()