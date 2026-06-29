import customtkinter as ctk
from PIL import Image
from tkinter import messagebox, simpledialog
from database.database import conectar, listar_prioridades, atualizar_prioridade_consulta

class Prioridades(ctk.CTk):

    def __init__(self, usuario=None):
        super().__init__()
        self.usuario = usuario if usuario else {"nome": "Utilizador", "perfil": "Administrador"}

        self.title("HAN - Gestão de Prioridades")
        self.after(10, lambda: self.state("zoomed"))        
        self.configure(fg_color="#F4F6FB")    
        
        self.filtro_atual = "Todos"
        self.linha_selecionada = None
        self.id_consulta_selecionado = None
        
        self.ui()

    def ui(self):
        self.container = ctk.CTkFrame(self, fg_color="#F4F6FB")
        self.container.pack(fill="both", expand=True)
        self.sidebar_ui()
        self.main_ui()

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

        def icon(path): return ctk.CTkImage(Image.open(path), size=(20, 20))

        menu = [
            ("Painel Principal", icon("assets/casa.png")), ("Pacientes", icon("assets/utilizadores.png")),
            ("Médicos", icon("assets/perfil.png")), ("Marcações", icon("assets/agendar.png")),
            ("Reagendamento", icon("assets/reagendar.png")), ("Cancelamento", icon("assets/cancelar.png")),
            ("Triagem", icon("assets/triagem.png")), ("Prioridades", icon("assets/prioridade.png")),
            ("Relatórios", icon("assets/relatorio.png")), ("Definições", icon("assets/definicao.png")),
        ]

        for text, ic in menu:
            bg_color = "#2563EB" if text == "Prioridades" else "transparent"
            ctk.CTkButton(
                self.sidebar, text=text, image=ic, compound="left", fg_color=bg_color,
                text_color="white", anchor="w", hover_color="#11457B", height=45,
                command=lambda nome=text: self.abrir_menu(nome)
            ).pack(fill="x", padx=15, pady=3)

    def main_ui(self):
        self.main = ctk.CTkFrame(self.container, fg_color="#F4F6FB")
        self.main.pack(side="left", fill="both", expand=True, padx=35, pady=25)

        # Cabeçalho
        lbl_titulo = ctk.CTkLabel(self.main, text="Fila de Prioridades", font=("Segoe UI", 30, "bold"), text_color="#183153")
        lbl_titulo.pack(anchor="w")
        
        # --- ZONA DE FILTROS E BOTÕES ---
        toolbar = ctk.CTkFrame(self.main, fg_color="transparent")
        toolbar.pack(fill="x", pady=(20, 15))

        # Filtros (Segmented Button fica excelente visualmente)
        self.filtro_switch = ctk.CTkSegmentedButton(
            toolbar, values=["Todos", "Urgente", "Alta", "Média", "Baixa"],
            height=40, font=("Segoe UI", 12, "bold"), command=self.filtrar
        )
        self.filtro_switch.set("Todos")
        self.filtro_switch.pack(side="left")

        # Botão Atualizar Lista
        ctk.CTkButton(
            toolbar, text="🔄 Atualizar Lista", width=140, height=40, fg_color="#10B981",
            hover_color="#059669", font=("Segoe UI", 12, "bold"), command=self.refresh_table
        ).pack(side="right", padx=5)

        # Botão Alterar Prioridade
        self.btn_alterar = ctk.CTkButton(
            toolbar, text="✏️ Alterar Prioridade", width=160, height=40, fg_color="#2563EB",
            hover_color="#1E4FD8", font=("Segoe UI", 12, "bold"), command=self.alterar_prioridade
        )
        self.btn_alterar.pack(side="right", padx=5)

        # Tabela
        self.table_area()

    def table_area(self):
        self.card = ctk.CTkFrame(self.main, fg_color="white", corner_radius=12, border_width=1, border_color="#E4E7EC")
        self.card.pack(fill="both", expand=True)

        # Cabeçalho da Tabela
        t_header = ctk.CTkFrame(self.card, fg_color="#EAEFF8", height=50, corner_radius=0)
        t_header.pack(fill="x")
        t_header.pack_propagate(False)

        colunas = [("ID", 60), ("Paciente", 220), ("Prioridade", 130), ("Hora de Chegada", 160), ("Médico", 200)]
        for texto, largura in colunas:
            ctk.CTkLabel(t_header, text=texto, width=largura, anchor="w", font=("Segoe UI", 13, "bold"), text_color="#183153").pack(side="left", padx=15)

        self.body = ctk.CTkScrollableFrame(self.card, fg_color="white", corner_radius=0)
        self.body.pack(fill="both", expand=True)
        self.table_rows()

    def table_rows(self):
        # Remove registros anteriores se houver
        for widget in self.body.winfo_children():
            widget.destroy()

        dados_consultas = listar_prioridades(self.filtro_atual)
        self.frames_linhas = {}

        if not dados_consultas:
            ctk.CTkLabel(self.body, text="Nenhum paciente em espera nesta categoria.", font=("Segoe UI", 14), text_color="gray").pack(pady=40)
            return

        for consulta in dados_consultas:
            c_id, paciente, prioridade, hora, medico = consulta

            linha = ctk.CTkFrame(self.body, fg_color="white", height=55, cursor="hand2")
            linha.pack(fill="x", pady=2)
            linha.pack_propagate(False)

            # Efeito visual de seleção de linha
            linha.bind("<Button-1>", lambda e, id=c_id: self.selecionar_linha(id))

            # Cores das tags de prioridade
            cor_tag = "#EF4444" if prioridade == "Urgente" else "#F59E0B" if prioridade == "Alta" else "#3B82F6" if prioridade == "Média" else "#10B981"

            # Renderização das Células
            valores = [(f"#{c_id}", 60), (paciente, 220), (prioridade, 130), (hora, 160), (medico, 200)]
            for val, larg in valores:
                lbl = ctk.CTkLabel(linha, text=str(val), width=larg, anchor="w", font=("Segoe UI", 13))
                lbl.pack(side="left", padx=15, pady=12)
                lbl.bind("<Button-1>", lambda e, id=c_id: self.selecionar_linha(id))
                
                if val == prioridade:
                    lbl.configure(text_color=cor_tag, font=("Segoe UI", 13, "bold"))

            self.frames_linhas[c_id] = linha

    def selecionar_linha(self, consulta_id):
        # Limpa seleção anterior
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

        # Pop-up simples para escolher a nova prioridade
        nova = simpledialog.askstring("Alterar Prioridade", "Escreva a nova prioridade:\n(Urgente, Alta, Média, Baixa)")
        if nova and nova.capitalize() in ["Urgente", "Alta", "Média", "Baixa"]:
            atualizar_prioridade_consulta(self.id_consulta_selecionado, nova.capitalize())
            self.refresh_table()
            messagebox.showinfo("Sucesso", "Prioridade atualizada com sucesso!")
        elif nova:
            messagebox.showerror("Erro", "Prioridade inválida! Escolha entre Urgente, Alta, Média ou Baixa.")

    def refresh_table(self):
        self.id_consulta_selecionado = None
        self.table_rows()

    def abrir_menu(self, menu):
        self.destroy()
        if menu == "Pacientes":
            from interface.pacientes import Pacientes
            Pacientes(usuario=self.usuario).mainloop()
        elif menu == "Dashboard" or menu == "Painel Principal":
            from interface.dashboard import Dashboard
            Dashboard(usuario=self.usuario).mainloop()
        elif menu == "Prioridades":
            Prioridades(usuario=self.usuario).mainloop()
        elif menu == "Definições":
            from interface.definicao import Definicao
            Definicao(usuario=self.usuario).mainloop()

if __name__ == "__main__":
    app = Prioridades()
    app.mainloop()