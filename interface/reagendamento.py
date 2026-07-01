import customtkinter as ctk
from tkinter import messagebox
from utils.helpers import centralizar_janela

class ReagendamentoContent:

    def __init__(self, parent):
        self.parent = parent
        self.header()
        self.search_area()
        self.table_area()

    def abrir_form_reagendamento(self):
        janela = ctk.CTkToplevel(self.parent)
        janela.title("Reagendar Consulta")
        janela.geometry("400x400")
        janela.resizable(False, False)
        janela.grab_set()
        centralizar_janela(janela, 450, 350)

        ctk.CTkLabel(janela, text="Reagendar por ID do Paciente", font=("Segoe UI", 20, "bold")).pack(pady=20)

        self.paciente_id = ctk.CTkEntry(janela, placeholder_text="Digite o ID do Paciente")
        self.paciente_id.pack(pady=10, fill="x", padx=20)

        self.nova_data = ctk.CTkEntry(janela, placeholder_text="Nova Data (YYYY-MM-DD)")
        self.nova_data.pack(pady=10, fill="x", padx=20)

        self.nova_hora = ctk.CTkEntry(janela, placeholder_text="Nova Hora (HH:MM)")
        self.nova_hora.pack(pady=10, fill="x", padx=20)

        self._form_janela = janela
        ctk.CTkButton(janela, text="Guardar Reagendamento", fg_color="#2563EB", hover_color="#1E4FD8", 
                      font=("Segoe UI", 13, "bold"), command=self.guardar_reagendamento).pack(pady=20)

    def guardar_reagendamento(self):
        id_p = self.paciente_id.get()
        data = self.nova_data.get()
        hora = self.nova_hora.get()

        if not id_p or not data or not hora:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        try:
            # Importação segura para evitar tela branca
            from database.database import reagendar_consulta_por_paciente
            
            sucesso = reagendar_consulta_por_paciente(id_p, data, hora)
            
            if not sucesso:
                messagebox.showerror("Erro", f"Não foi encontrada nenhuma consulta ativa para o Paciente ID #{id_p}.")
                return
            
            self._form_janela.destroy()
            messagebox.showinfo("Sucesso", f"Consulta do Paciente #{id_p} reagendada com sucesso!")
            self.refresh_table()

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível reagendar: {e}")

    def header(self):
        header = ctk.CTkFrame(self.parent, fg_color="#F4F6FB", height=90)
        header.pack(fill="x", padx=35, pady=(25, 15))
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(left, text="Reagendamento", font=("Segoe UI", 30, "bold"), text_color="#183153").pack(anchor="w")
        ctk.CTkLabel(left, text="Modificar datas e horários de consultas marcadas.", font=("Segoe UI", 14), text_color="#6B7280").pack(anchor="w", pady=(3, 0))

        ctk.CTkButton(
            header, text="+ Reagendar Consulta",
            width=190, height=45, corner_radius=8,
            fg_color="#2563EB", hover_color="#1E4FD8",
            font=("Segoe UI", 15, "bold"),
            command=self.abrir_form_reagendamento,
        ).pack(side="right")

    def search_area(self):
        filtros = ctk.CTkFrame(self.parent, fg_color="transparent")
        filtros.pack(fill="x", padx=35, pady=(0, 20))

        self.txt_pesquisa = ctk.CTkEntry(filtros, placeholder_text="🔍 Pesquisar...", height=45, corner_radius=8)
        self.txt_pesquisa.pack(side="left", fill="x", expand=True)

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
        for texto, largura in [("ID", 60), ("Paciente", 180), ("Médico", 180), ("Data", 120), ("Hora", 100), ("Estado", 130)]:
            ctk.CTkLabel(header, text=texto, width=largura, anchor="w", font=("Segoe UI", 13, "bold"), text_color="#475467").pack(side="left", padx=5)

    def table_rows(self):
        try:
            from database.database import listar_consultas_geral
            consultas = listar_consultas_geral("Todos")
            larguras = [60, 180, 180, 120, 100, 130]

            for i, consulta in enumerate(consultas):
                linha = ctk.CTkFrame(self.body, fg_color="white", height=68)
                linha.pack(fill="x")
                linha.pack_propagate(False)

                estado = consulta[5]
                cor_estado = {"Cancelado": "#EF4444", "Em Espera": "#3B82F6", "Reagendado": "#F59E0B"}.get(estado, "#344054")

                for valor, largura in zip(consulta, larguras):
                    cel = ctk.CTkFrame(linha, width=largura, fg_color="white")
                    cel.pack(side="left", fill="y")
                    cel.pack_propagate(False)
                    lbl = ctk.CTkLabel(cel, text=str(valor), anchor="w", font=("Segoe UI", 13), text_color="#344054")
                    lbl.pack(fill="both", padx=12)
                    if str(valor) == estado:
                        lbl.configure(text_color=cor_estado, font=("Segoe UI", 13, "bold"))

                if i < len(consultas) - 1:
                    ctk.CTkFrame(self.body, height=1, fg_color="#F1F5F9").pack(fill="x", padx=15)
        except Exception as e:
            print(f"Erro ao carregar linhas: {e}")

<<<<<<< HEAD
            app.mainloop()
        if menu == "Pacientes":
            from interface.pacientes import Pacientes
            Pacientes().mainloop()   
        
        elif menu == "Marcações":
            from interface.Agendamento import Marcacao
            Marcacao().mainloop() 
        elif menu == "Dashboard":
            from interface.dashboard import Dashboard
            Dashboard().mainloop() 
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
            text="Reagendamnetos",
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
    app = Reagendamento()
    app.mainloop()
=======
    def refresh_table(self):
        self.card.destroy()
        self.table_area()
>>>>>>> e6c7e2e51d53b791fbb4f265798f0f6350352252
