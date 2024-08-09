import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os

class PersonalTrainerApp:
    def __init__(self, frame, alunos_frame):
        self.frame = frame
        self.alunos_frame = alunos_frame
        self.clients = {}
        self.photo_path = None
        self.json_file = "clientes.json"  # Nome do arquivo JSON
        self.load_clients()  # Carregar os dados ao iniciar
        self.create_clients_tab()
        self.create_alunos_cadastrados_tab()

    def create_clients_tab(self):
        frame = tk.LabelFrame(self.frame, text="Cadastro de Clientes", padx=20, pady=20, bg="light gray")
        frame.pack(fill="both", expand="yes", padx=20, pady=10)

        # Photo upload
        self.photo_frame = tk.Frame(frame, bg="#D3D3D3")
        self.photo_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
        self.photo_frame.grid_columnconfigure(0, weight=1)
        self.photo_label = tk.Label(self.photo_frame, text="Foto do Cliente", font=('Helvetica', 10, 'bold'), bg="light gray")
        self.photo_label.pack(anchor="center")
        self.photo_button = ttk.Button(self.photo_frame, text="Carregar Foto", command=self.load_photo, style="TButton")
        self.photo_button.pack(pady=10, anchor="center")
        self.photo_display = tk.Label(self.photo_frame, bg='light gray')
        self.photo_display.pack(anchor="center")

        # Client form
        self.client_form = {}
        fields = ["Nome Completo", "Idade", "Sexo", "Peso", "Altura", "Data de Início"]
        for idx, field in enumerate(fields):
            label = tk.Label(frame, text=field, font=('Helvetica', 10, 'bold'), bg="#D3D3D3")
            label.grid(row=idx + 1, column=0, padx=10, pady=5, sticky="E")
            if field == "Data de Início":
                entry = DateEntry(frame, width=27, background='blue', foreground='blue', borderwidth=2)
            else:
                entry = ttk.Entry(frame, width=30)
            entry.grid(row=idx + 1, column=1, padx=10, pady=5, sticky="W")
            self.client_form[field] = entry

        # Buttons
        btn_frame = tk.Frame(frame, bg="black")
        btn_frame.grid(row=len(fields) + 2, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Adicionar", command=self.add_client, style="TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Atualizar", command=self.update_client, style="TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_client, style="TButton").pack(side="left", padx=5)

    def load_photo(self):
        self.photo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if self.photo_path:
            image = Image.open(self.photo_path)
            image = image.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.photo_display.config(image=photo)
            self.photo_display.image = photo

    def add_client(self):
        data = {field: self.client_form[field].get() for field in self.client_form}
        if not all(data.values()):
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        # Validate Age, Weight, and Height
        try:
            data["Idade"] = int(data["Idade"])
            data["Peso"] = float(data["Peso"])
            data["Altura"] = float(data["Altura"])
        except ValueError:
            messagebox.showwarning("Aviso", "Idade, Peso e Altura devem ser números válidos!")
            return

        client_id = len(self.clients) + 1
        self.clients[client_id] = {**data, "Foto": self.photo_path}
        self.clear_form(self.client_form)

        # Salvar os dados no JSON
        self.save_clients()

        # Atualizar a exibição na Treeview
        self.update_alunos_cadastrados()

    def update_client(self):
        selected_item = self.alunos_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Nenhum cliente selecionado!")
            return

        client_id = int(selected_item[0])
        data = {field: self.client_form[field].get() for field in self.client_form}
        if not all(data.values()):
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        # Validate Age, Weight, and Height
        try:
            data["Idade"] = int(data["Idade"])
            data["Peso"] = float(data["Peso"])
            data["Altura"] = float(data["Altura"])
        except ValueError:
            messagebox.showwarning("Aviso", "Idade, Peso e Altura devem ser números válidos!")
            return

        self.clients[client_id] = {**data, "Foto": self.photo_path}
        self.clear_form(self.client_form)

        # Salvar os dados no JSON
        self.save_clients()

        # Atualizar a exibição na Treeview
        self.update_alunos_cadastrados()

    def delete_client(self):
        selected_item = self.alunos_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Nenhum cliente selecionado!")
            return

        client_id = int(selected_item[0])
        del self.clients[client_id]

        # Salvar os dados no JSON
        self.save_clients()

        # Atualizar a exibição na Treeview
        self.update_alunos_cadastrados()

    def clear_form(self, form):
        for field in form:
            form[field].delete(0, tk.END)
        self.photo_display.config(image='')
        self.photo_display.image = None
        self.photo_path = None

    def save_clients(self):
        """Salva os clientes no arquivo JSON."""
        with open(self.json_file, 'w') as file:
            json.dump(self.clients, file, indent=4)

    def load_clients(self):
        """Carrega os clientes do arquivo JSON, se existir."""
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as file:
                self.clients = json.load(file)

    def create_alunos_cadastrados_tab(self):
        self.alunos_tree = ttk.Treeview(self.alunos_frame, columns=("Nome", "Idade", "Sexo", "Peso", "Altura", "Data de Início"), show="headings")
        self.alunos_tree.heading("Nome", text="Nome Completo")
        self.alunos_tree.heading("Idade", text="Idade")
        self.alunos_tree.heading("Sexo", text="Sexo")
        self.alunos_tree.heading("Peso", text="Peso")
        self.alunos_tree.heading("Altura", text="Altura")
        self.alunos_tree.heading("Data de Início", text="Data de Início")
        self.alunos_tree.pack(fill=tk.BOTH, expand=True)
        self.update_alunos_cadastrados()

    def update_alunos_cadastrados(self):
        # Limpar a Treeview
        for item in self.alunos_tree.get_children():
            self.alunos_tree.delete(item)

        # Adicionar os dados na Treeview
        for client_id, data in self.clients.items():
            self.alunos_tree.insert("", "end", iid=client_id, values=(data["Nome Completo"], data["Idade"], data["Sexo"], data["Peso"], data["Altura"], data["Data de Início"]))

class FinanceTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Finanças")
        
        self.json_file = "payments.json"  # Nome do arquivo JSON para pagamentos
        self.payments = []
        self.load_payments()

        # Interface básica de finanças
        ttk.Label(self.frame, text="Registro de Pagamento").pack(pady=10)
        
        self.payment_date = DateEntry(self.frame)
        self.payment_date.pack(pady=5)
        self.payment_amount = ttk.Entry(self.frame, width=30)
        self.payment_amount.pack(pady=5)
        self.payment_client = ttk.Entry(self.frame, width=30)
        self.payment_client.pack(pady=5)
        
        ttk.Button(self.frame, text="Registrar Pagamento", command=self.add_payment).pack(pady=10)

        self.payment_list = tk.Listbox(self.frame, height=10)
        self.payment_list.pack(pady=10, fill=tk.BOTH, expand=True)
        self.display_payments()

    def add_payment(self):
        payment = {
            "Data": self.payment_date.get(),
            "Valor": self.payment_amount.get(),
            "Cliente": self.payment_client.get()
        }

        if not all(payment.values()):
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        try:
            payment["Valor"] = float(payment["Valor"])
        except ValueError:
            messagebox.showwarning("Aviso", "O valor do pagamento deve ser um número!")
            return

        self.payments.append(payment)
        self.save_payments()
        self.display_payments()

    def display_payments(self):
        self.payment_list.delete(0, tk.END)
        for payment in self.payments:
            self.payment_list.insert(tk.END, f"{payment['Data']} - {payment['Cliente']} - R${payment['Valor']:.2f}")

    def save_payments(self):
        """Salva os pagamentos no arquivo JSON."""
        with open(self.json_file, 'w') as file:
            json.dump(self.payments, file, indent=4)

    def load_payments(self):
        """Carrega os pagamentos do arquivo JSON, se existir."""
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as file:
                self.payments = json.load(file)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestão")
        self.geometry("800x600")
        self.configure(bg="black")

        # Criando Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True)

        # Criando Frames para cada aba
        self.frame_agenda = ttk.Frame(self.notebook, width=780, height=580)
        self.frame_alunos = ttk.Frame(self.notebook, width=780, height=580)
        self.frame_equipamentos = ttk.Frame(self.notebook, width=780, height=580)
        self.frame_suplentes = ttk.Frame(self.notebook, width=780, height=580)
        self.frame_aluno= ttk.Frame(self.notebook, width=780, height=580)
        self.frame_agenda.pack(fill='both', expand=True)
        self.frame_alunos.pack(fill='both', expand=True)
        self.frame_equipamentos.pack(fill='both', expand=True)
        self.frame_suplentes.pack(fill='both', expand=True)

        # Adicionando frames no notebook
        self.notebook.add(self.frame_agenda, text='Agenda')
        self.notebook.add(self.frame_alunos, text='Alunos')
        self.notebook.add(self.frame_equipamentos, text='Equipamentos')
        self.notebook.add(self.frame_suplentes, text='Suplentes')
        self.notebook.add(self.frame_aluno, text='Alunos Cadastrados')
        # Componentes das abas
        self.create_agenda_tab()
        self.create_alunos_tab()
        self.create_equipamentos_tab()
        self.create_suplentes_tab()

        # Adicionando a aba de Finanças
        self.create_finance_tab()

        # Estilo dos botões
        style = ttk.Style()
        style.configure("TButton", background="black", foreground="black")

    def create_agenda_tab(self):
        days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
        times = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
        self.agenda = {day: {time: "" for time in times} for day in days}

        agenda_canvas = tk.Canvas(self.frame_agenda, bg="light gray")
        agenda_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.frame_agenda, orient="vertical", command=agenda_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        agenda_canvas.configure(yscrollcommand=scrollbar.set)
        agenda_canvas.bind('<Configure>', lambda e: agenda_canvas.configure(scrollregion=agenda_canvas.bbox('all')))

        agenda_frame = tk.Frame(agenda_canvas)
        agenda_canvas.create_window((0, 0), window=agenda_frame, anchor='nw')

        for day in days:
            day_frame = tk.LabelFrame(agenda_frame, text=day, background="light gray")
            day_frame.pack(fill="both", expand="yes", padx=10, pady=5)
            for time in times:
                time_frame = tk.Frame(day_frame, background="black")
                time_frame.pack(fill="both", expand="yes", padx=10, pady=5)
                time_label = tk.Label(time_frame, text=time, background="light gray")
                time_label.pack(side=tk.LEFT)
                person_var = tk.StringVar()
                person_var.set("")
                person_entry = ttk.Combobox(time_frame, textvariable=person_var)
                person_entry.pack(side=tk.LEFT, padx=5)
                add_button = ttk.Button(time_frame, text="Adicionar",
                                        command=lambda d=day, t=time, v=person_var: self.add_to_agenda(d, t, v))
                add_button.pack(side=tk.LEFT, padx=5)
                remove_button = ttk.Button(time_frame, text="Remover",
                                            command=lambda d=day, t=time, v=person_var: self.remove_from_agenda(d, t, v))
                remove_button.pack(side=tk.LEFT, padx=5)

    def add_to_agenda(self, day, time, person_var):
        person = person_var.get()
        if person:
            self.agenda[day][time] = person
            person_var.set(person)
        else:
            messagebox.showwarning("Aviso", "Selecione uma pessoa para adicionar.")

    def remove_from_agenda(self, day, time, person_var):
        self.agenda[day][time] = ""
        person_var.set("")

    def create_alunos_tab(self):
        PersonalTrainerApp(self.frame_alunos, self.frame_aluno)

    def create_equipamentos_tab(self):
        pass

    def create_suplentes_tab(self):  
        pass

    def create_finance_tab(self):
        FinanceTab(self.notebook)
    def save_registration(self, window):
        # Lógica para salvar registro
        messagebox.showinfo("Salvo", "Registro salvo com sucesso!")
        window.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
 