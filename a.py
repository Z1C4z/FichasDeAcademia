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

        self.dicta = {}
        self.lista = []

    def create_widgets(self):
        # Main Frame
        self.frame_main = tk.Frame(self, height=720, width=1280)
        self.frame_main.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Info Frame
        self.frame_info = tk.Frame(self.frame_main)
        self.frame_info.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        
        list_infos = {
            "name": "Nome: Andre Luis",
            "meta": 'Objetivo: Hipertrofia',
            "gender": 'Gênero: Masculino',
            "olds": 'Idade: 16',
            "weight": 'Peso: 47kg',
            "height": 'Altura: 1.68m'
        }
        
        r = 0
        c = 0
        for key, value in list_infos.items():
            if c == 3:
                c = 0
                r += 1
            tk.Label(self.frame_info, text=value).grid(row=r, column=c, padx=10, pady=5, sticky="w")
            c += 1

        self.button_save = tk.Button(self.frame_info, text="Salvar")
        self.button_save.grid(row=0, column=3, padx=10, pady=5)

        self.monthly = tk.Entry(self.frame_info)
        self.monthly.grid(row=1, column=3, padx=10, pady=5)

        self.button_math = tk.Button(self.frame_info, text="Calcular")
        self.button_math.grid(row=1, column=4, padx=10, pady=5)

        # Week Frame
        self.frame_week = tk.Frame(self.frame_main)
        self.frame_week.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        self.notebook = ttk.Notebook(self.frame_week,width=1240)
        self.notebook.pack(fill="both", expand=True)

        self.tabs = []
        days = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]

        for day in days:
            main_frame = tk.Frame(self.notebook)
            scroll = ScrollableFrame(main_frame)
            scroll.pack(fill="both", expand=True)

            self.notebook.add(main_frame, text=day)
            self.tabs.append(scroll.scrollable_frame)
        
        
        self.headers = ["Nome", "Músculo", "Equipamento", "Séries", "Repetições", "Peso", "Tempo"]
        self.rows = [1,1,1,1,1,1,1]

        for i in range(len(self.headers)):
          label = tk.Label(self.tabs[0],text=self.headers[i],width=10).grid(row=0,column=i,padx=10,pady=10)
          button = tk.Button(self.tabs[0],text='Adiconar Exercicio',command=lambda: self.add_exercise(0)).grid(row=0,column=7)

    def add_exercise(self,index):
        for i in range(len(self.headers)):
            entry = tk.Entry(self.tabs[index],width=10).grid(row=self.rows[index],column=i,padx=10,pady=10)
            self.dicta[self.rows[index]] = self.lista
            tk.Button(self.tabs[0],text='Remover',command=lambda:self.remove_exercise(self.rows[index])).grid(row=self.rows[index],column=7)
        self.rows[index] += 1

    def remove_exercise(self,index):
        print(self.dicta)
            

if __name__ == '__main__':
    app = Screen_Record()
    app.mainloop()
