import customtkinter as ctk
from interface.dashboard import DashboardAdmin
from database.database import consultas_hoje, consultar_prioridade, consultar_agenda_medicos


class DashboardContent(DashboardAdmin):

    def __init__(self, parent):
        super().__init__(parent, "Painel Principal")

    # =========================
    # CARDS
    # =========================
    def get_cards_data(self):
        return [
            ("Consultas Hoje", "48", "#2E86C1"),
            ("Médicos", "12", "#28B463"),
            ("Urgências", "18", "#E74C3C"),
            ("Tempo Médio", "32 min", "#F39C12")
        ]

    # =========================
    # TABELA
    # =========================
    def table_title(self):
        return "Consultas de Hoje"

    def table_columns(self):
        return ["Paciente", "Médico", "Hora", "Prioridade", "Estado"]

    def table_widths(self):
        return [120, 120, 80, 100, 100]

    def get_table_data(self):
        return consultas_hoje()

    # =========================
    # MIDDLE
    # =========================
    def middle_title(self):
        return "Consultas por Prioridade"

    def get_middle_data(self):
        return consultar_prioridade()

    def render_middle_item(self, box, item):
        prioridade, total = item

        row = ctk.CTkFrame(box, fg_color="#F4F6FB")
        row.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            row,
            text=prioridade,
            width=120,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            row,
            text=f"{total} consultas"
        ).pack(side="left")

    # =========================
    # RIGHT
    # =========================
    def right_title(self):
        return "Agenda dos Médicos"

    def get_right_data(self):
        return consultar_agenda_medicos()

    def render_right_item(self, box, item):
        nome, especialidade, horario = item

        card = ctk.CTkFrame(box, fg_color="#F4F6FB", corner_radius=8)
        card.pack(fill="x", padx=15, pady=6)

        ctk.CTkLabel(
            card,
            text=nome,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=10, pady=(8, 0))

        ctk.CTkLabel(
            card,
            text=especialidade,
            text_color="gray"
        ).pack(anchor="w", padx=10)

        ctk.CTkLabel(
            card,
            text=horario,
            text_color="#2E86C1"
        ).pack(anchor="w", padx=10, pady=(0, 8))