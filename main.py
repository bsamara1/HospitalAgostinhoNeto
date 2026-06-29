import customtkinter as ctk
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.database import criar_tabelas, criar_admin
from interface.app_shell import AppShell

criar_tabelas()
criar_admin()

root = ctk.CTk()
root.withdraw()

AppShell(root)

root.mainloop()
