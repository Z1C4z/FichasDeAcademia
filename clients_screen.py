import tkinter as tk
from tkinter import ttk

class Main_Screen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tela Principal')
        self.geometry('1280x720')
        self.screen()

    def screen(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(padx=10, pady=10, expand=True, fill='both')

        self.tabs = []
        for aba in ['Clientes','Equipamentos','Suplementos','Treinadores']:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=aba)
            self.tabs.append(tab)

if __name__ == '__main__':
    sys = Main_Screen()
    sys.mainloop()