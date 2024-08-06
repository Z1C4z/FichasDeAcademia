import tkinter as tk
from tkinter import ttk

class Screen_Record(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Edição de Fichas')
        self.geometry('1280x720')
        self.screen()

    def screen(self):
        self.frame_main = tk.Frame(self, height=720, width=1280)
        self.frame_main.pack(padx=10, pady=10,fill='both', expand=True)

        self.frame_info = tk.Frame(self.frame_main, height=180, width=1240)
        self.frame_info.grid(row=0, column=0, pady=10, padx=10)

        list_infos = {
            "name": f"Nome: {'Andre Luis'}",
            "meta": f'Objetivo: {'Hipertrofia'}',
            "gender": f'Genero: {'Masculino'}',
            "olds": f'Idade: {16}',
            "weight": f'Peso: {47}kg',
            "heigth": f'Altura: {1.68}m'
                      }
        
        r = 0; c = 0
        for key, value in list_infos.items():
            if c == 3: c = 0; r =1

            label_name = tk.Label(self.frame_info, text=value)
            label_name.grid(row=r, column=c, padx=10, pady=5)
            c += 1

        self.button_save = tk.Button(self.frame_info, text="Salvar")
        self.button_save.grid(row=0, column=3, padx=10, pady=5)

        self.mouthly = tk.Entry(self.frame_info)
        self.mouthly.grid(row=1,column=3)

        self.button_math = tk.Button(self.frame_info, text="Calcular")
        self.button_math.grid(row=1, column=4, padx=10, pady=5)

        self.frame_week = tk.Frame(self.frame_main, height=180, width=1240)
        self.frame_week.grid(row=1, column=0, pady=10, padx=10)
        
        self.notebook = ttk.Notebook(self.frame_week,height=260,width=1240)
        self.notebook.pack(fill="both", expand=True)

        self.tabs = []
        days = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
        for day in days:
            tab = tk.ScrollableFrame(self.notebook, width=780, height=580)
            self.notebook.add(tab, text=days[day])
            self.tabs.append(tab)

        for a in range(len(self.tabs)): 

            list_frame = tk.Frame(self.tabs[a], height=180, width=1240)
            list_frame.grid(row=2, column=0, pady=10, padx=10)
            headers = ["Nome", "Músculo", "Equipamento", "Séries", "Repetições", "Peso", "Tempo"]

            for i, header in enumerate(headers):
                
                entry = tk.Entry(list_frame, placeholder_text=header, width=100)
                entry.grid(row=0, column=i, padx=5, pady=5)
                
                button_remove = tk.Button(list_frame,text='REMOVER')
                button_remove.grid(row=0, column=10, padx=5, pady=5)

                button_add_exercise = tk.Button(self.tabs[a], text="Adicionar Exercício")
                button_add_exercise.grid(row=3, column=0, pady=10)
            
            scrollbar = tk.Scrollbar(self.tabs[a])
            scrollbar.grid(row=0, column=1, sticky="ns")

class ScrollableFrame(tk.Frame):
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
                    
if __name__ == '__main__':
    sys = Screen_Record()
    sys.mainloop()