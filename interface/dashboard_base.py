import customtkinter as ctk
from interface._base import _topbar_base


class DashboardBase:

    def __init__(self, parent, title="Dashboard"):
        self.parent = parent

        _topbar_base(parent, title)

        self.build_cards()
        self.build_center()

    # =========================
    # CARDS
    # =========================
    def build_cards(self):
        frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(30, 20))
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        cards = self.get_cards_data()

        for i, (title, value, color) in enumerate(cards):
            card = ctk.CTkFrame(frame, fg_color=color, corner_radius=18, width=260, height=180)
            card.grid(row=0, column=i, padx=12, sticky="nsew")
            card.grid_propagate(False)

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(expand=True, fill="both", padx=20, pady=20)

            ctk.CTkLabel(inner, text=title, text_color="white",
                         font=("Segoe UI", 15)).pack(anchor="w", padx=20, pady=(20, 5))

            ctk.CTkLabel(inner, text=value, text_color="white",
                         font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=20)

    # =========================
    # CENTRO
    # =========================
    def build_center(self):
        center = ctk.CTkFrame(self.parent, fg_color="transparent")
        center.pack(fill="both", expand=True, padx=20, pady=15)

        center.grid_columnconfigure((0, 1, 2), weight=1)
        center.grid_rowconfigure(0, weight=1)

        self.table_ui(center)
        self.middle_ui(center)
        self.right_ui(center)

    # =========================
    # TABLE
    # =========================
    def table_ui(self, parent):
        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        box.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(box, text=self.table_title(),
                     font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=10)

        header = ctk.CTkFrame(box, fg_color="transparent")
        header.pack(fill="x", padx=20)

        for col in self.table_columns():
            ctk.CTkLabel(header, text=col, width=120,
                         anchor="w").pack(side="left")

        for row in self.get_table_data():
            r = ctk.CTkFrame(box, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=3)

            for val, w in zip(row, self.table_widths()):
                ctk.CTkLabel(r, text=val, width=w,
                             anchor="w").pack(side="left")

    # =========================
    # MIDDLE
    # =========================
    def middle_ui(self, parent):
        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        box.grid(row=0, column=1, sticky="nsew", padx=10)

        ctk.CTkLabel(box, text=self.middle_title(),
                     font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=10)

        for item in self.get_middle_data():
            self.render_middle_item(box, item)

    # =========================
    # RIGHT
    # =========================
    def right_ui(self, parent):
        box = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        box.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(box, text=self.right_title(),
                     font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=10)

        for item in self.get_right_data():
            self.render_right_item(box, item)

    # =========================
    # DEFAULTS (override)
    # =========================
    def get_cards_data(self): return []
    def table_title(self): return ""
    def table_columns(self): return []
    def table_widths(self): return []
    def get_table_data(self): return []
    def middle_title(self): return ""
    def get_middle_data(self): return []
    def right_title(self): return ""
    def get_right_data(self): return []
    def render_middle_item(self, box, item): pass
    def render_right_item(self, box, item): pass