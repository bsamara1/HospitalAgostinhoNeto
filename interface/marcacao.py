import customtkinter as ctk
from database import conectar
from PIL import Image
from tkinter import messagebox

class Marcacao(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("HAN - Hospital Agostinho Neto")
        
        # Em vez de chamar direto, agendamos para rodar logo após a janela abrir:
        self.after(10, lambda: self.state("zoomed"))

        self.configure(fg_color="#F4F6FB")
        self.ui()

    # =========================
    # UI PRINCIPAL
    # =========================
    def ui(self):
        self.container = ctk.CTkFrame(self, fg_color="#F4F6FB")
        self.container.pack(fill="both", expand=True)

        self.sidebar_ui()
        self.main_ui()

    # =========================
    # SIDEBAR
    # =========================
    def sidebar_ui(self):
        self.sidebar = ctk.CTkFrame(
            self.container,
            width=240,
            fg_color="#0B2A4A"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = ctk.CTkImage(Image.open("assets/logo.png"), size=(40, 40))

        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(25, 35), padx=20, fill="x")

        ctk.CTkLabel(logo_frame, image=logo, text="").grid(row=0, column=0, rowspan=2, padx=10)

        ctk.CTkLabel(
            logo_frame,
            text="HAN",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        ).grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            logo_frame,
            text="Hospital Agostinho Neto",
            font=("Segoe UI", 13),
            text_color="#D6E4F0"
        ).grid(row=1, column=1, sticky="w")

        # ICONS
        def icon(path):
            return ctk.CTkImage(Image.open(path), size=(20, 20))

        menu = [
            ("Painel Principal", icon("assets/casa.png")),
            ("Pacientes", icon("assets/utilizadores.png")),
            ("Médicos", icon("assets/perfil.png")),
            ("Marcações", icon("assets/agendar.png")),
            ("Reagendamento", icon("assets/reagendar.png")),
            ("Cancelamento", icon("assets/cancelar.png")),
            ("Triagem", icon("assets/triagem.png")),
            ("Prioridades", icon("assets/prioridade.png")),
            ("Relatórios", icon("assets/relatorio.png")),
            ("Definições", icon("assets/definicao.png")),
        ]

        # MENU
        for text, ic in menu:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                image=ic,
                compound="left",
                fg_color="transparent",
                text_color="white",
                anchor="w",
                hover_color="#11457B",
                height=45,
                command=lambda nome=text: self.abrir_menu(nome)
            ).pack(fill="x", padx=15, pady=3)

        # TERMINAR SESSÃO (fora do for)
        ctk.CTkButton(
            self.sidebar,
            text="Terminar Sessão",
            image=icon("assets/sair.png"),
            compound="left",
            fg_color="transparent",
            text_color="#FF6B6B",
            hover_color="#2A3F5F",
            anchor="w",
            height=45,
            command=self.terminar_sessao
        ).pack(side="bottom", fill="x", padx=15, pady=20)
        
        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color="#35506E"
        ).pack(side="bottom", fill="x", padx=15, pady=(0, 10))

    def terminar_sessao(self):
        confirmar = messagebox.askyesno(
            "Terminar Sessão",
            "Deseja realmente terminar a sessão?"
        )

        if confirmar:
            self.destroy()
            from interface.login import Login
            root = ctk.CTk()
            Login(root)
            root.mainloop()

    def abrir_menu(self, menu):
        if menu == "Pacientes" and self.__class__.__name__ in ["Pacientes", "pacientes"]:
            return
        if menu == "Médicos" and self.__class__.__name__ in ["Medicos", "medicos"]:
            return
        if menu == "Marcações" and self.__class__.__name__ in ["Marcacao", "marcacao"]:
            return

        self.destroy()

        if menu in ["Dashboard", "Painel Principal"]:
            from interface.dashboard import Dashboard
            Dashboard().mainloop()
        elif menu == "Pacientes":
            from interface.pacientes import Pacientes
            Pacientes().mainloop()   
        elif menu == "Médicos":
            import interface.medicos as medicos_modulo
            try:
                medicos_modulo.Medicos().mainloop()
            except AttributeError:
                medicos_modulo.medicos().mainloop()
        elif menu == "Marcações":
            from interface.marcacao import Marcacao
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
        self.main = ctk.CTkFrame(
            self.container,
            fg_color="#F4F6FB"
        )
        self.main.pack(
            side="left",
            fill="both",
            expand=True
        )
        self.topbar()
        self.formulario()

    # =========================
    # TOPBAR
    # =========================
    def topbar(self):
        topbar = ctk.CTkFrame(
            self.main,
            fg_color="#F4F6FB",
            height=60
        )
        topbar.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            topbar,
            text="Marcações",
            font=("Segoe UI", 22, "bold"),
            text_color="#0B2A4A"
        ).pack(side="left", padx=20)

        avatar = ctk.CTkImage(
            Image.open("assets/perfil.png"),
            size=(42, 42)
        )

        user = ctk.CTkFrame(
            topbar,
            fg_color="transparent"
        )
        user.pack(side="right")

        ctk.CTkLabel(
            user,
            image=avatar,
            text=""
        ).pack(side="left", padx=10)

        texto = ctk.CTkFrame(
            user,
            fg_color="transparent"
        )
        texto.pack(side="left")

        ctk.CTkLabel(
            texto,
            text="Administrador",
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            texto,
            text="Administrador",
            text_color="gray"
        ).pack(anchor="w")

        linha = ctk.CTkFrame(
            self.main,
            height=1,
            fg_color="#D8DEE9"
        )
        linha.pack(fill="x", pady=(5, 0))

    # =========================
    # FORMULÁRIO (Reestruturado)
    # =========================
    def formulario(self):
        frame = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=15
        )
        frame.pack(
            fill="x",
            padx=30,
            pady=30
        )

        ctk.CTkLabel(
            frame,
            text="Nova Marcação",
            font=("Segoe UI", 22, "bold"),
            text_color="#0B2A4A"
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            pady=25
        )

        # --- LINHA 1: Paciente e Médico ---
        ctk.CTkLabel(frame, text="Paciente").grid(row=1, column=0, padx=20, pady=10)
        self.paciente = ctk.CTkEntry(frame, width=300, placeholder_text="Nome do paciente")
        self.paciente.grid(row=1, column=1, padx=10)

        ctk.CTkLabel(frame, text="Médico").grid(row=1, column=2, padx=20, pady=10)
        lista_nomes_medicos = []
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM medicos")
            lista_nomes_medicos = [linha[0] for linha in cursor.fetchall()]
            conn.close()
        except Exception as e:
            print(f"Erro ao carregar médicos: {e}")

        if not lista_nomes_medicos:
            lista_nomes_medicos = ["Nenhum médico encontrado"]

        self.medico = ctk.CTkComboBox(frame, width=300, values=lista_nomes_medicos)
        self.medico.grid(row=1, column=3, padx=10)
        self.medico.set(lista_nomes_medicos[0])

        # --- LINHA 2: NOVOS CAMPOS (Telefone e Nascimento) ---
        ctk.CTkLabel(frame, text="Telefone").grid(row=2, column=0, padx=20, pady=10)
        self.telefone = ctk.CTkEntry(frame, width=300, placeholder_text="Ex: 9xxxxxx")
        self.telefone.grid(row=2, column=1, padx=10)

        ctk.CTkLabel(frame, text="Nascimento").grid(row=2, column=2, padx=20, pady=10)
        self.nascimento = ctk.CTkEntry(frame, width=300, placeholder_text="dd/mm/aaaa")
        self.nascimento.grid(row=2, column=3, padx=10)

        # --- LINHA 3: Data e Hora ---
        ctk.CTkLabel(frame, text="Data").grid(row=3, column=0, padx=20, pady=10)
        self.data = ctk.CTkEntry(frame, width=300, placeholder_text="dd/mm/aaaa")
        self.data.grid(row=3, column=1, padx=10)

        ctk.CTkLabel(frame, text="Hora").grid(row=3, column=2, padx=20, pady=10)
        self.hora = ctk.CTkEntry(frame, width=300, placeholder_text="08:00")
        self.hora.grid(row=3, column=3, padx=10)

        # --- LINHA 4: Prioridade e Especialidade ---
        ctk.CTkLabel(frame, text="Prioridade").grid(row=4, column=0, padx=20, pady=10)
        self.prioridade = ctk.CTkComboBox(
            frame, width=300, 
            values=["Baixa", "Média", "Alta", "Urgente"]
        )
        self.prioridade.set("Baixa")
        self.prioridade.grid(row=4, column=1, padx=10)

        ctk.CTkLabel(frame, text="Especialidade").grid(row=4, column=2, padx=20, pady=10)
        self.especialidade = ctk.CTkComboBox(
            frame, width=300, 
            values=["Cardiologia", "Pediatria", "Ortopedia", "Neurologia", "Medicina Geral", "Ginecologia"]
        )
        self.especialidade.set("Medicina Geral")
        self.especialidade.grid(row=4, column=3, padx=10)

        # --- LINHA 5: Botões ---
        botoes = ctk.CTkFrame(frame, fg_color="transparent")
        botoes.grid(row=5, column=0, columnspan=4, pady=30)

        ctk.CTkButton(
            botoes,
            text="Guardar Marcação",
            width=180,
            command=self.guardar_marcacao
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            botoes,
            text="Limpar",
            width=150,
            fg_color="gray",
            command=self.limpar_campos
        ).pack(side="left", padx=10)

    # =========================
    # GUARDAR
    # =========================
    def guardar_marcacao(self):
        paciente = self.paciente.get().strip()
        telefone = self.telefone.get().strip()
        nascimento = self.nascimento.get().strip()
        medico = self.medico.get()
        data = self.data.get().strip()
        hora = self.hora.get().strip()
        prioridade = self.prioridade.get()

        if not paciente or not data or not hora:
            messagebox.showwarning("Campos Vazios", "Preencha pelo menos o Nome do Paciente, Data e Hora.")
            return

        # Fallbacks amigáveis caso o utilizador deixe vazio os dados secundários
        if not telefone:
            telefone = "Não Registado"
        if not nascimento:
            nascimento = "dd/mm/aaaa"

        try:
            conn = conectar()
            cursor = conn.cursor()

            # Verificar se o paciente já existe
            cursor.execute("SELECT id FROM pacientes WHERE nome=?", (paciente,))
            resultado = cursor.fetchone()

            if resultado:
                paciente_id = resultado[0]
                # Opcional: Atualiza o registo se já existir para manter os novos dados inseridos
                cursor.execute("""
                    UPDATE pacientes SET telefone=?, nascimento=? WHERE id=?
                """, (telefone, nascimento, paciente_id))
            else:
                # Inserir novo paciente com os dados completos obtidos do formulário
                cursor.execute("""
                    INSERT INTO pacientes (nome, telefone, nascimento) 
                    VALUES (?, ?, ?)
                """, (paciente, telefone, nascimento))
                conn.commit()
                paciente_id = cursor.lastrowid

            # Verificar médico
            cursor.execute("SELECT id FROM medicos WHERE nome=?", (medico,))
            medico_resultado = cursor.fetchone()

            if medico_resultado is None:
                messagebox.showerror("Erro", "Médico não encontrado.")
                conn.close()
                return

            medico_id = medico_resultado[0]

            # Inserir a consulta vinculando os IDs corretos
            cursor.execute("""
                INSERT INTO consultas(paciente, medico, data, hora, prioridade, estado)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (paciente_id, medico_id, data, hora, prioridade, "Agendada"))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Marcação registada com sucesso.")
            self.limpar_campos()

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    # =========================
    # LIMPAR
    # =========================
    def limpar_campos(self):
        self.paciente.delete(0, "end")
        self.telefone.delete(0, "end")
        self.nascimento.delete(0, "end")
        self.data.delete(0, "end")
        self.hora.delete(0, "end")
        self.prioridade.set("Baixa")
        self.especialidade.set("Medicina Geral")


if __name__ == "__main__":
    app = Marcacao()
    app.mainloop()