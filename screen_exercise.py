import tkinter as tk
from tkinter import ttk
import json
import os

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 2), window=self.scrollable_frame, anchor="nw", width=970)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class Screen_Record(tk.Frame):
    def __init__(self, parent, client):
        super().__init__(parent)
        self.week = {day: {} for day in ['DO', 'SE', 'TE', 'QA', 'QI', 'SX', 'SB']}
        self.rows = [1] * 7
        self.entries_info = {}
        self.arq = self.load_json()
        self.parent = parent
        self.client = client
        if self.client not in self.arq:
            self.arq[self.client] = {"infos": {"name": "", "meta": "", "gender": "", "olds": "", "weight": "",
                                               "height": "", "monthly": ""}, "exercises": {}}
            self.save_json()
        self.create_widgets()
        self.load_existing_data()

    def create_widgets(self):
        self.frame_main = tk.Frame(self, height=720, width=1280)
        self.frame_main.pack(padx=10, pady=10, fill='both', expand=True)
        self.create_info_frame()
        self.create_return_day_frame()

    def create_info_frame(self):
        self.frame_info = tk.Frame(self.frame_main)
        self.frame_info.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        list_infos = self.arq[self.client]["infos"]
        labels = ["Nome", "Objetivo", "Gênero", "Idade", "Peso", "Altura"]
        for i, (key, label) in enumerate(zip(list_infos.keys(), labels)):
            self.create_label_entry(self.frame_info, key, label, list_infos[key], i // 3, i % 3)
        self.create_save_cancel_buttons()
        self.create_monthly_entry()

    def create_label_entry(self, parent, key, text, value, row, column):
        label_frame = tk.LabelFrame(parent, text=text, height=55, width=145)
        label_frame.grid(row=row, column=column, padx=10, pady=5, sticky="w")
        label_frame.grid_propagate(False)
        entry = tk.Entry(label_frame)
        entry.insert(0, value)
        entry.grid(padx=10, pady=5)
        self.entries_info[key] = entry

    def create_save_cancel_buttons(self):
        self.button_save = tk.Button(self.frame_info, text="Sair e Salvar", command=self.save_to_json, width=15, height=6)
        self.button_save.grid(row=0, column=10, padx=11, rowspan=2, pady=5)
        self.button_back = tk.Button(self.frame_info, text="Cancelar", command=self.back_screen, width=15, height=6)
        self.button_back.grid(row=0, column=11, padx=11, rowspan=2, pady=5)

    def create_monthly_entry(self):
        label_frame = tk.LabelFrame(self.frame_info, text="Preço da Mensalidade", width=160, height=55)
        label_frame.grid(row=0, column=5, columnspan=2, padx=10, pady=5)
        label_frame.grid_propagate(False)
        tk.Label(label_frame, text='R$:').grid(row=0, column=0)
        self.monthly = tk.Entry(label_frame, width=20)
        self.monthly.grid(row=0, column=1)

    def create_return_day_frame(self):
        self.frame_return_day = tk.Frame(self.frame_main)
        self.frame_return_day.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', padding=[45, 10])
        self.notebook = ttk.Notebook(self.frame_return_day, width=970, style='TNotebook')
        self.notebook.pack(fill="both", expand=True, padx=0, pady=0)
        days = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
        self.tabs = [self.create_tab(day) for day in days]
        self.create_headers_and_buttons()

    def create_tab(self, day):
        main_frame = tk.Frame(self.notebook)
        scroll = ScrollableFrame(main_frame)
        scroll.pack(fill="both", expand=True)
        self.notebook.add(main_frame, text=day)
        return scroll.scrollable_frame

    def create_headers_and_buttons(self):
        self.headers = ["Nome", "Músculo", "Equipamento", "Séries", "Repetições", "Peso", "Tempo"]
        for index, tab in enumerate(self.tabs):
            for i, header in enumerate(self.headers):
                tk.Label(tab, text=header, width=13).grid(row=0, column=i, padx=10, pady=10)
            tk.Button(tab, text='Adicionar Exercício', width=14, height=2,
                      command=lambda idx=index: self.add_exercise(idx)).grid(row=0, column=len(self.headers), padx=0, pady=0)

    def add_exercise(self, index, values=None):
        lista = [self.create_exercise_entry(self.tabs[index], i, self.rows[index], values) for i in range(len(self.headers))]
        button = tk.Button(self.tabs[index], text='Remover', width=14, height=2, command=lambda: self.remove_exercise(index, self.rows[index]))
        button.grid(row=self.rows[index], column=len(self.headers))
        lista.append(button)
        self.week[self.return_day(index)][self.rows[index]] = lista
        self.rows[index] += 1

    def create_exercise_entry(self, tab, col, row, values):
        entry = tk.Text(tab, width=11, height=2)
        entry.grid(row=row, column=col, padx=1, pady=1)
        if values and col < len(values):
            entry.insert("1.0", values[col])
        return entry

    def remove_exercise(self, index, row):
        lista = self.week[self.return_day(index)].pop(row, None)
        if lista:
            for widget in lista:
                widget.destroy()

    def save_to_json(self, filename='exercises.json'):
        for key, entry in self.entries_info.items():
            self.arq[self.client]["infos"][key] = entry.get()
        data = {day: {str(idx): [widget.get("1.0", "end-1c") for widget in widgets if isinstance(widget, tk.Text)]
                      for idx, widgets in entries.items()}
                for day, entries in self.week.items()}
        self.arq[self.client]["infos"]["monthly"] = self.monthly.get()
        self.arq[self.client]["exercises"] = data
        self.save_json(filename)
        self.back_screen()

    def save_json(self, filename='exercises.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.arq, f, indent=4, ensure_ascii=False)

    def load_existing_data(self):
        exercises = self.arq.get(self.client, {}).get("exercises", {})
        for day, data in exercises.items():
            index = self.return_day_index(day)
            if index is not None:
                for idx, values in data.items():
                    self.add_exercise(index=index, values=values)

    def back_screen(self):
        self.master.destroy()

    def return_day(self, index):
        return ['DO', 'SE', 'TE', 'QA', 'QI', 'SX', 'SB'][index]
    
    def return_day_index(self, day):
        return {'DO': 0, 'SE': 1, 'TE': 2, 'QA': 3, 'QI': 4, 'SX': 5, 'SB': 6}.get(day, None)
    
    def load_json(self, filename="exercises.json"):
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'r') as file:
                return json.load(file)
        return {}