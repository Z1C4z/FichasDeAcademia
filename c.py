import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from screen_exercise import Screen_Record

class ManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento")
        self.geometry("800x500")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True, fill="both")

        self.tabs = {
            "Alunos": ["Nome", "ID"],
            "Equipamentos": ["ID", "Nome", "Quantidade"],
            "Suplementos": ["ID", "Nome", "Quantidade"],
            "Agenda": ["Dia", "Horário", "Descrição"],
            "Treinadores": ["ID", "Nome"],
            "Finanças": ["ID", "Valor", "Descrição"],
        }

        self.populate_tabs()

    def populate_tabs(self):
        for title, fields in self.tabs.items():
            frame = self.create_tab(title)
            tree = self.create_treeview(frame, fields)
            
            add_button = ttk.Button(frame, text="Adicionar", 
                                    command=lambda t=tree, f=fields: self.create_add_popup(t, f))
            add_button.pack(side="left", padx=10, pady=10)
            
            remove_button = ttk.Button(frame, text="Remover", 
                                       command=lambda t=tree: self.remove_item(t))
            remove_button.pack(side="left", padx=10, pady=10)

    def create_tab(self, title):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        return frame

    def create_treeview(self, frame, columns):
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
        
        tree.bind('<Double-1>', lambda event: self.edit_item(tree, columns))
        
        return tree

    def create_add_popup(self, tree, fields):
        popup = tk.Toplevel(self)
        popup.title("Adicionar Item")
        
        entries = []
        for field in fields:
            tk.Label(popup, text=field).pack(pady=5)
            if field in ["Dia", "Horário"]:
                if field == "Dia":
                    entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
                else:
                    entry = tk.Entry(popup)
            else:
                entry = tk.Entry(popup)
            entry.pack(pady=5)
            entries.append(entry)
        
        confirm_button = tk.Button(popup, text="Confirmar", 
                                   command=lambda: [self.add_item(tree, entries), popup.destroy()])
        confirm_button.pack(pady=10)
        
        cancel_button = tk.Button(popup, text="Cancelar", command=popup.destroy)
        cancel_button.pack(pady=5)

    def add_item(self, tree, entries):
        values = [entry.get() for entry in entries]
        tree.insert('', 'end', values=values)
        for entry in entries:
            entry.delete(0, tk.END)

    def remove_item(self, tree):
        selected_item = tree.selection()
        if selected_item:
            tree.delete(selected_item)
        else:
            messagebox.showwarning("Atenção", "Nenhum item selecionado.")

    def edit_item(self, tree, fields):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item, 'values')
            tab_name = self.notebook.tab(self.notebook.select(), "text")
            
            if tab_name == "Alunos":
                self.open_student_edit_screen(aluno=list(values)[1])
            else:
                edit_popup = tk.Toplevel(self)
                edit_popup.title("Editar Item")
                
                entries = []
                for field, value in zip(fields, values):
                    tk.Label(edit_popup, text=field).pack(pady=5)
                    if field in ["Dia", "Horário"]:
                        if field == "Dia":
                            entry = DateEntry(edit_popup, width=12, background='darkblue', foreground='white', borderwidth=2)
                            entry.set_date(value)
                        else:
                            entry = tk.Entry(edit_popup)
                            entry.insert(0, value)
                    else:
                        entry = tk.Entry(edit_popup)
                        entry.insert(0, value)
                    entry.pack(pady=5)
                    entries.append(entry)
                
                def save_changes():
                    new_values = [entry.get() for entry in entries]
                    tree.item(selected_item, values=new_values)
                    edit_popup.destroy()

                tk.Button(edit_popup, text="Salvar", command=save_changes).pack(pady=10)
                tk.Button(edit_popup, text="Cancelar", command=edit_popup.destroy).pack(pady=5)
        else:
            messagebox.showwarning("Atenção", "Nenhum item selecionado.")

    def open_student_edit_screen(self,aluno):
        student_screen = tk.Toplevel(self)
        student_screen.title("Editar Aluno")
        a = Screen_Record(student_screen,client=aluno)
        a.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = ManagementSystem()
    app.mainloop()