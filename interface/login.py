import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
from database.database import conectar

class LoginContent:

    def __init__(self, parent, on_success, on_register):
        self.parent = parent
        self.on_success = on_success
        self.on_register = on_register

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self._build()

    # ==================================================
    # UI
    # ==================================================
    def _build(self):

        self.main = ctk.CTkFrame(self.parent, fg_color="#F5F7FB")
        self.main.pack(fill="both", expand=True)

        # ==================================================
        # SIDEBAR
        # ==================================================
        sidebar = ctk.CTkFrame(
            self.main,
            width=120,
            fg_color="#081A3C",
            corner_radius=0
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # ==================================================
        # LEFT AREA
        # ==================================================
        left_area = ctk.CTkFrame(self.main, fg_color="#F5F7FB")
        left_area.pack(side="left", fill="both", expand=True)

        # ==================================================
        # LOGO
        # ==================================================
        logo_frame = ctk.CTkFrame(left_area, fg_color="transparent")
        logo_frame.place(x=90, y=130)

        try:
            logo = Image.open("assets/logo.png")
            self._logo_img = ctk.CTkImage(
                light_image=logo,
                dark_image=logo,
                size=(180, 180)
            )

            ctk.CTkLabel(
                logo_frame,
                image=self._logo_img,
                text=""
            ).pack(side="left")

        except Exception:
            pass

        ctk.CTkLabel(
            logo_frame,
            text="HAN",
            font=("Segoe UI", 80, "bold"),
            text_color="#081A3C"
        ).pack(side="left", padx=(30, 0))

        # ==================================================
        # TEXTO
        # ==================================================
        ctk.CTkLabel(
            left_area,
            text="Hospital Agostinho Neto\nSistema de Gestão Hospitalar",
            font=("Segoe UI", 25),
            text_color="#4B5563",
            justify="center"
        ).place(x=230, y=300)

        # ==================================================
        # IMAGEM
        # ==================================================
        try:
            img = Image.open("assets/hospital.png")
            self._main_img = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(720, 350)
            )

            ctk.CTkLabel(
                left_area,
                image=self._main_img,
                text=""
            ).place(x=0, y=480)

        except Exception:
            pass

        # ==================================================
        # CARD
        # ==================================================
        card = ctk.CTkFrame(
            self.main,
            width=580,
            height=760,
            fg_color="white",
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB"
        )

        card.place(relx=0.74, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # ==================================================
        # TITULO
        # ==================================================
        ctk.CTkLabel(
            card,
            text="Bem-vindo de volta!",
            font=("Segoe UI", 32, "bold"),
            text_color="#081A3C"
        ).pack(pady=(60, 10))

        ctk.CTkLabel(
            card,
            text="Inicie sessão para continuar",
            font=("Segoe UI", 16),
            text_color="#6B7280"
        ).pack(pady=(0, 40))

        # ==================================================
        # UTILIZADOR
        # ==================================================
        ctk.CTkLabel(
            card,
            text="Utilizador",
            font=("Segoe UI", 14, "bold"),
            text_color="#081A3C"
        ).pack(anchor="w", padx=65)

        self.utilizador = ctk.CTkEntry(
            card,
            width=450,
            height=52,
            placeholder_text="Introduza o utilizador"
        )
        self.utilizador.pack(pady=(8, 20))

        # ==================================================
        # PASSWORD
        # ==================================================
        ctk.CTkLabel(
            card,
            text="Palavra-passe",
            font=("Segoe UI", 14, "bold"),
            text_color="#081A3C"
        ).pack(anchor="w", padx=65)

        self.senha = ctk.CTkEntry(
            card,
            width=450,
            height=52,
            show="*",
            placeholder_text="Digite a palavra-passe"
        )
        self.senha.pack(pady=(8, 20))

        self.senha.bind("<Return>", lambda e: self._login())

        # ==================================================
        # BOTÃO LOGIN
        # ==================================================
        ctk.CTkButton(
            card,
            text="Entrar",
            width=450,
            height=55,
            font=("Segoe UI", 16, "bold"),
            command=self._login
        ).pack(pady=(20, 10))

        # ==================================================
        # CRIAR CONTA
        # ==================================================
        ctk.CTkLabel(
            card,
            text="Não tem conta?",
            font=("Segoe UI", 14),
            text_color="#6B7280"
        ).pack(pady=(15, 0))

        ctk.CTkButton(
            card,
            text="Criar conta",
            fg_color="transparent",
            hover_color="#E5E7EB",
            text_color="#2563EB",
            font=("Segoe UI", 14, "bold"),
            command=self.on_register
        ).pack(pady=(5, 20))

    # ==================================================
    # LOGIN LOGICA
    # ==================================================
    def _login(self):

        utilizador = self.utilizador.get().strip()
        senha = self.senha.get().strip()

        if not utilizador or not senha:
            messagebox.showwarning(
                "Campos Vazios",
                "Preencha o utilizador e a palavra-passe."
            )
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nome, username, perfil, email, telefone, paciente_id
                FROM utilizadores
                WHERE username = ? AND senha = ?
            """, (utilizador, senha))

            user = cursor.fetchone()
            conn.close()

            if not user:
                messagebox.showerror(
                    "Erro",
                    "Credenciais inválidas."
                )
                return

            id_user, nome, username, perfil, email, telefone, paciente_id = user


            sessao = {
                "id": id_user,
                "nome": nome,
                "username": username,
                "perfil": perfil,
                "email": email,
                "telefone": telefone,
                "paciente_id": paciente_id,
            }

            # Envia a sessão para a aplicação principal
            if self.on_success:
                self.on_success(sessao)

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro",
                f"Erro na base de dados:\n{erro}"
            )