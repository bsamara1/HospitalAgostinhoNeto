import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from database.database import conectar, listar_medicos


class Medicos(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("HAN - Hospital Agostinho Neto")
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
    # MAIN
    # =========================
    def main_ui(self):

        self.main = ctk.CTkFrame(self.container, fg_color="#F4F6FB")
        self.main.pack(side="left", fill="both", expand=True)

        self.header()
        self.table_area()

    # =========================
    # HEADER
    # =========================
    def header(self):

        header = ctk.CTkFrame(self.main, fg_color="#F4F6FB", height=90)
        header.pack(fill="x", padx=35, pady=(25, 15))
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left,
            text="Médicos",
            font=("Segoe UI", 30, "bold"),
            text_color="#183153"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Gerir todos os médicos registados.",
            font=("Segoe UI", 14),
            text_color="#6B7280"
        ).pack(anchor="w")

        # BOTÃO ADICIONAR MÉDICO
        ctk.CTkButton(
            header,
            text="+ Adicionar Médico",
            width=200,
            height=45,
            fg_color="#2563EB",
            hover_color="#1E4FD8",
            font=("Segoe UI", 15, "bold"),
            command=self.abrir_form_medico
        ).pack(side="right")

    # =========================
    # FORMULÁRIO
    # =========================
    def abrir_form_medico(self):

        self.janela = ctk.CTkToplevel(self)
        self.janela.title("Adicionar Médico")
        self.janela.geometry("400x550")
        self.janela.resizable(False, False)

        self.janela.grab_set()

        ctk.CTkLabel(
            self.janela,
            text="Novo Médico",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)

        self.nome = ctk.CTkEntry(self.janela, placeholder_text="Nome completo")
        self.nome.pack(pady=10, fill="x", padx=20)

        self.email = ctk.CTkEntry(self.janela, placeholder_text="Email")
        self.email.pack(pady=10, fill="x", padx=20)

        self.especialidade = ctk.CTkEntry(self.janela, placeholder_text="Especialidade")
        self.especialidade.pack(pady=10, fill="x", padx=20)

        self.telefone = ctk.CTkEntry(self.janela, placeholder_text="Telefone")
        self.telefone.pack(pady=10, fill="x", padx=20)

        # =========================
        # ESTADO DO MÉDICO
        # =========================
        self.estado = ctk.CTkComboBox(
            self.janela,
            values=["Disponível", "Ocupado", "Férias"],
            state="readonly"
        )
        self.estado.set("Disponível")
        self.estado.pack(pady=10, fill="x", padx=20)

        ctk.CTkButton(
            self.janela,
            text="Guardar",
            fg_color="#2563EB",
            hover_color="#1E4FD8",
            command=self.guardar_medico
        ).pack(pady=20)

    # =========================
    # GUARDAR MÉDICO
    # =========================
    def guardar_medico(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO medicos(nome, email, especialidade, telefone, estado)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.nome.get(),
            self.email.get(),
            self.especialidade.get(),
            self.telefone.get(),
            self.estado.get()
        ))

        conn.commit()
        conn.close()
        

        self.janela.destroy()

        messagebox.showinfo("Sucesso", "Médico adicionado com sucesso!")

        self.refresh_table()

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
    # TABELA
    # =========================
    def table_area(self):

        self.card = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E4E7EC"
        )
        self.card.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        self.content = ctk.CTkFrame(self.card, fg_color="white")
        self.content.pack(fill="both", expand=True)

        self.table_header()

        self.body = ctk.CTkScrollableFrame(self.content, fg_color="white")
        self.body.pack(fill="both", expand=True)

        self.table_rows()

        self.table_footer()

    # =========================
    # HEADER TABELA
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
            ("Nome", 180),
            ("Email", 90),
            ("Especialidade", 80),
            ("Telefone", 160),
            ("Estado", 170),
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
    # LINHAS
    # =========================
    def table_rows(self):

        medicos = listar_medicos()

        larguras = [60, 180, 90, 80, 160, 170, 100]

        for i, medicos in enumerate(medicos):

            linha = ctk.CTkFrame(
                self.body,
                fg_color="white",
                height=68
            )

            linha.pack(fill="x")
            linha.pack_propagate(False)

            # Colunas
            for valor, largura in zip(medicos, larguras):

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
            if i < len(medicos) - 1:

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

        total = len(listar_medicos())

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


if __name__ == "__main__":
    app = Medicos()
    app.mainloop()