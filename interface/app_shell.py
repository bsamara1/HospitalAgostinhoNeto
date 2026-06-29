import customtkinter as ctk


class AppShell(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)
        self.title("HAN - Hospital Agostinho Neto")
        self.after(100, lambda: self.state("zoomed"))
        self.show_login()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def show_login(self):
        self._clear()
        self.configure(fg_color="#F5F7FB")
        from interface.login import LoginContent
        LoginContent(self, on_success=self.show_app)

    def show_app(self):
        self._clear()
        self.configure(fg_color="#F4F6FB")
        from interface.main_window import MainContent
        MainContent(self, on_logout=self.show_login)
