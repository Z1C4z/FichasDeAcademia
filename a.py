import tkinter as tk
from tkinter import ttk, messagebox

class GymManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.equipamentos = {
            "Esteira": {"Alunos": ["Carlos Fagundes", "Ana Clara Nogueira"], "Séries": 3, "Repetiçoes": 3},
            "Bicicleta Ergométrica": {"Alunos": ["Pedro Souza", "Maria Eduarda da Silva"], "Séries": 4, "Repetiçoes": 4},
            "Supino": {"Alunos": ["João Paulo Ferreira", "Mariana Fernandes"], "Séries": 4, "Repetiçoes": 15},
            "Agachamento": {"Alunos": ["José Carlos Siloé", "Paula Bárbara Guimarães"], "Séries": 5, "Repetiçoes": 20},
            "Cadeira Abdutora": {"Alunos": ["Kéllen Barbosa", "Jefferson Antunes"], "Séries": 4, "Repetiçoes": 10},
            "Leg Press Horizontal": {"Alunos": ["Thaís Limma", "Matheus de Pádua"], "Séries": 5, "Repetiçoes": 5},
            "Cadeira Extensora": {"Alunos": ["Josué Henrique", "Vítor Bello"], "Séries": 4, "Repetiçoes": 10}
        }

        self.suplementos = {
            "Whey Protein": {"Carlos Fagundes": 2, "Ana Clara Nogueira": 3},
            "Creatina": {"Pedro Souza": 5, "Maria Eduarda da Silva": 4},
            "BCAA": {"João Paulo Ferreira": 6, "Mariana Fernandes": 4},
            "Glutamina": {"José Carlos Siloé": 3, "Paula Bárbara Guimarães": 2},
            "Caseína": {"Kéllen Barbosa": 7, "Jefferson Antunes": 5},
            "Maltodextrina": {"Josué Henrique": 3, "Vítor Bello": 4},
            "L Carnitina": {"Thaís Limma": 5, "Matheus de Pádua": 6}
        }

        self.create_login_screen()

    def create_login_screen(self):
        self.frame_login = tk.Frame(self.root, bg="#dcedc8")
        self.frame_login.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        label_usuario = tk.Label(self.frame_login, text="Tipo de Usuário:", bg="#dcedc8", font=("Arial", 14))
        label_usuario.pack(pady=5)

        self.tipo_usuario = tk.StringVar(value="")
        rb_aluno = tk.Radiobutton(self.frame_login, text="Aluno", variable=self.tipo_usuario, value="aluno", bg="#dcedc8", font=("Arial", 12))
        rb_aluno.pack(pady=5)

        rb_treinador = tk.Radiobutton(self.frame_login, text="Treinador", variable=self.tipo_usuario, value="treinador", bg="#dcedc8", font=("Arial", 12))
        rb_treinador.pack(pady=5)

        label_nome_login = tk.Label(self.frame_login, text="Nome de Login:", bg="#dcedc8", font=("Arial", 14))
        label_nome_login.pack(pady=5)

        self.entrada_usuario = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entrada_usuario.pack(pady=5)

        label_senha_login = tk.Label(self.frame_login, text="Senha:", bg="#dcedc8", font=("Arial", 14))
        label_senha_login.pack(pady=5)

        self.entrada_senha = tk.Entry(self.frame_login, font=("Arial", 12), show="*")
        self.entrada_senha.pack(pady=5)

        botao_entrar = tk.Button(self.frame_login, text="Entrar", command=self.login, bg="#8bc34a", font=("Arial", 14))
        botao_entrar.pack(pady=10)

    def login(self):
        user_type = self.tipo_usuario.get()
        username = self.entrada_usuario.get().strip()
        password = self.entrada_senha.get().strip()

        if username and password:
            if user_type == "aluno" or user_type == "treinador":
                self.open_main_screen(user_type)
            else:
                messagebox.showwarning("Tipo de Usuário", "Por favor, selecione um tipo de usuário válido.")
        else:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos de login.")

    def open_main_screen(self, user_type):
        self.frame_login.destroy()
        self.root.title("Gerenciamento de Equipamentos")

        frame_equipamentos = tk.Frame(self.root, bg="#e0e0e0")
        frame_equipamentos.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        label_equipamentos = tk.Label(frame_equipamentos, text="Equipamentos", bg="#e0e0e0", font=("Arial", 14, "bold"))
        label_equipamentos.pack(pady=5)

        self.lista_equipamentos = tk.Listbox(frame_equipamentos, font=("Arial", 12))
        self.lista_equipamentos.pack(expand=True, fill=tk.BOTH)

        for equipamento in self.equipamentos.keys():
            self.lista_equipamentos.insert(tk.END, equipamento)

        frame_detalhes = tk.Frame(self.root, bg="#f0f0f0")
        frame_detalhes.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        label_detalhes = tk.Label(frame_detalhes, text="Detalhes do Equipamento", bg="#f0f0f0", font=("Arial", 14, "bold"))
        label_detalhes.pack(pady=5)

        self.texto_detalhes = tk.StringVar()
        label_texto_detalhes = tk.Label(frame_detalhes, textvariable=self.texto_detalhes, bg="#f0f0f0", font=("Arial", 12), justify=tk.LEFT)
        label_texto_detalhes.pack(expand=True, fill=tk.BOTH, pady=5)

        botao_suplementos = tk.Button(self.root, text="Gerenciar Suplementos", command=self.abrir_tela_suplementos, bg="#64b5f6", font=("Arial", 12))
        botao_suplementos.pack(pady=10)

        self.lista_equipamentos.bind("<<ListboxSelect>>", self.exibir_detalhes)

    def exibir_detalhes(self, event):
        equipamento_selecionado = self.lista_equipamentos.get(self.lista_equipamentos.curselection())
        detalhes = self.equipamentos[equipamento_selecionado]

        self.texto_detalhes.set(
            f"Equipamento: {equipamento_selecionado}\n"
            f"Alunos: {', '.join(detalhes['Alunos'])}\n"
            f"Séries: {detalhes['Séries']}\n"
            f"Repetições: {detalhes['Repetiçoes']}"
        )

    def abrir_tela_suplementos(self):
        janela_suplementos = tk.Toplevel(self.root)
        janela_suplementos.title("Gerenciamento de Suplementos")

        frame_suplementos = tk.Frame(janela_suplementos, bg="#e0f7fa")
        frame_suplementos.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        label_suplementos = tk.Label(frame_suplementos, text="Suplementos", bg="#e0f7fa", font=("Arial", 14, "bold"))
        label_suplementos.pack(pady=5)

        self.lista_suplementos = tk.Listbox(frame_suplementos, font=("Arial", 12))
        self.lista_suplementos.pack(expand=True, fill=tk.BOTH)

        for suplemento in self.suplementos.keys():
            self.lista_suplementos.insert(tk.END, suplemento)

        frame_detalhes = tk.Frame(janela_suplementos, bg="#f0f4c3")
        frame_detalhes.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        label_alunos = tk.Label(frame_detalhes, text="Alunos e Quantidades", bg="#f0f4c3", font=("Arial", 14, "bold"))
        label_alunos.pack(pady=5)

        self.lista_alunos = tk.Listbox(frame_detalhes, font=("Arial", 12))
        self.lista_alunos.pack(expand=True, fill=tk.BOTH, pady=5)

        frame_gerenciamento = tk.Frame(janela_suplementos, bg="#f0f0f0")
        frame_gerenciamento.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10)

        label_aluno = tk.Label(frame_gerenciamento, text="Aluno:", bg="#f0f0f0", font=("Arial", 12))
        label_aluno.pack(side=tk.LEFT, padx=5)

        self.entrada_aluno = tk.Entry(frame_gerenciamento, font=("Arial", 12))
        self.entrada_aluno.pack(side=tk.LEFT, padx=5)

        label_quantidade = tk.Label(frame_gerenciamento, text="Quantidade:", bg="#f0f0f0", font=("Arial", 12))
        label_quantidade.pack(side=tk.LEFT, padx=5)

        self.entrada_quantidade = tk.Entry(frame_gerenciamento, font=("Arial", 12))
        self.entrada_quantidade.pack(side=tk.LEFT, padx=5)

        botao_adicionar = tk.Button(frame_gerenciamento, text="Adicionar", command=self.adicionar_suplemento, bg="#a5d6a7", font=("Arial", 12))
        botao_adicionar.pack(side=tk.LEFT, padx=5)

        botao_remover = tk.Button(frame_gerenciamento, text="Remover", command=self.remover_suplemento, bg="#ef9a9a", font=("Arial", 12))
        botao_remover.pack(side=tk.LEFT, padx=5)

        self.lista_suplementos.bind("<<ListboxSelect>>", self.exibir_alunos)

    def exibir_alunos(self, event):
        suplemento_selecionado = self.lista_suplementos.get(self.lista_suplementos.curselection())
        alunos = self.suplementos[suplemento_selecionado]

        self.lista_alunos.delete(0, tk.END)
        for aluno, quantidade in alunos.items():
            self.lista_alunos.insert(tk.END, f"{aluno}: {quantidade}")

    def adicionar_suplemento(self):
        suplemento_selecionado = self.lista_suplementos.get(self.lista_suplementos.curselection())
        aluno = self.entrada_aluno.get().strip()
        quantidade = self.entrada_quantidade.get().strip()

        if aluno and quantidade.isdigit():
            quantidade = int(quantidade)
            if suplemento_selecionado in self.suplementos:
                self.suplementos[suplemento_selecionado][aluno] = quantidade
            else:
                self.suplementos[suplemento_selecionado] = {aluno: quantidade}
            self.exibir_alunos(None)
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira um nome de aluno e quantidade válida.")

    def remover_suplemento(self):
        suplemento_selecionado = self.lista_suplementos.get(self.lista_suplementos.curselection())
        aluno = self.entrada_aluno.get().strip()

        if aluno in self.suplementos[suplemento_selecionado]:
            del self.suplementos[suplemento_selecionado][aluno]
            self.exibir_alunos(None)
        else:
            messagebox.showwarning("Remoção Falhou", "Aluno não encontrado para este suplemento.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GymManagementApp(root)
    root.mainloop()
