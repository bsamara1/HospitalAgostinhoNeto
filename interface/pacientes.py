import customtkinter as ctk
from tkinter import messagebox
from database.database import conectar, listar_pacientes
from interface._base import _topbar_base


class PacientesContent:

    def __init__(self, parent):
        self.parent = parent
        _topbar_base(parent, "Pacientes")
        self.header()
        self.search_area()
        self.table_area()

    def abrir_form_paciente(self):
        janela = ctk.CTkToplevel(self.parent)
        janela.title("Adicionar Paciente")
        janela.geometry("400x500")
        janela.resizable(False, False)
        janela.grab_set()

        ctk.CTkLabel(janela, text="Novo Paciente", font=("Segoe UI", 20, "bold")).pack(pady=20)

        self.nome = ctk.CTkEntry(janela, placeholder_text="Nome completo")
        self.nome.pack(pady=10, fill="x", padx=20)

        self.sexo = ctk.CTkComboBox(janela, values=["Masculino", "Feminino"])
        self.sexo.pack(pady=10, fill="x", padx=20)

        self.idade = ctk.CTkEntry(janela, placeholder_text="Idade")
        self.idade.pack(pady=10, fill="x", padx=20)

        self.telefone = ctk.CTkEntry(janela, placeholder_text="Telefone")
        self.telefone.pack(pady=10, fill="x", padx=20)

        self.bi = ctk.CTkEntry(janela, placeholder_text="BI")
        self.bi.pack(pady=10, fill="x", padx=20)

        self.nascimento = ctk.CTkEntry(janela, placeholder_text="Data nascimento (YYYY-MM-DD)")
        self.nascimento.pack(pady=10, fill="x", padx=20)

        self.morada = ctk.CTkEntry(janela, placeholder_text="Morada")
        self.morada.pack(pady=10, fill="x", padx=20)

        self._form_janela = janela
        ctk.CTkButton(janela, text="Guardar", fg_color="#2563EB", command=self.guardar_paciente).pack(pady=20)

    def guardar_paciente(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pacientes(nome, sexo, idade, telefone, bi, nascimento, morada)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.nome.get(), self.sexo.get(), self.idade.get(),
            self.telefone.get(), self.bi.get(),
            self.nascimento.get(), self.morada.get()
        ))
        conn.commit()
        conn.close()
        self._form_janela.destroy()
        messagebox.showinfo("Sucesso", "Paciente adicionado com sucesso!")
        self.refresh_table()

    def header(self):
        header = ctk.CTkFrame(self.parent, fg_color="#F4F6FB", height=90)
        header.pack(fill="x", padx=35, pady=(25, 15))
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(left, text="Pacientes", font=("Segoe UI", 30, "bold"), text_color="#183153").pack(anchor="w")
        ctk.CTkLabel(left, text="Gerir todos os pacientes registados.", font=("Segoe UI", 14), text_color="#6B7280").pack(anchor="w", pady=(3, 0))

        ctk.CTkButton(
            header, text="+ Adicionar Paciente",
            width=190, height=45, corner_radius=8,
            fg_color="#2563EB", hover_color="#1E4FD8",
            font=("Segoe UI", 15, "bold"),
            command=self.abrir_form_paciente,
        ).pack(side="right")

    def search_area(self):
        filtros = ctk.CTkFrame(self.parent, fg_color="transparent")
        filtros.pack(fill="x", padx=35, pady=(0, 20))

        self.txt_pesquisa = ctk.CTkEntry(
            filtros, placeholder_text="🔍 Pesquisar por nome, BI ou telefone...",
            height=45, corner_radius=8, border_width=1, font=("Segoe UI", 14),
        )
        self.txt_pesquisa.pack(side="left", fill="x", expand=True)

        self.combo_estado = ctk.CTkComboBox(filtros, values=["Todos", "Masculino", "Feminino"], width=180, height=45, corner_radius=8)
        self.combo_estado.pack(side="left", padx=(15, 0))
        self.combo_estado.set("Todos")

    def table_area(self):
        self.card = ctk.CTkFrame(self.parent, fg_color="white", corner_radius=12, border_width=1, border_color="#E4E7EC")
        self.card.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        self.content = ctk.CTkFrame(self.card, fg_color="white", corner_radius=12)
        self.content.pack(fill="both", expand=True)

        self.table_header()

        self.body = ctk.CTkScrollableFrame(self.content, fg_color="white", corner_radius=0)
        self.body.pack(fill="x", expand=False)

        self.table_rows()
        self.table_footer()

    def table_header(self):
        header = ctk.CTkFrame(self.content, fg_color="#C9C9C9", height=65, corner_radius=0)
        header.pack(fill="x", pady=(0, 2))
        header.pack_propagate(False)

        for texto, largura in [("ID", 60), ("Nome", 200), ("Sexo", 90), ("Idade", 80), ("Telefone", 160), ("BI", 170), ("Morada", 170), ("Ações", 100)]:
            ctk.CTkLabel(header, text=texto, width=largura, anchor="w", font=("Segoe UI", 13, "bold"), text_color="#475467").pack(side="left", padx=2)

        ctk.CTkFrame(self.content, height=1, fg_color="#E5E7EB").pack(fill="x")

    def table_rows(self):
        pacientes = listar_pacientes()
        larguras = [60, 200, 90, 80, 160, 170, 100]

        for i, paciente in enumerate(pacientes):
            linha = ctk.CTkFrame(self.body, fg_color="white", height=68)
            linha.pack(fill="x")
            linha.pack_propagate(False)

            for valor, largura in zip(paciente, larguras):
                cel = ctk.CTkFrame(linha, width=largura, fg_color="white")
                cel.pack(side="left", fill="y")
                cel.pack_propagate(False)
                ctk.CTkLabel(cel, text=str(valor), anchor="w", font=("Segoe UI", 13), text_color="#344054").pack(fill="both", padx=12)

            acoes = ctk.CTkFrame(linha, width=210, fg_color="white")
            acoes.pack(side="left", fill="y")
            acoes.pack_propagate(False)

            ctk.CTkButton(acoes, text="Editar", width=75, height=34, corner_radius=8, fg_color="#2563EB", hover_color="#1D4ED8", text_color="white", font=("Segoe UI", 12, "bold")).pack(side="left", padx=(10, 5), pady=10)
            ctk.CTkButton(acoes, text="Eliminar", width=85, height=34, corner_radius=8, fg_color="#EF4444", hover_color="#DC2626", text_color="white", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5, pady=10)

            if i < len(pacientes) - 1:
                ctk.CTkFrame(self.body, height=1, fg_color="#F1F5F9").pack(fill="x", padx=15)

    def table_footer(self):
        ctk.CTkFrame(self.content, height=1, fg_color="#E5E7EB").pack(fill="x")
        footer = ctk.CTkFrame(self.content, fg_color="white", height=70, corner_radius=0)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        total = len(listar_pacientes())
        ctk.CTkLabel(footer, text=f"Mostrando 1 a {min(10, total)} de {total} pacientes", font=("Segoe UI", 12), text_color="#667085").pack(side="left", padx=20)

        paginas = ctk.CTkFrame(footer, fg_color="transparent")
        paginas.pack(side="right", padx=20)

        for label, cor, texto_cor in [("<", "white", "#344054"), ("1", "#2563EB", "white"), (">", "white", "#344054")]:
            ctk.CTkButton(paginas, text=label, width=36, height=36, corner_radius=8, fg_color=cor, border_width=1, border_color="#D0D5DD", text_color=texto_cor, hover_color="#F9FAFB").pack(side="left", padx=3)

    def refresh_table(self):
        self.card.destroy()
        self.table_area()
