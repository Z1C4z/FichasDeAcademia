import tkinter as tk
from tkinter import ttk
import json

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

        self.week = {'DO':{},'SE':{},'TE':{},'QA':{},'QI':{},'SX':{},'SB':{}}
        self.rows = [1,1,1,1,1,1,1]

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

        self.button_save = tk.Button(self.frame_info, text="Salvar",command=lambda: self.save_to_json())
        self.button_save.grid(row=0, column=3, padx=10, pady=5)

        self.monthly = tk.Entry(self.frame_info)
        self.monthly.grid(row=1, column=3, padx=10, pady=5)

        self.button_math = tk.Button(self.frame_info, text="Calcular")
        self.button_math.grid(row=1, column=4, padx=10, pady=5)

        # return_day Frame
        self.frame_return_day = tk.Frame(self.frame_main)
        self.frame_return_day.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        self.notebook = ttk.Notebook(self.frame_return_day,width=1240)
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

        for index in range(len(self.tabs)):
            for i in range(len(self.headers)):
                label = tk.Label(self.tabs[index], text=self.headers[i], width=10)
                label.grid(row=0, column=i, padx=10, pady=10)

            button_col = len(self.headers)
            button = tk.Button(self.tabs[index], text='Adicionar Exercício', 
                            command=lambda idx=index: self.add_exercise(index=idx))
            button.grid(row=0, column=button_col, padx=10, pady=10)

    def add_exercise(self,index):
        lista = []
        for i in range(len(self.headers)):
            entrys = tk.Entry(self.tabs[index],width=10)
            entrys.grid(row=self.rows[index],column=i,padx=10,pady=10)
            lista.append(entrys)
        button = tk.Button(self.tabs[index],text='Remover',command=lambda:self.remove_exercise(index=index))
        button.grid(row=self.rows[index],column=7)
        lista.append(button)
        
        self.week[self.return_day(index=index)][self.rows[index]] = lista
        print(self.week)
        self.rows[index] += 1

    def remove_exercise(self,index):
        lista = self.week[self.return_day(index=index)]
        for index in list(lista.keys()):
            aux = lista[index]
            for wigth in aux:
                wigth.destroy()

    def save_to_json(self, filename='exercises.json'):
        data = {}

        for category, entries in self.week.items():
            category_data = {}
            for index, widgets in entries.items():
                widgets_data = []
                for widget in widgets:
                    try:
                        if isinstance(widget, tk.Entry):
                            widgets_data.append(widget.get()) 
                    except Exception as e:
                        widgets_data.append(f"Error: {str(e)}")

                category_data[str(index)] = widgets_data

            data[category] = category_data

        # Salvar o dicionário de dados em um arquivo JSON
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def save_button(self,index):
        aux = list(self.week.keys())
        for index in range(len(aux)):
            lista = self.week[aux[index]]
            for widget in lista:
                try:
                    print(widget.get())
                except:
                    pass
    
    def sla(self):
        lista = ['DO','SE','TE','QA','QI','SX','SB']
        for index in range(len(lista)):
            aux = self.week[lista[index]]
            for i in aux:
                try:
                    print(i.get())
                except:
                    pass

    def return_day(self,index):
        lista = ['DO','SE','TE','QA','QI','SX','SB']
        return lista[index]
            
if __name__ == '__main__':
    app = Screen_Record()
    app.mainloop()
