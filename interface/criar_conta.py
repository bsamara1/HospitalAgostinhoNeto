import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
from database.database import conectar


class CriarContaContent:

    def __init__(self, parent, on_back, perfil_definido=None):
        self.parent = parent
        self.on_back = on_back
        self.perfil_definido = perfil_definido  # ✔ CORRETO

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self._build()

    # ==================================================
    # UI
    # ==================================================
    def _build(self):

        self.main = ctk.CTkFrame(self.parent, fg_color="#F5F7FB")
        self.main.pack(fill="both", expand=True)

        sidebar = ctk.CTkFrame(
            self.main,
            width=120,
            fg_color="#081A3C",
            corner_radius=0
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        left_area = ctk.CTkFrame(self.main, fg_color="#F5F7FB")
        left_area.pack(side="left", fill="both", expand=True)

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

        ctk.CTkLabel(
            left_area,
            text="Criar Conta\nSistema Hospitalar",
            font=("Segoe UI", 25),
            text_color="#4B5563",
            justify="center"
        ).place(x=230, y=300)

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

        ctk.CTkLabel(
            card,
            text="Criar Conta",
            font=("Segoe UI", 32, "bold"),
            text_color="#081A3C"
        ).pack(pady=(60, 10))

        ctk.CTkLabel(
            card,
            text="Preencha os dados para registo",
            font=("Segoe UI", 16),
            text_color="#6B7280"
        ).pack(pady=(0, 30))

        self.nome = self._campo(card, "Nome completo")
        self.username = self._campo(card, "Utilizador")
        self.email = self._campo(card, "Email")
        self.telefone = self._campo(card, "Telefone")

        self.senha = self._campo(card, "Palavra-passe", show="*")
        self.confirmar = self._campo(card, "Confirmar palavra-passe", show="*")

        ctk.CTkButton(
            card,
            text="Criar Conta",
            width=450,
            height=55,
            font=("Segoe UI", 16, "bold"),
            command=self.criar_conta
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            card,
            text="Já tem conta?",
            font=("Segoe UI", 14),
            text_color="#6B7280"
        ).pack(pady=(10, 0))

        ctk.CTkButton(
            card,
            text="Fazer login",
            fg_color="transparent",
            hover_color="#E5E7EB",
            text_color="#2563EB",
            font=("Segoe UI", 14, "bold"),
            command=self.on_back
        ).pack(pady=(5, 20))

    # ==================================================
    # CAMPO
    # ==================================================
    def _campo(self, parent, placeholder, show=None):
        entry = ctk.CTkEntry(
            parent,
            width=450,
            height=52,
            placeholder_text=placeholder,
            show=show
        )
        entry.pack(pady=(8, 15))
        return entry

    # ==================================================
    # REGISTO
    # ==================================================
    def criar_conta(self):

        nome = self.nome.get().strip()
        username = self.username.get().strip()
        email = self.email.get().strip()
        telefone = self.telefone.get().strip()
        senha = self.senha.get().strip()
        confirmar = self.confirmar.get().strip()

        if not all([nome, username, email, telefone, senha, confirmar]):
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        if senha != confirmar:
            messagebox.showerror("Erro", "As palavras-passe não coincidem.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            # ✔ PERFIL FIXO OU DEFINIDO PELO ADMIN
            perfil = self.perfil_definido if self.perfil_definido else "paciente"

            cursor.execute("""
                INSERT INTO utilizadores (nome, username, senha, perfil, email, telefone)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nome,
                username,
                senha,
                perfil,
                email,
                telefone
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Username já existe!")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro na base de dados:\n{erro}")