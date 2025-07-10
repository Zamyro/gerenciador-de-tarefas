import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Classe principal do gerenciador de tarefas
class TaskManager:
    # função construtora para inicializar a interface e o banco de dados
    def __init__(self, root):
        
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("700x600")
        self.root.config(bg="#f3f4f6")
        
        self.conn = sqlite3.connect("tasks.db")
        self.criar_tabela()

        self.tasks = []
        self.filtered_tasks = []

        self.style_font = ("Segoe UI", 11)

        # ---------- TÍTULO ----------
        tk.Label(
            root, text="Minhas Tarefas",
            font=("Segoe UI", 20, "bold"),
            bg="#f3f4f6", fg="#1f2937"
        ).pack(pady=15)

        # ---------- CAMPOS EM LINHA ----------
        self.input_frame = tk.Frame(root, bg="#f3f4f6")
        self.input_frame.pack(pady=10)

        self.title_entry = self.create_entry("Título", 20)
        self.desc_entry = self.create_entry("Descrição", 25)
        self.date_entry = self.create_entry("dd/mm/aaaa", 12)

        self.priority_var = tk.StringVar(value="Média")
        self.priority_menu = tk.OptionMenu(self.input_frame, self.priority_var, "Alta", "Média", "Baixa")
        self.priority_menu.config(
            bg="#e5e7eb", fg="#111827", font=self.style_font,
            relief="flat", highlightthickness=1, width=10
        )
        self.priority_menu.grid(row=0, column=3, padx=5)
        
        # Frame de filtros
        self.filter_frame = tk.Frame(root, bg="#f3f4f6")
        self.filter_frame.pack(pady=5)

        # Filtro de status
        self.status_filter = tk.StringVar(value="Todas")
        tk.Label(self.filter_frame, text="Status:", bg="#f3f4f6", font=self.style_font).pack(side=tk.LEFT)
        tk.OptionMenu(self.filter_frame, self.status_filter, "Todas", "Concluídas", "Pendentes", command=lambda _: self.update_list()).pack(side=tk.LEFT, padx=5)

        # Filtro de prioridade
        self.priority_filter = tk.StringVar(value="Todas")
        tk.Label(self.filter_frame, text="Prioridade:", bg="#f3f4f6", font=self.style_font).pack(side=tk.LEFT, padx=(20, 0))
        tk.OptionMenu(self.filter_frame, self.priority_filter, "Todas", "Alta", "Média", "Baixa", command=lambda _: self.update_list()).pack(side=tk.LEFT, padx=5)


        # ---------- BOTÃO ADICIONAR ----------
        self.add_button = tk.Button(
            root, text="Adicionar Tarefa", command=self.add_task,
            bg="#2563eb", fg="white", font=self.style_font,
            relief="flat", padx=12, pady=8, borderwidth=0
        )
        self.add_button.pack(pady=10)
        self.add_button.configure(highlightthickness=0)

        self.round_corners(self.add_button)

        # ---------- LISTA DE TAREFAS ----------
        self.task_listbox = tk.Listbox(
            root, selectmode=tk.SINGLE, width=80, height=15,
            font=("Segoe UI", 10), bg="#ffffff", fg="#111827",
            relief="flat", borderwidth=0, highlightthickness=1, highlightcolor="#d1d5db"
        )
        self.task_listbox.pack(pady=15)

        # ---------- BOTÕES DE AÇÃO ----------
        self.button_frame = tk.Frame(root, bg="#f3f4f6")
        self.button_frame.pack(pady=5)

        self.create_action_button("Concluir", self.complete_task, "#10b981")
        self.create_action_button("Excluir", self.delete_task, "#ef4444")
        self.create_action_button("Detalhes", self.show_details, "#6b7280")
        
        self.carregar_tarefas()

    # Método para criar a tabela de tarefas no banco de dados
    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                data TEXT,
                prioridade TEXT,
                concluida INTEGER
            )
        ''')
        self.conn.commit()

    # Método para carregar tarefas do banco de dados
    def carregar_tarefas(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tarefas")
        rows = cursor.fetchall()

        self.tasks = []
        for row in rows:
            self.tasks.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "due_date": datetime.strptime(row[3], "%Y-%m-%d"),
                "priority": row[4],
                "done": bool(row[5])
            })

        self.update_list()
    
    # Método para criar entradas com placeholders
    def create_entry(self, placeholder, width):
        entry = tk.Entry(self.input_frame, width=width, font=self.style_font, bg="white", fg="gray")
        entry.insert(0, placeholder)
        col = len(self.input_frame.grid_slaves())
        entry.grid(row=0, column=col, padx=5)

        def on_focus_in(event, e=entry, ph=placeholder):
            if e.get() == ph:
                e.delete(0, tk.END)
                e.config(fg="black")

        def on_focus_out(event, e=entry, ph=placeholder):
            if not e.get():
                e.insert(0, ph)
                e.config(fg="gray")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return entry

    # Método para arredondar os cantos dos botões
    def round_corners(self, button):
        button.configure(
            relief="flat",
            highlightbackground="#2563eb",
            bd=0
        )

    # Método para criar botões de ação com estilo
    def create_action_button(self, text, command, color):
        btn = tk.Button(
            self.button_frame, text=text, command=command,
            bg=color, fg="white", font=self.style_font,
            relief="flat", padx=14, pady=6, borderwidth=0
        )
        btn.pack(side=tk.LEFT, padx=10)
        self.round_corners(btn)

    # Método para adicionar uma nova tarefa
    def add_task(self):
        title = self.title_entry.get().strip()
        desc = self.desc_entry.get().strip()
        date_str = self.date_entry.get().strip()
        priority = self.priority_var.get()

        if title == "Título" or not title:
            messagebox.showwarning("Campo obrigatório", "Informe o título da tarefa.")
            return
        
        if desc == "Descrição" or not desc:
            messagebox.showwarning("Campo obrigatório", "Informe a descrição da tarefa.")
            return

        try:
            due_date = datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Data inválida", "Use o formato dd/mm/aaaa.")
            return

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tarefas (titulo, descricao, data, prioridade, concluida)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, desc, due_date.strftime("%Y-%m-%d"), priority, 0))
        self.conn.commit()

        self.clear_inputs()
        self.carregar_tarefas()

    # Método para limpar os campos de entrada
    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, "Título")
        self.title_entry.config(fg="gray")

        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, "Descrição")
        self.desc_entry.config(fg="gray")

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, "dd/mm/aaaa")
        self.date_entry.config(fg="gray")

        self.priority_var.set("Média")

    # Método para atualizar a lista de tarefas
    def update_list(self):
        self.task_listbox.delete(0, tk.END)
        self.filtered_tasks = []

        filter_status = self.status_filter.get()
        filter_priority = self.priority_filter.get()

        query = "SELECT * FROM tarefas WHERE 1=1"
        params = []

        if filter_status == "Concluídas":
            query += " AND concluida = 1"
        elif filter_status == "Pendentes":
            query += " AND concluida = 0"

        if filter_priority != "Todas":
            query += " AND prioridade = ?"
            params.append(filter_priority)

        cursor = self.conn.cursor()
        rows = cursor.execute(query, params).fetchall()

        for row in rows:
            task = {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "due_date": datetime.strptime(row[3], "%Y-%m-%d"),
                "priority": row[4],
                "done": bool(row[5])
            }
            self.filtered_tasks.append(task)

            status = "✔" if task["done"] else " "
            line = f"[{status}] {task['title']} ({task['priority']}) - {task['due_date'].strftime('%d/%m')}"
            self.task_listbox.insert(tk.END, line)

    # Método para concluir uma tarefa
    def complete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            task = self.filtered_tasks[selected[0]]
            task["done"] = not task["done"]
            
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE tarefas SET concluida = ? WHERE id = ?
            ''', (1 if task["done"] else 0, task["id"]))
            self.conn.commit()
            
            self.carregar_tarefas()

    # Método para excluir uma tarefa
    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            task = self.filtered_tasks[selected[0]]

            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM tarefas WHERE id = ?", (task["id"],))
            self.conn.commit()

            self.carregar_tarefas()

    # Método para mostrar detalhes de uma tarefa
    def show_details(self):
        selected = self.task_listbox.curselection()
        if not selected:
            return

        task = self.filtered_tasks[selected[0]]
        index_in_tasks = self.tasks.index(task)

        # Janela popup moderna
        detail_win = tk.Toplevel(self.root)
        detail_win.title("Editar Tarefa")
        detail_win.geometry("480x460")
        detail_win.resizable(False, False)
        detail_win.configure(bg="#f9fafb")

        # ----------- Título -----------
        tk.Label(detail_win, text="Editar Tarefa", font=("Segoe UI", 16, "bold"),
                bg="#f9fafb", fg="#111827").pack(pady=(20, 10))

        # Container
        form_frame = tk.Frame(detail_win, bg="#f9fafb")
        form_frame.pack(padx=25, fill="both")

        def add_label_entry(label_text, default, row):
            tk.Label(form_frame, text=label_text, bg="#f9fafb", anchor="w",
                    font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w", pady=4)
            entry = tk.Entry(form_frame, font=self.style_font, bg="#ffffff", width=35)
            entry.insert(0, default)
            entry.grid(row=row, column=1, padx=5, pady=4, sticky="w")
            return entry

        title_entry = add_label_entry("Título:", task["title"], 0)
        date_entry = add_label_entry("Data:", task["due_date"].strftime("%d/%m/%Y"), 1)

        # ----------- Descrição -----------
        tk.Label(form_frame, text="Descrição:", bg="#f9fafb",
                font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="nw", pady=(8, 4))
        desc_text = tk.Text(form_frame, font=self.style_font, width=35, height=4, bg="#ffffff", wrap="word")
        desc_text.insert("1.0", task["description"])
        desc_text.grid(row=2, column=1, pady=4, sticky="w")

        # ----------- Prioridade -----------
        tk.Label(form_frame, text="Prioridade:", bg="#f9fafb",
                font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky="w", pady=8)
        priority_var = tk.StringVar(value=task["priority"])
        priority_menu = tk.OptionMenu(form_frame, priority_var, "Alta", "Média", "Baixa")
        priority_menu.config(bg="#e5e7eb", font=self.style_font, width=10, relief="flat")
        priority_menu.grid(row=3, column=1, sticky="w", pady=8)

        # ----------- Status -----------
        tk.Label(form_frame, text="Status:", bg="#f9fafb",
                font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w", pady=4)
        status_var = tk.StringVar(value="Concluída" if task["done"] else "Pendente")
        status_menu = tk.OptionMenu(form_frame, status_var, "Concluída", "Pendente")
        status_menu.config(bg="#e5e7eb", font=self.style_font, width=10, relief="flat")
        status_menu.grid(row=4, column=1, sticky="w", pady=4)

        # ----------- Botões -----------
        def salvar():
            title = title_entry.get().strip()
            desc = desc_text.get("1.0", tk.END).strip()
            date_str = date_entry.get().strip()

            if not title:
                messagebox.showwarning("Erro", "O título é obrigatório.")
                return

            try:
                due_date = datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                messagebox.showwarning("Erro", "Data inválida. Use o formato dd/mm/aaaa.")
                return

            task_id = self.tasks[index_in_tasks]["id"]
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE tarefas SET
                    titulo = ?, descricao = ?, data = ?, prioridade = ?, concluida = ?
                WHERE id = ?
            ''', (
                title,
                desc,
                due_date.strftime("%Y-%m-%d"),
                priority_var.get(),
                1 if status_var.get() == "Concluída" else 0,
                task_id
            ))
            self.conn.commit()

            self.update_list()
            detail_win.destroy()

        button_frame = tk.Frame(detail_win, bg="#f9fafb")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Salvar Alterações", command=salvar,
                bg="#10b981", fg="white", font=("Segoe UI", 10, "bold"),
                padx=14, pady=6, relief="flat").pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Cancelar", command=detail_win.destroy,
                bg="#6b7280", fg="white", font=("Segoe UI", 10, "bold"),
                padx=14, pady=6, relief="flat").pack(side=tk.LEFT, padx=10)

# função principal para iniciar o aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
