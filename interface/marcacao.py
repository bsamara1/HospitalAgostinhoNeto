import customtkinter as ctk
from tkinter import messagebox

# Importa a função que a tua colega resolveu no banco de dados
from database.database import listar_consultas_geral 
from interface._base import _topbar_base
from utils.helpers import centralizar_janela


class MarcacaoContent:

    def __init__(self, parent):
        self.parent = parent

        # Renderiza os blocos visuais idênticos aos dos Pacientes e Cancelamentos
        self.header()
        self.search_area()
        self.table_area()

    # =========================================================================
    # CABEÇALHO DO ADMIN
    # =========================================================================
    def header(self):
        header = ctk.CTkFrame(self.parent, fg_color="#F4F6FB", height=90)
        header.pack(fill="x", padx=35, pady=(25, 15))
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(left, text="Marcação de Consultas", font=("Segoe UI", 30, "bold"), text_color="#183153").pack(anchor="w")
        ctk.CTkLabel(left, text="Painel de Administração: Consultas agendadas pelos pacientes.", font=("Segoe UI", 14), text_color="#6B7280").pack(anchor="w", pady=(3, 0))

    # =========================================================================
    # ÁREA DE FILTROS (ADMIN)
    # =========================================================================
    def search_area(self):
        filtros = ctk.CTkFrame(self.parent, fg_color="transparent")
        filtros.pack(fill="x", padx=35, pady=(0, 20))

        self.txt_pesquisa = ctk.CTkEntry(
            filtros, placeholder_text="🔍 Pesquisar por paciente, médico ou especialidade...",
            height=45, corner_radius=8, border_width=1, font=("Segoe UI", 14),
        )
        self.txt_pesquisa.pack(side="left", fill="x", expand=True)

        # Combo de estados que aciona a pesquisa filtrada
        self.combo_estado = ctk.CTkComboBox(
            filtros, 
            values=["Todos", "Agendado", "Concluído", "Cancelado"], 
            width=180, height=45, corner_radius=8,
            command=lambda _: self.refresh_table()
        )
        self.combo_estado.pack(side="left", padx=(15, 0))
        self.combo_estado.set("Todos")

    # =========================================================================
    # ÁREA DA TABELA (CARD ARREDONDADO)
    # =========================================================================
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

        # Colunas com o ID da consulta, Nome do Paciente que inseriu os dados, Médico escolhido, Data, Hora e Estado
        colunas = [("ID", 60), ("Paciente", 200), ("Médico", 180), ("Data", 110), ("Hora", 90), ("Estado", 120), ("Ações", 210)]
        for texto, largura in colunas:
            ctk.CTkLabel(header, text=texto, width=largura, anchor="w", font=("Segoe UI", 13, "bold"), text_color="#475467").pack(side="left", padx=2)

        ctk.CTkFrame(self.content, height=1, fg_color="#E5E7EB").pack(fill="x")

    def table_rows(self):
        try:
            # Carrega as consultas dinâmicas usando a query inteligente que junta tabelas
            consultas = listar_consultas_geral(filtro_estado=self.combo_estado.get()) 
            larguras = [60, 200, 180, 110, 90]

            if not consultas:
                ctk.CTkLabel(self.body, text="Nenhum agendamento pendente realizado por pacientes.", font=("Segoe UI", 14), text_color="#6B7280").pack(pady=40)
                return

            for i, c in enumerate(consultas):
                linha = ctk.CTkFrame(self.body, fg_color="white", height=68)
                linha.pack(fill="x")
                linha.pack_propagate(False)

                # c[0]=ID, c[1]=Nome Paciente, c[2]=Nome Médico, c[3]=Data, c[4]=Hora
                for valor, largura in zip(c[:5], larguras):
                    cel = ctk.CTkFrame(linha, width=largura, fg_color="white")
                    cel.pack(side="left", fill="y")
                    cel.pack_propagate(False)
                    ctk.CTkLabel(cel, text=str(valor), anchor="w", font=("Segoe UI", 13), text_color="#344054").pack(fill="both", padx=12)

                # Coluna de Estado (Com badge colorido baseado no estado)
                estado_cel = ctk.CTkFrame(linha, width=120, fg_color="white")
                estado_cel.pack(side="left", fill="y")
                estado_cel.pack_propagate(False)
                lbl_est = ctk.CTkLabel(estado_cel, text=str(c[5]), anchor="w", font=("Segoe UI", 13, "bold"))
                lbl_est.pack(fill="both", padx=12)
                
                if str(c[5]) == "Agendado": lbl_est.configure(text_color="#2563EB")
                elif str(c[5]) == "Concluído": lbl_est.configure(text_color="#16A34A")
                elif str(c[5]) == "Cancelado": lbl_est.configure(text_color="#EF4444")

                # Botões para o Admin gerir a marcação do paciente
                acoes = ctk.CTkFrame(linha, width=210, fg_color="white")
                acoes.pack(side="left", fill="y")
                acoes.pack_propagate(False)

                ctk.CTkButton(acoes, text="Reagendar", width=85, height=34, corner_radius=8, fg_color="#4B5563", hover_color="#374151").pack(side="left", padx=(10, 5), pady=10)
                ctk.CTkButton(acoes, text="Cancelar", width=85, height=34, corner_radius=8, fg_color="#EF4444", hover_color="#DC2626").pack(side="left", padx=5, pady=10)

                if i < len(consultas) - 1:
                    ctk.CTkFrame(self.body, height=1, fg_color="#F1F5F9").pack(fill="x", padx=15)
        except Exception as e:
            print(f"Erro ao carregar consultas no painel admin: {e}")

    def table_footer(self):
        ctk.CTkFrame(self.content, height=1, fg_color="#E5E7EB").pack(fill="x")
        footer = ctk.CTkFrame(self.content, fg_color="white", height=70, corner_radius=0)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        total = len(listar_consultas_geral(filtro_estado=self.combo_estado.get()))
        ctk.CTkLabel(footer, text=f"Total: {total} consultas agendadas pelos pacientes.", font=("Segoe UI", 12), text_color="#667085").pack(side="left", padx=20)

    def refresh_table(self):
        for widget in self.body.winfo_children():
            widget.destroy()
        if hasattr(self, 'card') and self.card:
            self.card.destroy()
        self.table_area()