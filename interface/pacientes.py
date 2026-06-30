import customtkinter as ctk
from tkinter import messagebox
from database.database import conectar, listar_pacientes
from interface._base import _topbar_base
from utils.helpers import centralizar_janela


class PacientesContent:

    def __init__(self, parent):
        self.parent = parent
        self.header()
        self.search_area()
        self.table_area()

    def abrir_form_paciente(self):
        janela = ctk.CTkToplevel(self.parent)
        janela.title("Adicionar Paciente")
        janela.geometry("400x500")
        janela.resizable(False, False)
        janela.grab_set()
        centralizar_janela(janela, 500, 500)

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
        nome = self.nome.get().strip()
        sexo = self.sexo.get().strip()
        idade = self.idade.get().strip()
        telefone = self.telefone.get().strip()
        bi = self.bi.get().strip()
        nascimento = self.nascimento.get().strip()
        morada = self.morada.get().strip()

        if not all([nome, sexo, idade, telefone, bi, nascimento, morada]):
            messagebox.showwarning("Erro", "Preencha todos os campos do paciente.")
            return

        if not idade.isdigit():
            messagebox.showwarning("Erro", "A idade deve ser um número válido.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pacientes(nome, sexo, idade, telefone, bi, nascimento, morada)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                nome, sexo, int(idade), telefone, bi,
                nascimento, morada
            ))
            conn.commit()
            conn.close()
            self._form_janela.destroy()
            messagebox.showinfo("Sucesso", "Paciente adicionado com sucesso!")
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível adicionar o paciente: {e}")

    # =========================================================================
    # NOVA FUNÇÃO: Executada quando clicas no botão Eliminar da tabela
    # =========================================================================
    def eliminar_paciente_acao(self, paciente_id):
        if messagebox.askyesno("Confirmar Cancelamento", f"Tens a certeza que desejas ELIMINAR o Paciente ID #{paciente_id}?\nEsta ação irá registá-lo como 'Cancelado' no histórico."):
            try:
                # Importa a função inteligente que criámos no teu database.py
                from database.database import eliminar_e_cancelar_paciente
                
                sucesso = eliminar_e_cancelar_paciente(paciente_id)
                
                if sucesso:
                    messagebox.showinfo("Sucesso", f"Paciente #{paciente_id} eliminado e movido para Cancelamentos!")
                    self.refresh_table()  # Atualiza instantaneamente a tabela de Pacientes
                else:
                    messagebox.showerror("Erro", "Não foi possível encontrar este paciente na base de dados.")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível processar: {e}")

    def limpar_todos_acao(self):
        if messagebox.askyesno("Confirmar Limpeza", "Tens a certeza que desejas apagar TODOS os pacientes e reiniciar os IDs para 1?"):
            try:
                from database.database import limpar_todos_pacientes_e_id
                
                limpar_todos_pacientes_e_id()
                messagebox.showinfo("Sucesso", "Todos os pacientes foram eliminados e o próximo ID será o 1!")
                self.refresh_table() # Atualiza a tabela no ecrã (ficará vazia)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível limpar: {e}")

    def header(self):
        header = ctk.CTkFrame(self.parent, fg_color="#F4F6FB", height=90)
        header.pack(fill="x", padx=35, pady=(25, 15))
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(left, text="Pacientes", font=("Segoe UI", 30, "bold"), text_color="#183153").pack(anchor="w")
        ctk.CTkLabel(left, text="Gerir todos os pacientes registados.", font=("Segoe UI", 14), text_color="#6B7280").pack(anchor="w", pady=(3, 0))

        # Contentor para os botões do lado direito
        botoes_frame = ctk.CTkFrame(header, fg_color="transparent")
        botoes_frame.pack(side="right")

        # NOVO BOTÃO: Limpar Tudo e Reiniciar ID
        ctk.CTkButton(
            botoes_frame, text="🗑️ Limpar Tudo",
            width=140, height=45, corner_radius=8,
            fg_color="#374151", hover_color="#1F2937",
            font=("Segoe UI", 14, "bold"),
            command=self.limpar_todos_acao,
        ).pack(side="left", padx=(0, 10))

        # Botão que já tinhas de Adicionar Paciente
        ctk.CTkButton(
            botoes_frame, text="+ Adicionar Paciente",
            width=190, height=45, corner_radius=8,
            fg_color="#2563EB", hover_color="#1E4FD8",
            font=("Segoe UI", 15, "bold"),
            command=self.abrir_form_paciente,
        ).pack(side="left")

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
        self.body.pack(fill="both", expand=True)  # Mudado para fill="both" para aceitar o scroll vertical direito

        self.table_rows()
        self.table_footer()

    def table_header(self):
        header = ctk.CTkFrame(self.content, fg_color="#C9C9C9", height=65, corner_radius=0)
        header.pack(fill="x", pady=(0, 2))
        header.pack_propagate(False)

        for texto, largura in [("ID", 60), ("Nome", 200), ("Sexo", 90), ("Idade", 80), ("Telefone", 160), ("BI", 170), ("Morada", 170), ("Ações", 210)]:
            ctk.CTkLabel(header, text=texto, width=largura, anchor="w", font=("Segoe UI", 13, "bold"), text_color="#475467").pack(side="left", padx=2)

        ctk.CTkFrame(self.content, height=1, fg_color="#E5E7EB").pack(fill="x")

    def table_rows(self):
        pacientes = listar_pacientes()
        larguras = [60, 200, 90, 80, 160, 170, 170] # Alinhada a largura da morada de acordo com o header

        for i, paciente in enumerate(pacientes):
            p_id = paciente[0]  # O primeiro item é o ID do paciente

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
            
            # ALTERADO: O botão Eliminar agora executa a nossa função passando o ID correto da linha!
            ctk.CTkButton(acoes, text="Eliminar", width=85, height=34, corner_radius=8, 
                          fg_color="#EF4444", hover_color="#DC2626", text_color="white", 
                          font=("Segoe UI", 12, "bold"),
                          command=lambda id_atual=p_id: self.eliminar_paciente_acao(id_atual)).pack(side="left", padx=5, pady=10)

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
        # 1. Limpa todas as linhas antigas que ficaram desenhadas no ecrã
        for widget in self.body.winfo_children():
            widget.destroy()
            
        # 2. Destrói o card antigo por completo para forçar a reconstrução total
        if hasattr(self, 'card') and self.card:
            self.card.destroy()
            
        # 3. Desenha a tabela novamente (agora totalmente atualizada a partir do banco de dados)
        self.table_area()