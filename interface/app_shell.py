import customtkinter as ctk


class AppShell(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("HAN")
        self.geometry("1280x820")
        self.minsize(900, 600)
        self.deiconify()
        self.lift()
        self.focus_force()
        self.update_idletasks()
        self.attributes("-topmost", True)
        self.after(500, lambda: self.attributes("-topmost", False))
        self.after(100, lambda: self.state("zoomed"))

        self.configure(fg_color="#F5F7FB")

        # 🔥 container fixo
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.show_login()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        from interface.login import LoginContent
        LoginContent(self.container, self.show_app, self.show_register)

    def show_app(self, sessao):
        self.clear()
        from interface.main_window import MainContent
        MainContent(self.container, self.show_login, sessao)

    def show_register(self):
        self.clear()
        from interface.criar_conta import CriarContaContent
        CriarContaContent(self.container, self.show_login, self.show_app)