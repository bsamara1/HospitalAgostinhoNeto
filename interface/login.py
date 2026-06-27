import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
from interface.dashboard import Dashboard
from database import conectar


class Login:

    def __init__(self, root):

        self.root = root
        self.root.title("Hospital Agostinho Neto")
        self.root.after(100, lambda: self.root.state("zoomed"))

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root.configure(fg_color="#F5F7FB")

        self.criar_interface()

    def criar_interface(self):

        # ==================================================
        # CONTAINER PRINCIPAL
        # ==================================================
        self.main = ctk.CTkFrame(
            self.root,
            fg_color="#F5F7FB"
        )
        self.main.pack(fill="both", expand=True)

        # ==================================================
        # SIDEBAR
        # ==================================================
        self.sidebar = ctk.CTkFrame(
            self.main,
            width=120,
            fg_color="#081A3C",
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # ==================================================
        # ÁREA ESQUERDA
        # ==================================================
        self.left_area = ctk.CTkFrame(
            self.main,
            fg_color="#F5F7FB"
        )
        self.left_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==================================================
        # LOGO + SIBES
        # ==================================================
        logo_frame = ctk.CTkFrame(
            self.left_area,
            fg_color="transparent"
        )
        logo_frame.place(
            x=90,
            y=130
        )

        try:

            logo = Image.open("assets/logo.png")

            self.logo_img = ctk.CTkImage(
                light_image=logo,
                dark_image=logo,
                size=(180, 180)
            )

            ctk.CTkLabel(
                logo_frame,
                image=self.logo_img,
                text=""
            ).pack(side="left")

        except:
            pass

        ctk.CTkLabel(
            logo_frame,
            text="HAN",
            font=("Segoe UI", 80, "bold"),
            text_color="#081A3C"
        ).pack(side="left", padx=(30, 0))

        # ==================================================
        # SUBTÍTULO
        # ==================================================
        ctk.CTkLabel(
        self.left_area,
        text="Hospital Agostinho Neto\nSistema de Gestão Hospitalar",
        font=("Segoe UI", 25, "normal"),
        text_color="#4B5563",
        justify="center"
        ).place(
            x=230,
             y=300
        )

        # ==================================================
        # IMAGEM PRINCIPAL
        # ==================================================
        try:

            img = Image.open("assets/hospital.png")

            self.main_img = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(720, 350)
            )

            ctk.CTkLabel(
                self.left_area,
                image=self.main_img,
                text=""
            ).place(
                x=0,
                y=480
            )

        except:
            pass

        # ==================================================
        # CARD LOGIN
        # ==================================================
        self.card = ctk.CTkFrame(
            self.main,
            width=580,
            height=760,
            fg_color="white",
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB"
        )

        self.card.place(
            relx=0.74,
            rely=0.5,
            anchor="center"
        )

        self.card.pack_propagate(False)

        # ==================================================
        # TÍTULO
        # ==================================================
        ctk.CTkLabel(
            self.card,
            text="Bem-vindo de volta!",
            font=("Segoe UI", 32, "bold"),
            text_color="#081A3C"
        ).pack(pady=(60, 10))

        ctk.CTkLabel(
            self.card,
            text="Inicie sessão para continuar",
            font=("Segoe UI", 16),
            text_color="#6B7280"
        ).pack(pady=(0, 40))

        # ==================================================
        # EMAIL
        # ==================================================
        ctk.CTkLabel(
            self.card,
            text="Utilizador",
            font=("Segoe UI", 14, "bold"),
            
            text_color="#081A3C"
        ).pack(anchor="w", padx=65)

        self.utilizador = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            placeholder_text="Introduza o utilizador"
        )
        self.utilizador.pack(pady=(8, 20))

        # ==================================================
        # SENHA
        # ==================================================
        ctk.CTkLabel(
            self.card,
            text="Palavra-passe",
            font=("Segoe UI", 14, "bold"),
            text_color="#081A3C"
        ).pack(anchor="w", padx=65)

        self.senha = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            placeholder_text="Digite a sua palavra-passe",
            show="*"
        )
        self.senha.pack(pady=(8, 20))

        # ==================================================
        # BOTÃO LOGIN
        # ==5================================================
        ctk.CTkButton(
            self.card,
            text="Entrar",
            width=450,
            height=55,
            font=("Segoe UI", 16, "bold"),
            command=self.login
        ).pack(pady=(35, 25))

       

        # ==================================================
    # FUNÇÕES
    # ==================================================


    def login(self):

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
                SELECT id, nome, username, perfil
                FROM utilizadores
                WHERE username = ?
                AND senha = ?
            """, (utilizador, senha))

            dados = cursor.fetchone()

            conn.close()

            if dados:


                self.root.destroy()

                dashboard = Dashboard()
                dashboard.mainloop()

            else:

                messagebox.showerror(
                    "Erro",
                    "Utilizador ou palavra-passe inválidos."
                )

        except sqlite3.Error as erro:

         messagebox.showerror(
            "Erro",
            f"Erro na base de dados:\n{erro}"
        )

if __name__ == "__main__":
   
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    

    root = ctk.CTk()

    app = Login(root)

    root.mainloop()