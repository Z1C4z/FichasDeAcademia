import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
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

class Screen_Record(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('Edição de Fichas')
        self.geometry('1280x720')
        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        self.frame_main = tk.Frame(self, height=720, width=1280)
        self.frame_main.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Info Frame
        self.frame_info = tk.Frame(self.frame_main)
        self.frame_info.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        
        self.create_info_labels()

        self.button_save = tk.Button(self.frame_info, text="Salvar", command=self.save_info)
        self.button_save.grid(row=0, column=3, padx=10, pady=5)

        self.monthly = tk.Entry(self.frame_info)
        self.monthly.grid(row=1, column=3, padx=10, pady=5)

        self.button_math = tk.Button(self.frame_info, text="Calcular", command=self.calculate)
        self.button_math.grid(row=1, column=4, padx=10, pady=5)

        # Week Frame
        self.frame_week = tk.Frame(self.frame_main)
        self.frame_week.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        self.notebook = ttk.Notebook(self.frame_week)
        self.notebook.pack(fill="both", expand=True)

        self.create_tabs()

    def create_info_labels(self):
        # Hard-coded info labels
        labels = [
            "Nome: Andre Luis", 
            'Objetivo: Hipertrofia', 
            'Gênero: Masculino', 
            'Idade: 16', 
            'Peso: 47kg', 
            'Altura: 1.68m'
        ]
        
        for i, text in enumerate(labels):
            row = i // 3
            col = i % 3
            tk.Label(self.frame_info, text=text).grid(row=row, column=col, padx=10, pady=5, sticky="w")

    def create_tabs(self):
        days = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]

        self.tabs = []

        for i, day in enumerate(days):
            main_frame = tk.Frame(self.notebook)
            scroll = ScrollableFrame(main_frame)
            scroll.pack(fill="both", expand=True)

            self.notebook.add(main_frame, text=day)
            self.tabs.append(scroll.scrollable_frame)

            # Hard-coded example row with headers
            self.create_exercise_row(scroll.scrollable_frame)

    def create_exercise_row(self, parent_frame):
        # Header row
        tk.Label(parent_frame, text="Nome", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(parent_frame, text="Músculo", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(parent_frame, text="Equipamento", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        tk.Label(parent_frame, text="Séries", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)
        tk.Label(parent_frame, text="Repetições", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5, pady=5)
        tk.Label(parent_frame, text="Peso", font=("Arial", 10, "bold")).grid(row=0, column=5, padx=5, pady=5)
        tk.Label(parent_frame, text="Tempo", font=("Arial", 10, "bold")).grid(row=0, column=6, padx=5, pady=5)

        # Example entry row
        tk.Entry(parent_frame, width=15).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(parent_frame, width=15).grid(row=1, column=1, padx=5, pady=5)
        tk.Entry(parent_frame, width=15).grid(row=1, column=2, padx=5, pady=5)
        tk.Entry(parent_frame, width=15).grid(row=1, column=3, padx=5, pady=5)
        tk.Entry(parent_frame, width=15).grid(row=1, column=4, padx=5, pady=5)
        tk.Entry(parent_frame, width=15).grid(row=1, column=5, padx=5, pady=5)
        tk.Entry(parent_frame, width=15).grid(row=1, column=6, padx=5, pady=5)

        # Buttons for adding/removing exercises
        button_frame = tk.Frame(parent_frame)
        button_frame.grid(row=2, column=0, columnspan=7, pady=10)
        tk.Button(button_frame, text='REMOVER', command=lambda: self.remove_exercise(parent_frame)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Adicionar Exercício", command=lambda: self.create_exercise_row(parent_frame)).pack(side="left", padx=5)

    def add_exercise_row(self, parent_frame):
        row = parent_frame.grid_size()[1]
        headers = ["Nome", "Músculo", "Equipamento", "Séries", "Repetições", "Peso", "Tempo"]

        for i, header in enumerate(headers):
            tk.Entry(parent_frame, width=15).grid(row=row, column=i, padx=5, pady=5)

    def remove_exercise(self, parent_frame):
        children = parent_frame.grid_slaves()
        if children:
            for widget in children:
                if widget.grid_info()["row"] > 1:  # Remove rows except header
                    widget.destroy()

if __name__ == '__main__':
    app = Screen_Record()
    app.mainloop()