import customtkinter as ctk
from tkinter import messagebox
from database.database import conectar, listar_prioridades
from interface._base import _topbar_base


class PrioridadesContent:

    def __init__(self, parent):
        self.parent = parent
        self.id_consulta_selecionado = None
        self.frames_linhas = {}

        self.header()
        self.search_area()
        self.table_area()

    def abrir_form_prioridade(self):
        janela = ctk.CTkToplevel(self.parent)
        janela.title("Adicionar Prioridade")
        janela.geometry("400x400")
        janela.resizable(False, False)
        janela.grab_set()  # Bloqueia a janela de trás até fechar esta

        ctk.CTkLabel(janela, text="Nova Prioridade", font=("Segoe UI", 20, "bold")).pack(pady=20)

        # Criar os inputs guardando-os na instância (self)
        self.paciente_id = ctk.CTkEntry(janela, placeholder_text="ID do Paciente ou Consulta")
        self.paciente_id.pack(pady=10, fill="x", padx=20)

        self.prioridade_nivel = ctk.CTkComboBox(janela, values=["Urgente", "Alta", "Média", "Baixa"])
        self.prioridade_nivel.pack(pady=10, fill="x", padx=20)
        self.prioridade_nivel.set("Média") # Define um valor padrão

        self.medico = ctk.CTkEntry(janela, placeholder_text="Nome do Médico")
        self.medico.pack(pady=10, fill="x", padx=20)

        # Guarda a referência da janela para conseguir fechá-la depois
        self._form_janela = janela

        # BOTÃO CORRIGIDO: Vinculado diretamente à função self.guardar_prioridade
        ctk.CTkButton(
            janela, 
            text="Guardar", 
            fg_color="#2563EB", 
            hover_color="#1D4ED8",
            command=self.guardar_prioridade
        ).pack(pady=20)

    def guardar_prioridade(self):
        try:
            # 1. Abre a conexão com o banco de dados
            conn = conectar()
            cursor = conn.cursor()
            
            id_digitado = self.paciente_id.get()
            
            # 2. Busca se o paciente com esse ID realmente existe
            cursor.execute("SELECT nome FROM pacientes WHERE id = ?", (id_digitado,))
            paciente = cursor.fetchone()
            
            # 3. Se o paciente não for encontrado, avisa o usuário e para a execução
            if not paciente:
                messagebox.showerror("Aviso", f"Não existe nenhum paciente com o ID #{id_digitado} cadastrado!")
                conn.close()
                return
                
            # 4. Se o paciente existe, guarda na tabela 'prioridades'
            cursor.execute("""
                INSERT INTO prioridades(paciente_id, nivel, medico, hora_chegada)
                VALUES (?, ?, ?, time('now'))
            """, (
                id_digitado,
                self.prioridade_nivel.get(),
                self.medico.get()
            ))
            
            conn.commit()
            conn.close()
            
            # 5. Fecha o formulário e atualiza a tela
            self._form_janela.destroy()
            messagebox.showinfo("Sucesso", f"Prioridade adicionada com sucesso para o paciente: {paciente[0]}!")
            self.refresh_table()

        except Exception as erro:
            messagebox.showerror("Erro no Banco de Dados", f"Não foi possível guardar:\n{erro}")

    def header(self):
        header = ctk.CTkFrame(self.parent, fg_color="#F4F6FB", height=90)
        header.pack(fill="x", padx=35, pady=(25, 15))
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(left, text="Prioridades", font=("Segoe UI", 30, "bold"), text_color="#183153").pack(anchor="w")
        ctk.CTkLabel(left, text="Gerir o fluxo e níveis de prioridade dos atendimentos.", font=("Segoe UI", 14), text_color="#6B7280").pack(anchor="w", pady=(3, 0))

        ctk.CTkButton(
            header, text="+ Adicionar Prioridade",
            width=190, height=45, corner_radius=8,
            fg_color="#2563EB", hover_color="#1E4FD8",
            font=("Segoe UI", 15, "bold"),
            command=self.abrir_form_prioridade,
        ).pack(side="right")

    def search_area(self):
        filtros = ctk.CTkFrame(self.parent, fg_color="transparent")
        filtros.pack(fill="x", padx=35, pady=(0, 20))

        self.txt_pesquisa = ctk.CTkEntry(
            filtros, placeholder_text="🔍 Pesquisar por urgente ou médico...",
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
        self.card = ctk.CTkFrame(self.parent, fg_color="white", corner_radius=12, border_width=1, border_color="#E4E7EC")
        self.card.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        self.content = ctk.CTkFrame(self.card, fg_color="white", corner_radius=12)
        self.content.pack(fill="both", expand=True)

        self.table_header()

        self.body = ctk.CTkScrollableFrame(self.content, fg_color="white", corner_radius=0)
        self.body.pack(fill="both", expand=True)

        self.table_rows()
        self.table_footer()

    def table_header(self):
        header = ctk.CTkFrame(self.content, fg_color="#C9C9C9", height=65, corner_radius=0)
        header.pack(fill="x", pady=(0, 2))
        header.pack_propagate(False)

        colunas = [("ID", 60), ("Paciente", 200), ("Prioridade", 120), ("Hora Chegada", 150), ("Médico", 180), ("Ações", 100)]
        for texto, largura in colunas:
            ctk.CTkLabel(header, text=texto, width=largura, anchor="w", font=("Segoe UI", 13, "bold"), text_color="#475467").pack(side="left", padx=2)

        ctk.CTkFrame(self.content, height=1, fg_color="#E5E7EB").pack(fill="x")

    def table_rows(self):
        # Obtém o estado do ComboBox para filtrar a listagem
        filtro = self.combo_estado.get()
        dados = listar_prioridades(filtro if filtro != "Todos" else "Todos")
        larguras = [60, 200, 120, 150, 180]

        for i, registro in enumerate(dados):
            linha = ctk.CTkFrame(self.body, fg_color="white", height=68)
            linha.pack(fill="x")
            linha.pack_propagate(False)

            # Define a cor baseada na prioridade recebida
            prioridade = registro[2]
            cor_tag = {"Urgente": "#EF4444", "Alta": "#F59E0B", "Média": "#3B82F6", "Baixa": "#10B981"}.get(prioridade, "#344054")

            for valor, largura in zip(registro, larguras):
                cel = ctk.CTkFrame(linha, width=largura, fg_color="white")
                cel.pack(side="left", fill="y")
                cel.pack_propagate(False)
                
                lbl = ctk.CTkLabel(cel, text=str(valor), anchor="w", font=("Segoe UI", 13), text_color="#344054")
                lbl.pack(fill="both", padx=12)
                
                if str(valor) == prioridade:
                    lbl.configure(text_color=cor_tag, font=("Segoe UI", 13, "bold"))

            # Adiciona a mesma seção de ações (Botões Editar e Eliminar)
            acoes = ctk.CTkFrame(linha, width=210, fg_color="white")
            acoes.pack(side="left", fill="y")
            acoes.pack_propagate(False)

            ctk.CTkButton(acoes, text="Editar", width=75, height=34, corner_radius=8, fg_color="#2563EB", hover_color="#1D4ED8", text_color="white", font=("Segoe UI", 12, "bold")).pack(side="left", padx=(10, 5), pady=10)
            ctk.CTkButton(acoes, text="Eliminar", width=85, height=34, corner_radius=8, fg_color="#EF4444", hover_color="#DC2626", text_color="white", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5, pady=10)

            if i < len(dados) - 1:
                ctk.CTkFrame(self.body, height=1, fg_color="#F1F5F9").pack(fill="x", padx=15)

    def table_footer(self):
        ctk.CTkFrame(self.content, height=1, fg_color="#E5E7EB").pack(fill="x")
        footer = ctk.CTkFrame(self.content, fg_color="white", height=70, corner_radius=0)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        filtro = self.combo_estado.get()
        total = len(listar_prioridades(filtro))
        ctk.CTkLabel(footer, text=f"Mostrando 1 a {min(10, total)} de {total} registros", font=("Segoe UI", 12), text_color="#667085").pack(side="left", padx=20)

        paginas = ctk.CTkFrame(footer, fg_color="transparent")
        paginas.pack(side="right", padx=20)

        for label, cor, texto_cor in [("<", "white", "#344054"), ("1", "#2563EB", "white"), (">", "white", "#344054")]:
            ctk.CTkButton(paginas, text=label, width=36, height=36, corner_radius=8, fg_color=cor, border_width=1, border_color="#D0D5DD", text_color=texto_cor, hover_color="#F9FAFB").pack(side="left", padx=3)

    def refresh_table(self):
        self.card.destroy()
        self.table_area()