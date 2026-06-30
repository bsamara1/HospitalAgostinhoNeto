import customtkinter as ctk
from tkinter import messagebox
from functools import partial

from database.database import (
    listar_fila_triagem,
    guardar_triagem,
    calcular_prioridade,
    listar_prioridades
)

from interface._base import _topbar_base


class TriagemContent:

    def __init__(self, parent):
<<<<<<< HEAD
        _placeholder(parent, "Triagem")
=======
        self.parent = parent

        _topbar_base(parent, "Triagem")

        self.header()
        self.search_area()
        self.table_area()

    # =========================
    # HEADER
    # =========================
    def header(self):

        header = ctk.CTkFrame(self.parent, fg_color="#F4F6FB", height=90)
        header.pack(fill="x", padx=35, pady=(25, 15))
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left,
            text="Triagem",
            font=("Segoe UI", 30, "bold"),
            text_color="#183153"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Gestão da triagem automática de pacientes.",
            font=("Segoe UI", 14),
            text_color="#6B7280"
        ).pack(anchor="w")

        ctk.CTkButton(
            header,
            text="+ Adicionar Triagem",
            width=180,
            height=45,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.abrir_selecionar_consulta
        ).pack(side="right")

    # =========================
    # SEARCH
    # =========================
    def search_area(self):

        filtros = ctk.CTkFrame(self.parent, fg_color="transparent")
        filtros.pack(fill="x", padx=35, pady=(0, 20))

        self.txtPesquisa = ctk.CTkEntry(
            filtros,
            placeholder_text="Pesquisar paciente...",
            height=45
        )
        self.txtPesquisa.pack(side="left", fill="x", expand=True)

        self.combo = ctk.CTkComboBox(
            filtros,
            values=["Todos", "Aguarda", "Em triagem", "Concluída"],
            width=180,
            height=45
        )
        self.combo.set("Todos")
        self.combo.pack(side="left", padx=15)

    # =========================
    # TABLE
    # =========================
    def table_area(self):

        self.card = ctk.CTkFrame(
            self.parent,
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
    # TABLE HEADER
    # =========================
    def table_header(self):

        header = ctk.CTkFrame(self.content, fg_color="#C9C9C9", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        colunas = [
            ("ID", 60),
            ("Paciente", 220),
            ("Idade", 80),
            ("Hora", 120),
            ("Prioridade", 120),
            ("Estado", 120),
        ]

        for texto, largura in colunas:
            ctk.CTkLabel(
                header,
                text=texto,
                width=largura,
                anchor="w",
                font=("Segoe UI", 13, "bold")
            ).pack(side="left", padx=5)

    # =========================
    # TABLE ROWS
    # =========================
    def table_rows(self):

        triagens = listar_fila_triagem()

        if not triagens:
            ctk.CTkLabel(
                self.body,
                text="Nenhum paciente na triagem.",
                font=("Segoe UI", 15),
                text_color="gray"
            ).pack(pady=40)
            return

        for t in triagens:

            linha = ctk.CTkFrame(self.body, fg_color="white", height=60)
            linha.pack(fill="x")
            linha.pack_propagate(False)

            dados = [t[0], t[1], t[2], t[3], t[4], t[5]]
            larguras = [60, 220, 80, 120, 120, 120]

            for valor, largura in zip(dados, larguras):
                ctk.CTkLabel(
                    linha,
                    text=str(valor),
                    width=largura,
                    anchor="w",
                    font=("Segoe UI", 13)
                ).pack(side="left", padx=5)

    # =========================
    # FOOTER
    # =========================
    def table_footer(self):

        footer = ctk.CTkFrame(self.content, fg_color="white", height=50)
        footer.pack(fill="x")
        footer.pack_propagate(False)

        total = len(listar_fila_triagem())

        ctk.CTkLabel(
            footer,
            text=f"Total: {total} pacientes",
            font=("Segoe UI", 12),
            text_color="#667085"
        ).pack(side="left", padx=20)

    # =========================
    # REFRESH
    # =========================
    def refresh_table(self):
        self.card.destroy()
        self.table_area()

    # =========================
    # SELECIONAR CONSULTA
    # =========================
    def abrir_selecionar_consulta(self):

        janela = ctk.CTkToplevel(self.parent)
        janela.title("Selecionar Consulta")
        janela.geometry("600x400")
        janela.grab_set()

        consultas = listar_prioridades()

        if not consultas:
            ctk.CTkLabel(
                janela,
                text="Nenhuma consulta disponível",
                font=("Segoe UI", 14),
                text_color="gray"
            ).pack(pady=40)
            return

        for c in consultas:

            consulta_id = c[0]
            paciente = c[1]
            prioridade = c[2]

            linha = ctk.CTkFrame(janela)
            linha.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(
                linha,
                text=f"ID {consulta_id} | {paciente} - {prioridade}"
            ).pack(side="left")

            ctk.CTkButton(
                linha,
                text="Selecionar",
                command=partial(self.abrir_form_triagem, consulta_id, janela)
            ).pack(side="right")

    # =========================
    # FORM TRIAGEM
    # =========================
    def abrir_form_triagem(self, consulta_id, janela_select=None):

        if janela_select:
            janela_select.destroy()

        self.consulta_id = consulta_id

        janela = ctk.CTkToplevel(self.parent)
        janela.title("Triagem")
        janela.geometry("600x700")
        janela.grab_set()

        self.janela_triagem = janela

        ctk.CTkLabel(
            janela,
            text="Triagem do Paciente",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=15)

        self.temp = ctk.CTkEntry(janela, placeholder_text="Temperatura")
        self.temp.pack(fill="x", padx=30, pady=5)

        self.pressao = ctk.CTkEntry(janela, placeholder_text="Pressão arterial")
        self.pressao.pack(fill="x", padx=30, pady=5)

        self.fc = ctk.CTkEntry(janela, placeholder_text="Frequência cardíaca")
        self.fc.pack(fill="x", padx=30, pady=5)

        self.sat = ctk.CTkEntry(janela, placeholder_text="Saturação (%)")
        self.sat.pack(fill="x", padx=30, pady=5)

        self.sintomas = ctk.CTkTextbox(janela, height=100)
        self.sintomas.pack(fill="x", padx=30, pady=10)

        ctk.CTkButton(
            janela,
            text="Calcular e Guardar",
            fg_color="#2563EB",
            command=self.salvar_triagem
        ).pack(pady=15)

    # =========================
    # SALVAR TRIAGEM
    # =========================
    def salvar_triagem(self):

        if not hasattr(self, "consulta_id"):
            messagebox.showerror("Erro", "Selecione uma consulta primeiro")
            return

        dados = {
            "temperatura": self.temp.get(),
            "spo2": self.sat.get(),
            "frequencia_cardiaca": self.fc.get(),
            "pressao": self.pressao.get(),
            "sintomas": self.sintomas.get("1.0", "end")
        }

        prioridade, score = calcular_prioridade(dados)

        guardar_triagem(
            self.consulta_id,
            prioridade,
            self.temp.get(),
            self.pressao.get(),
            self.fc.get(),
            self.sat.get(),
            "",
            "",
            dados["sintomas"]
        )

        self.janela_triagem.destroy()

        messagebox.showinfo(
            "Triagem concluída",
            f"Prioridade: {prioridade}\nScore: {score}"
        )

        self.refresh_table()
>>>>>>> ffe469d85f5e4ece0417cc81e3d0ba3aa256b428
