import customtkinter as ctk
from tkinter import messagebox
from interface._base import _topbar_base
from database.database import listar_consultas_paciente, reagendar_consulta_por_paciente

class ReagendarContent:

    def __init__(self, parent, id_paciente):
        self.parent = parent
        self.id_paciente = id_paciente

        _topbar_base(parent, "Reagendar Consulta")
        self.build_ui()

    def build_ui(self):
        box = ctk.CTkFrame(self.parent, fg_color="#F4F6FB")
        box.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(box, text="Reagendar Consulta",
                     font=("Segoe UI", 24, "bold"),
                     text_color="#0B2A4A").pack(anchor="w", pady=(0, 10))

        consultas = listar_consultas_paciente(self.id_paciente)

        texto = "" if consultas else "Não existem consultas ativas para este paciente."
        ctk.CTkLabel(box, text=texto,
                     font=("Segoe UI", 14),
                     text_color="#667085").pack(anchor="w", pady=(0, 15))

        if not consultas:
            return

        form = ctk.CTkFrame(box, fg_color="white", corner_radius=12)
        form.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(form, text="Nova Data (YYYY-MM-DD)", font=("Segoe UI", 13)).pack(anchor="w", padx=15, pady=(15, 5))
        self.nova_data = ctk.CTkEntry(form, placeholder_text="2026-07-01")
        self.nova_data.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkLabel(form, text="Nova Hora (HH:MM)", font=("Segoe UI", 13)).pack(anchor="w", padx=15, pady=(5, 5))
        self.nova_hora = ctk.CTkEntry(form, placeholder_text="14:30")
        self.nova_hora.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(form, text="Guardar Reagendamento",
                      fg_color="#2563EB", hover_color="#1D4ED8",
                      font=("Segoe UI", 13, "bold"),
                      command=self.guardar_reagendamento).pack(pady=(0, 15), padx=15)

    def guardar_reagendamento(self):
        nova_data = self.nova_data.get()
        nova_hora = self.nova_hora.get()

        if not nova_data or not nova_hora:
            messagebox.showwarning("Aviso", "Por favor preencha a nova data e hora.")
            return

        sucesso = reagendar_consulta_por_paciente(self.id_paciente, nova_data, nova_hora)

        if not sucesso:
            messagebox.showerror("Erro", "Não foi possível reagendar a consulta.")
            return

        messagebox.showinfo("Sucesso", "Consulta reagendada com sucesso.")
