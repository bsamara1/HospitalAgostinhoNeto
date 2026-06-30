import customtkinter as ctk
from tkinter import messagebox
from utils.helpers import centralizar_janela

class CancelamentoContent:

    def __init__(self, parent):
        self.parent = parent
        self.header()
        self.search_area()
        self.table_area()

    def abrir_form_cancelamento(self):
        janela = ctk.CTkToplevel(self.parent)
        janela.title("Cancelar Consulta")
        janela.geometry("400x320")
        janela.resizable(False, False)
        janela.grab_set()
        centralizar_janela(janela, 450, 250)

        ctk.CTkLabel(janela, text="Cancelar por ID do Paciente", font=("Segoe UI", 20, "bold")).pack(pady=20)

        self.paciente_id = ctk.CTkEntry(janela, placeholder_text="Digite o ID do Paciente")
        self.paciente_id.pack(pady=15, fill="x", padx=20)

        self._form_janela = janela
        ctk.CTkButton(janela, text="Confirmar Cancelamento", fg_color="#EF4444", hover_color="#DC2626", 
                      font=("Segoe UI", 13, "bold"), command=self.guardar_cancelamento).pack(pady=20)

    def guardar_cancelamento(self):
        id_p = self.paciente_id.get()
        if not id_p:
            messagebox.showwarning("Aviso", "Por favor, insira o ID do paciente.")
            return

        # Confirmação extra para segurança do usuário, já que vai apagar dados
        if not messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja ELIMINAR definitivamente o Paciente ID #{id_p} e cancelar seu registro?"):
            return

        try:
            # Importação segura da nova função do banco de dados
            from database.database import eliminar_e_cancelar_paciente
            
            # Executa a remoção e o salvamento no histórico simultaneamente
            sucesso = eliminar_e_cancelar_paciente(id_p)
            
            if not sucesso:
                messagebox.showerror("Erro", f"Não foi encontrado nenhum paciente cadastrado com o ID #{id_p}.")
                return
            
            self._form_janela.destroy()
            messagebox.showinfo("Sucesso", f"Paciente #{id_p} cancelado e eliminado do sistema com sucesso!")
            self.refresh_table()

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível processar o cancelamento: {e}")

    def limpar_historico_acao(self):
        if messagebox.askyesno("Confirmar Limpeza", "Tens a certeza que desejas apagar todo o histórico de cancelamentos e reiniciar os IDs?"):
            try:
                from database.database import conectar
                
                conn = conectar()
                cursor = conn.cursor()
                
                # 1. Apaga todos os registos do histórico
                cursor.execute("DELETE FROM historico_consultas")
                
                # 2. Zera o contador do AUTOINCREMENT para esta tabela começar de 1
                cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'historico_consultas'")
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Sucesso", "O histórico foi limpo e o ID reiniciado para 1!")
                self.refresh_table() # Atualiza a tela
                
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível limpar: {e}")

    def header(self):
        header = ctk.CTkFrame(self.parent, fg_color="#F4F6FB", height=90)
        header.pack(fill="x", padx=35, pady=(25, 15))
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(left, text="Cancelamento", font=("Segoe UI", 30, "bold"), text_color="#183153").pack(anchor="w")
        ctk.CTkLabel(left, text="Gerir e cancelar consultas da fila.", font=("Segoe UI", 14), text_color="#6B7280").pack(anchor="w", pady=(3, 0))

        # 1. Primeiro criamos a caixinha (botoes_frame) para segurar os botões
        botoes_frame = ctk.CTkFrame(header, fg_color="transparent")
        botoes_frame.pack(side="right")

        # 2. Agora colocamos o botão de limpar dentro dessa caixinha
        ctk.CTkButton(
            botoes_frame, text="🗑️ Limpar Histórico",
            width=160, height=45, corner_radius=8,
            fg_color="#374151", hover_color="#1F2937",
            font=("Segoe UI", 14, "bold"),
            command=self.limpar_historico_acao,
        ).pack(side="left", padx=(0, 10))

        # 3. E por fim, o botão de cancelar consulta também dentro da caixinha
        ctk.CTkButton(
            botoes_frame, text="+ Cancelar Consulta",
            width=190, height=45, corner_radius=8,
            fg_color="#EF4444", hover_color="#DC2626",
            font=("Segoe UI", 14, "bold"),
            command=self.abrir_form_cancelamento,
        ).pack(side="left")

    def search_area(self):
        filtros = ctk.CTkFrame(self.parent, fg_color="transparent")
        filtros.pack(fill="x", padx=35, pady=(0, 20))

        self.txt_pesquisa = ctk.CTkEntry(filtros, placeholder_text="🔍 Pesquisar...", height=45, corner_radius=8)
        self.txt_pesquisa.pack(side="left", fill="x", expand=True)

        self.combo_estado = ctk.CTkComboBox(filtros, values=["Todos", "Em Espera", "Reagendado", "Cancelado"], width=180, height=45, command=lambda e: self.refresh_table())
        self.combo_estado.pack(side="left", padx=(15, 0))
        self.combo_estado.set("Todos")

    def table_area(self):
        self.card = ctk.CTkFrame(self.parent, fg_color="white", corner_radius=12, border_width=1, border_color="#E4E7EC")
        self.card.pack(fill="both", expand=True, padx=35, pady=(0, 25))
        self.content = ctk.CTkFrame(self.card, fg_color="white", corner_radius=12)
        self.content.pack(fill="both", expand=True)
        self.table_header()
        self.body = ctk.CTkScrollableFrame(self.content, fg_color="white", corner_radius=0)
        self.body.pack(fill="both", expand=True)
        self.table_rows()

    def table_header(self):
        header = ctk.CTkFrame(self.content, fg_color="#C9C9C9", height=65, corner_radius=0)
        header.pack(fill="x", pady=(0, 2))
        header.pack_propagate(False)

        # Definir as colunas corretas para o histórico de eliminados
        colunas = [("ID Registo", 100), ("Nome do Paciente", 200), ("Ação", 150), ("Informação / Estado", 350)]
        for texto, largura in colunas:
            ctk.CTkLabel(header, text=texto, width=largura, anchor="w", font=("Segoe UI", 13, "bold"), text_color="#475467").pack(side="left", padx=5)

    def table_rows(self):
        try:
            from database.database import listar_historico_cancelamentos
            cancelamentos = listar_historico_cancelamentos()
            larguras = [100, 200, 150, 350]

            if not cancelamentos:
                return

            for i, linha_dados in enumerate(cancelamentos):
                linha = ctk.CTkFrame(self.body, fg_color="white", height=68)
                linha.pack(fill="x")
                linha.pack_propagate(False)

                for valor, largura in zip(linha_dados, larguras):
                    cel = ctk.CTkFrame(linha, width=largura, fg_color="white")
                    cel.pack(side="left", fill="y")
                    cel.pack_propagate(False)
                    
                    lbl = ctk.CTkLabel(cel, text=str(valor), anchor="w", font=("Segoe UI", 13), text_color="#344054")
                    lbl.pack(fill="both", padx=12)
                    
                    # CORREÇÃO AQUI: Aceita tanto "Cancelado" como "Cancelamento" para pintar de vermelho
                    if str(valor) in ["Cancelado", "Cancelamento"]:
                        lbl.configure(text_color="#EF4444", font=("Segoe UI", 13, "bold"))

                if i < len(cancelamentos) - 1:
                    ctk.CTkFrame(self.body, height=1, fg_color="#F1F5F9").pack(fill="x", padx=15)
        except Exception as e:
            print(f"Erro ao carregar linhas de cancelamento: {e}")

    def refresh_table(self):
        # Destrói todos os elementos dentro do card para limpar a parte visual
        for widget in self.body.winfo_children():
            widget.destroy()
        
        # Reconstrói as linhas atualizadas (que agora estarão vazias)
        self.table_rows()