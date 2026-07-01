import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
from database.database import conectar


class CriarContaContent:

    def __init__(self, parent, on_back, on_created=None, perfil_definido=None):
        self.parent = parent
        self.on_back = on_back
        self.on_created = on_created
        self.perfil_definido = perfil_definido

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self._build()

    def _build(self):

        self.main = ctk.CTkFrame(self.parent, fg_color="#F5F7FB")
        self.main.pack(fill="both", expand=True)

        sidebar = ctk.CTkFrame(self.main, width=120, fg_color="#081A3C")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        left_area = ctk.CTkFrame(self.main, fg_color="#F5F7FB")
        left_area.pack(side="left", fill="both", expand=True)

        # LOGO
        logo_frame = ctk.CTkFrame(left_area, fg_color="transparent")
        logo_frame.place(x=90, y=130)

        try:
            logo = Image.open("assets/logo.png")
            self.logo_img = ctk.CTkImage(light_image=logo, dark_image=logo, size=(180, 180))

            ctk.CTkLabel(logo_frame, image=self.logo_img, text="").pack(side="left")

        except:
            pass

        ctk.CTkLabel(
            logo_frame,
            text="HAN",
            font=("Segoe UI", 80, "bold"),
            text_color="#081A3C"
        ).pack(side="left", padx=(30, 0))

        # FORM TITLE
        ctk.CTkLabel(
            left_area,
            text="Criar Conta\nSistema Hospitalar",
            font=("Segoe UI", 25),
            text_color="#4B5563"
        ).place(x=230, y=300)

        # CARD
        card = ctk.CTkFrame(
            self.main,
            width=580,
            height=760,
            fg_color="white",
            corner_radius=20
        )
        card.place(relx=0.74, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text="Criar Conta",
                     font=("Segoe UI", 32, "bold")).pack(pady=(50, 10))

        # CAMPOS
        self.nome = self._campo(card, "Nome completo")
        self.username = self._campo(card, "Utilizador")
        self.email = self._campo(card, "Email")
        self.telefone = self._campo(card, "Telefone")

        self.senha = self._campo(card, "Palavra-passe", show="*")
        self.confirmar = self._campo(card, "Confirmar palavra-passe", show="*")

        # BOTÃO
        ctk.CTkButton(
            card,
            text="Criar Conta",
            width=450,
            height=55,
            command=self.criar_conta
        ).pack(pady=20)

        # VOLTAR
        ctk.CTkButton(
            card,
            text="Já tem conta? Fazer login",
            fg_color="transparent",
            text_color="#2563EB",
            command=self.on_back
        ).pack()

    def _campo(self, parent, placeholder, show=None):
        entry = ctk.CTkEntry(parent, width=450, height=52,
                             placeholder_text=placeholder, show=show)
        entry.pack(pady=10)
        return entry

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

        # 🔥 REGRA IMPORTANTE DO PERFIL
        if self.perfil_definido:
            perfil = self.perfil_definido
        else:
            perfil = "paciente"  # só utilizadores normais

        try:
            conn = conectar()
            cursor = conn.cursor()

            paciente_id = None
            if perfil == "paciente":
                cursor.execute("""
                    INSERT INTO pacientes(nome, sexo, idade, telefone, bi, nascimento, morada, estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (nome, "Não definido", 0, telefone, "", "", "", ""))
                paciente_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO utilizadores
                (nome, username, senha, perfil, email, telefone, paciente_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome, username, senha, perfil, email, telefone, paciente_id))

            utilizador_id = cursor.lastrowid
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")

            sessao = {
                "id": utilizador_id,
                "nome": nome,
                "username": username,
                "perfil": perfil,
                "email": email,
                "telefone": telefone,
                "paciente_id": paciente_id,
            }

            if perfil == "paciente" and self.on_created:
                self.on_created(sessao)
                return

            if self.on_back:
                self.on_back()

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Username já existe!")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", str(e))