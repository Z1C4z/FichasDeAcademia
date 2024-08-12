import tkinter as tk
from tkinter import ttk, messagebox
import json
import uuid
import os
from tkcalendar import DateEntry
from screen_exercise import Screen_Record

class LoginFrame(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.create_widgets()

    def create_widgets(self):

        tk.Label(self, text="Usuário").pack(pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Senha").pack(pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.check_login).pack(pady=20)
        tk.Button(self, text="Login pelo ID", command=self.id_login).pack(pady=20)

    def check_login(self):
        if os.path.exists("Treinadores.json"):
            with open("Treinadores.json", 'r') as f:
                data = json.load(f)
            for ID in data:
                if self.username_entry.get() == data[ID][0] and self.password_entry.get() == data[ID][1]:
                    self.on_login_success()
                    aux = False
                else:
                    aux = True
            if aux:
                messagebox.showwarning("Login Invalido", "Usuaria e/ou Senha invalido(s).")
        else:
            self.on_login_success()

    def check_id(self):
        entry = self.entry_id.get()

        if os.path.exists("Treinadores.json"):
            with open("Treinadores.json", 'r') as f:
                data = json.load(f)
        else:
            self.popup.destroy()
        
        if entry in data.keys():
            self.popup.destroy()
            self.on_login_success()
        else:
            messagebox.showwarning("Login Invalido", "ID não encontrado")

    def id_login(self):
        self.popup = tk.Toplevel(self)
        self.popup.title(f"Login pelo ID")
        
        tk.Label(self.popup, text="Insira seu ID:").pack(pady=5)
        self.entry_id = tk.Entry(self.popup)
        self.entry_id.pack(pady=5)

        tk.Button(self.popup, text="Confirmar", 
                  command=self.check_id).pack(pady=10)
        
        tk.Button(self.popup, text="Cancelar", command=self.popup.destroy).pack(pady=5)

class ManagementSystem(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True, fill="both")
        self.open = False
        self.tabs = {
            "Alunos": ["Nome"],
            "Equipamentos": ["Nome", "Quantidade"],
            "Suplementos": ["Nome", "Quantidade"],
            "Agenda": ["Dia", "Horário", "Descrição"],
            "Finanças": ["Valor", "Descrição"],
            "Treinadores": ["Nome","Senha"]
        }

        self.data = {tab: {} for tab in self.tabs.keys()}
        self.populate_tabs()
        self.load_from_json()

    def populate_tabs(self):
        for title, fields in self.tabs.items():
            frame = self.create_tab(title)
            tree = self.create_treeview(frame, fields, title)

            self.add_b = ttk.Button(frame, text="Adicionar", 
                       command=lambda t=tree, f=fields, title=title: self.create_add_popup(t, f, title))
            self.add_b.pack(side="left", padx=10, pady=10)
            
            ttk.Button(frame, text="Remover", 
                       command=lambda t=tree, title=title: self.remove_item(t, title)).pack(side="left", padx=10, pady=10)

            ttk.Button(frame, text="Salvar", 
                       command=lambda t=tree, title=title: self.save_to_json(t, title)).pack(side="left", padx=10, pady=10)
            
            ttk.Button(frame, text="Sair e Salvar", command=self.save_and_exit).pack(pady=10,padx=20,side='right')

    def create_tab(self, title):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        return frame

    def create_treeview(self, frame, fields, title):
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=["ID"] + fields, show="headings")
        tree.heading("ID", text="ID")
        for col in fields:
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
        
        tree.bind('<Double-1>', lambda event, t=tree, f=fields, title=title: self.edit_item(t, f, title))
        
        return tree

    def create_add_popup(self, tree, fields, title):
        if not self.open:
            self.open = True
            popup = tk.Toplevel(self)
            popup.title(f"Adicionar {title[:-1]}")
            
            entries = {}
            for field in fields:
                tk.Label(popup, text=field).pack(pady=5)
                entry = DateEntry(popup) if field == "Dia" else tk.Entry(popup)
                entry.pack(pady=5)
                entries[field] = entry

            tk.Button(popup, text="Confirmar", 
                    command=lambda: [self.add_item(tree, entries, title), popup.destroy(), self.add_b.config(state=tk.NORMAL)]).pack(pady=10)
            
            tk.Button(popup, text="Cancelar", command=lambda: self.closePopup(popup)).pack(pady=5)
    def closePopup(self, pop):
        self.open = False
    def generate_unique_id(self, prefix):
        while True:
            unique_id = f"{prefix}{str(uuid.uuid4().int)[:6]}"
            if not any(unique_id in items for items in self.data.values()):
                return unique_id

    def add_item(self, tree, entries, title):
        self.open = False
        prefix = title[0]
        unique_id = self.generate_unique_id(prefix)
        values = [unique_id] + [entry.get() for entry in entries.values()]
        
        if all(values):
            tree.insert('', 'end', values=values)
            self.data[title][unique_id] = values[1:]
        else:
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")

    def remove_item(self, tree, title):
        selected_item = tree.selection()
        if selected_item:
            item_id = tree.item(selected_item, 'values')[0]
            if item_id in self.data[title]:
                del self.data[title][item_id]
            tree.delete(selected_item)
        else:
            messagebox.showwarning("Atenção", "Nenhum item selecionado.")

    def edit_item(self, tree, fields, title):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item, 'values')
            if title == "Alunos":
                self.open_student_edit_screen(aluno=values[0],alu=values[1])
            else:
                edit_popup = tk.Toplevel(self)
                edit_popup.title(f"Editar {title[:-1]}")
                
                entries = {}
                for field, value in zip(fields, values[1:]):
                    tk.Label(edit_popup, text=field).pack(pady=5)
                    entry = DateEntry(edit_popup) if field == "Dia" else tk.Entry(edit_popup)
                    entry.insert(0, value)
                    entry.pack(pady=5)
                    entries[field] = entry
                
                tk.Button(edit_popup, text="Salvar", 
                          command=lambda: [self.save_edited_item(tree, selected_item, entries, title, values[0]), edit_popup.destroy()]).pack(pady=10)
                tk.Button(edit_popup, text="Cancelar", command=edit_popup.destroy).pack(pady=5)
        else:
            messagebox.showwarning("Atenção", "Nenhum item selecionado.")

    def save_edited_item(self, tree, item, entries, title, item_id):
        new_values = [entry.get() for entry in entries.values()]
        if all(new_values):
            tree.item(item, values=[item_id] + new_values)
            self.data[title][item_id] = new_values
        else:
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")

    def open_student_edit_screen(self, aluno,alu):
        student_screen = tk.Toplevel(self)
        student_screen.title(f"Editar {alu} - {aluno}")
        screen = Screen_Record(student_screen, client=aluno)
        screen.pack(fill="both", expand=True)

    def save_to_json(self, tree, tab_name):
        items = tree.get_children()
        for item in items:
            values = tree.item(item, 'values')
            self.data[tab_name][values[0]] = values[1:]
        
        filename = f"jsons/{tab_name.lower()}.json"
        with open(filename, 'w') as f:
            json.dump(self.data[tab_name], f, indent=4)

    def load_from_json(self):
        for tab_name in self.tabs.keys():
            filename = f"jsons/{tab_name.lower()}.json"
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    loaded_data = json.load(f)
                    if isinstance(loaded_data, dict):
                        self.data[tab_name] = loaded_data
                    else:
                        messagebox.showwarning("Erro", f"O arquivo {filename} tem uma estrutura inválida.")
                        continue
                
                tree = self.get_treeview_by_tab_name(tab_name)
                for key, item in self.data[tab_name].items():
                    tree.insert('', 'end', values=[key] + item)

    def get_treeview_by_tab_name(self, tab_name):
        for index in range(self.notebook.index('end')):
            if self.notebook.tab(index, "text") == tab_name:
                return self.notebook.nametowidget(self.notebook.tabs()[index]).winfo_children()[0].winfo_children()[0]

    def save_and_exit(self):
        # Salva todos os itens de todas as abas
        for tab_name in self.tabs.keys():
            tree = self.get_treeview_by_tab_name(tab_name)
            self.save_to_json(tree, tab_name)
        
        # Fecha o programa
        self.master.quit()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento")
        self.geometry("900x600")

        self.login_frame = LoginFrame(self, self.show_management_system)
        self.login_frame.pack(fill="both", expand=True)

    def show_management_system(self):
        self.login_frame.pack_forget()
        self.management_system = ManagementSystem(self)
        self.management_system.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
