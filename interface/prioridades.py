import customtkinter as ctk
from tkinter import messagebox, simpledialog
from database.database import listar_prioridades, atualizar_prioridade_consulta
from interface._base import _topbar_base


class PrioridadesContent:

    def __init__(self, parent):
        self.parent = parent
        self.filtro_atual = "Todos"
        self.id_consulta_selecionado = None
        self.frames_linhas = {}

        _topbar_base(parent, "Prioridades")
        self.main_ui()

    def main_ui(self):
        frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=35, pady=(10, 25))

        ctk.CTkLabel(frame, text="Fila de Prioridades", font=("Segoe UI", 30, "bold"),
                     text_color="#183153").pack(anchor="w")

        toolbar = ctk.CTkFrame(frame, fg_color="transparent")
        toolbar.pack(fill="x", pady=(20, 15))

        self.filtro_switch = ctk.CTkSegmentedButton(
            toolbar, values=["Todos", "Urgente", "Alta", "Média", "Baixa"],
            height=40, font=("Segoe UI", 12, "bold"), command=self.filtrar,
        )
        self.filtro_switch.set("Todos")
        self.filtro_switch.pack(side="left")

        ctk.CTkButton(toolbar, text="🔄 Atualizar Lista", width=140, height=40,
                      fg_color="#10B981", hover_color="#059669",
                      font=("Segoe UI", 12, "bold"), command=self.refresh_table).pack(side="right", padx=5)

        ctk.CTkButton(toolbar, text="✏️ Alterar Prioridade", width=160, height=40,
                      fg_color="#2563EB", hover_color="#1E4FD8",
                      font=("Segoe UI", 12, "bold"), command=self.alterar_prioridade).pack(side="right", padx=5)

        self._table_parent = frame
        self.table_area()

    def table_area(self):
        self.card = ctk.CTkFrame(self._table_parent, fg_color="white", corner_radius=12,
                                  border_width=1, border_color="#E4E7EC")
        self.card.pack(fill="both", expand=True)

        t_header = ctk.CTkFrame(self.card, fg_color="#EAEFF8", height=50, corner_radius=0)
        t_header.pack(fill="x")
        t_header.pack_propagate(False)

        for texto, largura in [("ID", 60), ("Paciente", 220), ("Prioridade", 130), ("Hora de Chegada", 160), ("Médico", 200)]:
            ctk.CTkLabel(t_header, text=texto, width=largura, anchor="w",
                         font=("Segoe UI", 13, "bold"), text_color="#183153").pack(side="left", padx=15)

        self.body = ctk.CTkScrollableFrame(self.card, fg_color="white", corner_radius=0)
        self.body.pack(fill="both", expand=True)
        self.table_rows()

    def table_rows(self):
        for w in self.body.winfo_children():
            w.destroy()

        dados = listar_prioridades(self.filtro_atual)
        self.frames_linhas = {}

        if not dados:
            ctk.CTkLabel(self.body, text="Nenhum paciente em espera nesta categoria.",
                         font=("Segoe UI", 14), text_color="gray").pack(pady=40)
            return

        for c_id, paciente, prioridade, hora, medico in dados:
            linha = ctk.CTkFrame(self.body, fg_color="white", height=55, cursor="hand2")
            linha.pack(fill="x", pady=2)
            linha.pack_propagate(False)
            linha.bind("<Button-1>", lambda e, id=c_id: self.selecionar_linha(id))

            cor_tag = {"Urgente": "#EF4444", "Alta": "#F59E0B", "Média": "#3B82F6", "Baixa": "#10B981"}.get(prioridade, "gray")

            for val, larg in [(f"#{c_id}", 60), (paciente, 220), (prioridade, 130), (hora, 160), (medico, 200)]:
                lbl = ctk.CTkLabel(linha, text=str(val), width=larg, anchor="w", font=("Segoe UI", 13))
                lbl.pack(side="left", padx=15, pady=12)
                lbl.bind("<Button-1>", lambda e, id=c_id: self.selecionar_linha(id))
                if val == prioridade:
                    lbl.configure(text_color=cor_tag, font=("Segoe UI", 13, "bold"))

            self.frames_linhas[c_id] = linha

    def selecionar_linha(self, consulta_id):
        if self.id_consulta_selecionado in self.frames_linhas:
            self.frames_linhas[self.id_consulta_selecionado].configure(fg_color="white")
        self.id_consulta_selecionado = consulta_id
        self.frames_linhas[consulta_id].configure(fg_color="#E0EBF7")

    def filtrar(self, valor):
        self.filtro_atual = valor
        self.table_rows()

    def alterar_prioridade(self):
        if not self.id_consulta_selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um paciente da tabela clicando em cima da linha.")
            return
        nova = simpledialog.askstring("Alterar Prioridade",
                                      "Escreva a nova prioridade:\n(Urgente, Alta, Média, Baixa)")
        if nova and nova.capitalize() in ["Urgente", "Alta", "Média", "Baixa"]:
            atualizar_prioridade_consulta(self.id_consulta_selecionado, nova.capitalize())
            self.refresh_table()
            messagebox.showinfo("Sucesso", "Prioridade atualizada com sucesso!")
        elif nova:
            messagebox.showerror("Erro", "Prioridade inválida! Escolha entre Urgente, Alta, Média ou Baixa.")

    def refresh_table(self):
        self.id_consulta_selecionado = None
        self.card.destroy()
        self.table_area()
