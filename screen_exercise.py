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
        
        canvas.create_window((0,2), window=self.scrollable_frame, anchor="nw",width=970)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class Screen_Record(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('Edição de Fichas')
        self.geometry('1010x600')
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
        
        aux = self.abrir_json()
        list_infos = aux["cliente"]["infos"]
        
        r = 0
        c = 0
        for key, value in list_infos.items():
            if c == 3:
                c = 0
                r += 1

            if key  in ["name","meta","gender","olds","weight","height"]:
                tk.Label(self.frame_info, text=value).grid(row=r, column=c, padx=10, pady=5, sticky="w")
                c += 1

        self.button_save = tk.Button(self.frame_info, text="Salvar",command=lambda: self.save_to_json())
        self.button_save.grid(row=0, column=3, padx=10, pady=5)

        self.monthly = tk.Entry(self.frame_info)
        self.monthly.grid(row=1, column=3, padx=10, pady=5)

        # return_day Frame
        self.frame_return_day = tk.Frame(self.frame_main)
        self.frame_return_day.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', padding=[45, 10])
        
        self.notebook = ttk.Notebook(self.frame_return_day, width=970,style='TNotebook')
        self.notebook.pack(fill="both", expand=True, padx=0, pady=0)

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
                label = tk.Label(self.tabs[index], text=self.headers[i], width=13)
                label.grid(row=0, column=i, padx=10, pady=10)

            button_col = len(self.headers)
            button = tk.Button(self.tabs[index],width=14,height=2, text='Adicionar Exercício', 
                            command=lambda idx=index: self.add_exercise(index=idx))
            button.grid(row=0, column=button_col, padx=0, pady=0)

    def add_exercise(self, index):
        lista = []
        for i in range(len(self.headers)):
            entry = tk.Text(self.tabs[index], width=11,height=2)
            entry.grid(row=self.rows[index], column=i, padx=1, pady=1)
            lista.append(entry)
        button = tk.Button(self.tabs[index], text='Remover',width=14,height=2, command=lambda row=self.rows[index]: self.remove_exercise(index=index, row=row))
        button.grid(row=self.rows[index], column=7)
        lista.append(button)
        
        self.week[self.return_day(index=index)][self.rows[index]] = lista
        self.rows[index] += 1

    def remove_exercise(self, index, row):
        lista = self.week[self.return_day(index=index)].pop(row, None)
        if lista:
            for widget in lista:
                widget.destroy()

    def save_to_json(self, filename='exercises.json'):
        arq = self.abrir_json(filename)  # Assume que `abrir_json` retorna um dicionário válido
        data = {}

        for category, entries in self.week.items():
            if category not in data:
                data[category] = {}

            category_data = data[category]
            for index, widgets in entries.items():
                widgets_data = []
                for widget in widgets:
                    if isinstance(widget, tk.Text):
                        valor = widget.get("1.0", "end-1c")  # Obtém todo o texto do widget Text
                        widgets_data.append(valor)

                category_data[str(index)] = widgets_data

        arq.setdefault("cliente", {})
        arq["cliente"]["exercises"] = data

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(arq, f, indent=4, ensure_ascii=False)


    def return_day(self, index):
        lista = ['DO','SE','TE','QA','QI','SX','SB']
        return lista[index]
    
    def abrir_json(self, filename='exercises.json'):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)


if __name__ == '__main__':
    app = Screen_Record()
    app.mainloop()
