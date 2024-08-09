import tkinter as tk
from tkinter import ttk
from screen_exercise import Screen_Record

class Main_Screen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tela Principal')
        self.geometry('1280x720')
        self.screen()

    def screen(self):
        # Cria o notebook para as abas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(padx=10, pady=10, expand=True, fill='both')

        # Lista para armazenar as abas
        self.tabs = []
        for aba in ['Clientes', 'Equipamentos', 'Suplementos', 'Treinadores']:
            tab = ttk.Frame(self.notebook)  # Cria um Frame para cada aba
            self.notebook.add(tab, text=aba)  # Adiciona o Frame ao Notebook
            self.tabs.append(tab)  # Armazena a aba na lista

        # Instancia a classe Screen_Record na aba "Clientes"
        sr = Screen_Record(self.tabs[0])

if __name__ == '__main__':
    sys = Main_Screen()  # Cria a janela principal
    sys.mainloop()  # Inicia o loop principal da interface gráfica
