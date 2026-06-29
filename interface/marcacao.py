import customtkinter as ctk
from interface._base import _topbar_base, _placeholder


class MarcacaoContent:

    def __init__(self, parent):
        _topbar_base(parent, "Marcações")
        _placeholder(parent, "Marcações")
