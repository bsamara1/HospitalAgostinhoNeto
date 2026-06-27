import customtkinter as ctk
from database import criar_tabelas,criar_admin
from interface.login import Login

criar_tabelas()
criar_admin()

root = ctk.CTk()

Login(root)

root.mainloop()