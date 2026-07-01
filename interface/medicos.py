import customtkinter as ctk
from tkinter import messagebox
from database.database import conectar, listar_medicos,inserir_medico
from interface._base import _topbar_base
from utils.helpers import centralizar_janela


class MedicosContent:

    def __init__(self, parent):
        self.parent = parent
        self.header()
        self.search_area()
        self.table_area()

    def abrir_form_medico(self):
        janela = ctk.CTkToplevel(self.parent)
        janela.title("Adicionar Médico")
        janela.geometry("400x550")
        janela.resizable(False, False)
        janela.grab_set()
        centralizar_janela(janela, 500, 400)

        ctk.CTkLabel(janela, text="Novo Médico", font=("Segoe UI", 20, "bold")).pack(pady=20)

        self.nome = ctk.CTkEntry(janela, placeholder_text="Nome completo")
        self.nome.pack(pady=10, fill="x", padx=20)

        self.email = ctk.CTkEntry(janela, placeholder_text="Email")
        self.email.pack(pady=10, fill="x", padx=20)

        self.especialidade = ctk.CTkEntry(janela, placeholder_text="Especialidade")
        self.especialidade.pack(pady=10, fill="x", padx=20)

        self.telefone = ctk.CTkEntry(janela, placeholder_text="Telefone")
        self.telefone.pack(pady=10, fill="x", padx=20)

        self.estado = ctk.CTkComboBox(janela, values=["Disponível", "Ocupado", "Férias"], state="readonly")
        self.estado.set("Disponível")
        self.estado.pack(pady=10, fill="x", padx=20)

        self._form_janela = janela
        ctk.CTkButton(janela, text="Guardar", fg_color="#2563EB", hover_color="#1E4FD8",
                      command=self.guardar_medico).pack(pady=20)

    from database.database import inserir_medico

    def guardar_medico(self):
        nome = self.nome.get()
        email = self.email.get()
        especialidade = self.especialidade.get()
        telefone = self.telefone.get()
        estado = self.estado.get()

        username, senha = inserir_medico(
            nome, email, especialidade, telefone, estado
        )

        self._form_janela.destroy()

        self.mostrar_credenciais(username, senha)

        self.refresh_table()
        
    def mostrar_credenciais(self, username, senha):
        win = ctk.CTkToplevel(self.parent)
        win.title("Credenciais do Médico")
        win.geometry("400x280")
        win.grab_set()

        ctk.CTkLabel(
            win,
            text="Médico criado com sucesso!",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(win, text=f"Username: {username}").pack(pady=10)
        ctk.CTkLabel(win, text=f"Senha: {senha}").pack(pady=10)

        ctk.CTkButton(
            win,
            text="Copiar",
            command=lambda: win.clipboard_append(f"{username} | {senha}")
        ).pack(pady=15)

        ctk.CTkButton(
            win,
            text="Fechar",
            command=win.destroy
        ).pack()

    def header(self):
        header = ctk.CTkFrame(self.parent, fg_color="#F4F6FB", height=90)
        header.pack(fill="x", padx=35, pady=(25, 15))
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(left, text="Médicos", font=("Segoe UI", 30, "bold"), text_color="#183153").pack(anchor="w")
        ctk.CTkLabel(left, text="Gerir todos os médicos registados.", font=("Segoe UI", 14), text_color="#6B7280").pack(anchor="w")

        ctk.CTkButton(
            header, text="+ Adicionar Médico",
            width=200, height=45, fg_color="#2563EB", hover_color="#1E4FD8",
            font=("Segoe UI", 15, "bold"), command=self.abrir_form_medico,
        ).pack(side="right")

    def search_area(self):
        bar = ctk.CTkFrame(self.parent, fg_color="transparent")
        bar.pack(fill="x", padx=35, pady=(0, 12))

        self.txt_pesquisa = ctk.CTkEntry(
            bar, placeholder_text="🔍  Pesquisar por nome, email ou especialidade...",
            height=42, corner_radius=8, border_width=1, font=("Segoe UI", 13),
        )
        self.txt_pesquisa.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.txt_pesquisa.bind("<KeyRelease>", lambda e: self.table_rows())

        self.combo_estado = ctk.CTkComboBox(
            bar, values=["Todos", "Disponível", "Ocupado", "Férias"],
            width=160, height=42, corner_radius=8, font=("Segoe UI", 13),
            command=lambda _: self.table_rows(),
        )
        self.combo_estado.set("Todos")
        self.combo_estado.pack(side="left")

    def table_area(self):
        self.card = ctk.CTkFrame(self.parent, fg_color="white", corner_radius=12,
                                  border_width=1, border_color="#E4E7EC")
        self.card.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        self.content = ctk.CTkFrame(self.card, fg_color="white")
        self.content.pack(fill="both", expand=True)

        self.table_header()

        self.body = ctk.CTkScrollableFrame(self.content, fg_color="white")
        self.body.pack(fill="both", expand=True)

        self.table_rows()
        self.table_footer()

    # Pesos das colunas: ID, Nome, Email, Especialidade, Telefone, Estado, Ações
    _COL_WEIGHTS = [0, 3, 3, 2, 2, 1, 0]
    _COL_MINSIZES = [60, 160, 160, 130, 120, 110, 190]

    def _grid_cols(self, frame):
        for i, (w, m) in enumerate(zip(self._COL_WEIGHTS, self._COL_MINSIZES)):
            frame.grid_columnconfigure(i, weight=w, minsize=m)

    def table_header(self):
        header = ctk.CTkFrame(self.content, fg_color="#EAEFF8", height=52, corner_radius=0)
        header.pack(fill="x", pady=(0, 0))
        header.pack_propagate(False)
        self._grid_cols(header)

        for col, texto in enumerate(["ID", "Nome", "Email", "Especialidade", "Telefone", "Estado", "Ações"]):
            ctk.CTkLabel(header, text=texto, anchor="w",
                         font=("Segoe UI", 13, "bold"), text_color="#344054").grid(
                row=0, column=col, sticky="ew", padx=(16, 4), pady=14)

        ctk.CTkFrame(self.content, height=1, fg_color="#E5E7EB").pack(fill="x")

    def table_rows(self):
        for w in self.body.winfo_children():
            w.destroy()

        termo = self.txt_pesquisa.get().lower().strip() if hasattr(self, "txt_pesquisa") else ""
        estado = self.combo_estado.get() if hasattr(self, "combo_estado") else "Todos"

        medicos = [
            m for m in listar_medicos()
            if (not termo or any(termo in str(v).lower() for v in m[1:4]))
            and (estado == "Todos" or str(m[5]).lower() == estado.lower())
        ]

        for i, medico in enumerate(medicos):
            bg = "white" if i % 2 == 0 else "#FAFBFC"

            linha = ctk.CTkFrame(self.body, fg_color=bg, height=60, corner_radius=0)
            linha.pack(fill="x")
            linha.pack_propagate(False)
            self._grid_cols(linha)

            for col, valor in enumerate(medico):
                ctk.CTkLabel(linha, text=str(valor), anchor="w",
                             font=("Segoe UI", 13), text_color="#344054").grid(
                    row=0, column=col, sticky="ew", padx=(16, 4), pady=10)

            # Botões de ação na última coluna
            acoes = ctk.CTkFrame(linha, fg_color="transparent")
            acoes.grid(row=0, column=6, sticky="ew", padx=(8, 12), pady=10)

            ctk.CTkButton(acoes, text="Editar", width=75, height=34, corner_radius=8,
                          fg_color="#2563EB", hover_color="#1D4ED8", text_color="white",
                          font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 6))
            ctk.CTkButton(acoes, text="Eliminar", width=85, height=34, corner_radius=8,
                          fg_color="#EF4444", hover_color="#DC2626", text_color="white",
                          font=("Segoe UI", 12, "bold")).pack(side="left")

            ctk.CTkFrame(self.body, height=1, fg_color="#F1F5F9").pack(fill="x", padx=15)

    def table_footer(self):
        ctk.CTkFrame(self.content, height=1, fg_color="#E5E7EB").pack(fill="x")
        footer = ctk.CTkFrame(self.content, fg_color="white", height=70, corner_radius=0)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        total = len(listar_medicos())
        ctk.CTkLabel(footer, text=f"Mostrando 1 a {min(10, total)} de {total} médicos",
                     font=("Segoe UI", 12), text_color="#667085").pack(side="left", padx=20)

        paginas = ctk.CTkFrame(footer, fg_color="transparent")
        paginas.pack(side="right", padx=20)

        for label, cor, texto_cor in [("<", "white", "#344054"), ("1", "#2563EB", "white"), (">", "white", "#344054")]:
            ctk.CTkButton(paginas, text=label, width=36, height=36, corner_radius=8,
                          fg_color=cor, border_width=1, border_color="#D0D5DD",
                          text_color=texto_cor, hover_color="#F9FAFB").pack(side="left", padx=3)

<<<<<<< HEAD
        self.destroy()

        if menu == "Dasboard":
            from interface.dashboard import Dashboard

            Dashboard().mainloop()

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

    # =========================
    # TOPBAR
    # =========================
    def topbar(self):

        topbar = ctk.CTkFrame(self.main, fg_color="#F4F6FB", height=60)
        topbar.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            topbar,
            text="Medicos",
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
# RUN APP
# =========================
if __name__ == "__main__":
    app = Medicos()
    app.mainloop()
=======
    def refresh_table(self):
        self.card.destroy()
        self.table_area()
>>>>>>> e6c7e2e51d53b791fbb4f265798f0f6350352252
