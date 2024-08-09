import tkinter as tk
from tkinter import ttk
from screen_exercise import Screen_Record

class Main_Screen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tela Principal')
        self.geometry('1034x570')
        self.screen()

    def screen(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(padx=10, pady=10, expand=True, fill='both')

        self.tabs = []
        for aba in ['Clientes', 'Equipamentos', 'Suplementos', 'Treinadores']:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=aba)
            self.tabs.append(tab)

        self.leave_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.leave_tab, text='Sair e Salvar')
        self.tabs.append(self.leave_tab)
        
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)
    
    def on_tab_change(self, event):
        selected_tab = self.notebook.select()
        if selected_tab == str(self.leave_tab):
            self.leave()

    def leave(self, event=None):
        self.quit()

if __name__ == '__main__':
    sys = Main_Screen()
    sys.mainloop()