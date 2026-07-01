import customtkinter as ctk
from PIL import Image


def _placeholder(parent, titulo):
    """Ecrã em desenvolvimento — mostra mensagem centralizada."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="both", expand=True)

    card = ctk.CTkFrame(frame, fg_color="white", corner_radius=20,
                        border_width=1, border_color="#E0E4EC", width=420, height=220)
    card.place(relx=0.5, rely=0.45, anchor="center")
    card.pack_propagate(False)

    ctk.CTkLabel(card, text="🚧", font=("Segoe UI", 48)).pack(pady=(30, 5))
    ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 20, "bold"),
                 text_color="#0B2A4A").pack()
    ctk.CTkLabel(card, text="Esta secção está em desenvolvimento.",
                 font=("Segoe UI", 13), text_color="#6B7280").pack(pady=(5, 0))


def _topbar_base(parent, titulo):
    topbar = ctk.CTkFrame(parent, fg_color="#F4F6FB", height=60)
    topbar.pack(fill="x", padx=20, pady=10)
    topbar.pack_propagate(False)

    ctk.CTkLabel(topbar, text=titulo, font=("Segoe UI", 22, "bold"), text_color="#0B2A4A").pack(side="left", padx=20)

    ctk.CTkFrame(parent, height=1, fg_color="#D8DEE9", corner_radius=0).pack(fill="x", pady=(5, 0))

    user = ctk.CTkFrame(topbar, fg_color="transparent")
    user.pack(side="right")

    try:
        avatar = ctk.CTkImage(Image.open("assets/perfil.png"), size=(42, 42))
        lbl = ctk.CTkLabel(user, image=avatar, text="")
        lbl._img = avatar
        lbl.pack(side="left", padx=10)
    except Exception:
        pass

    texto = ctk.CTkFrame(user, fg_color="transparent")
    texto.pack(side="left")
    ctk.CTkLabel(texto, text="Administrador", font=("Segoe UI", 15, "bold")).pack(anchor="w")
    ctk.CTkLabel(texto, text="Administrador", text_color="gray").pack(anchor="w")
