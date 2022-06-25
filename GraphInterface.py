import tkinter as tk


class GraphInterface(tk.Toplevel):
    DEFAULT_BUTTON_WIDTH = 20
    DEFAULT_BUTTON_HEIGHT = 2

    def __init__(self, parent: tk.Tk, *, buttonWidth=DEFAULT_BUTTON_WIDTH, buttonHeight=DEFAULT_BUTTON_HEIGHT):
        super().__init__(parent)

        self.buttonWidth = buttonWidth
        self.buttonHeight = buttonHeight

    def createButton(self, text, command):
        tk.Button(self, text=text, command=command, width=self.buttonWidth, height=self.buttonHeight).pack()
