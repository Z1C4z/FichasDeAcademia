import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("System")  # Modos: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

class ScrollableFrame(ctk.CTkFrame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class NotebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notebook in Frame")

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, width=800, height=600, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Notebook (abas)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        # Adiciona abas ao notebook
        self.add_notebook_tabs()

    def add_notebook_tabs(self):
        tab1 = ScrollableFrame(self.notebook, width=780, height=580)
        tab2 = ctk.CTkFrame(self.notebook, width=780, height=580)

        self.notebook.add(tab1, text='Tab 1')
        self.notebook.add(tab2, text='Tab 2')

        # Dicionário de itens para criar labels
        items_dict = {"key1": "Value 1", "key2": "Value 2", "key3": "Value 3", "key4": "Value 4",
                      "key5": "Value 5", "key6": "Value 6", "key7": "Value 7", "key8": "Value 8"}

        # Criação de labels com base nos valores do dicionário
        for key, value in items_dict.items():
            label = ctk.CTkLabel(tab1.scrollable_frame, text=value, font=("Arial", 18))
            label.pack(pady=10, padx=10)

        # Conteúdo da Tab 2
        label2 = ctk.CTkLabel(tab2, text="This is tab 2", font=("Arial", 18))
        label2.pack(pady=20, padx=20)

if __name__ == "__main__":
    root = ctk.CTk()
    app = NotebookApp(root)
    root.mainloop()
