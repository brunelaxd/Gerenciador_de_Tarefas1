

import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class TaskFlowGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.tasks = []
        self.current_filter = "all"  
        self.data_file = "tasks_gui.json"
        
        self.setup_window()
        
        self.setup_styles()
        
        self.create_interface()
        
        self.load_tasks()
        
        self.refresh_task_list()
        self.update_statistics()
    
    def setup_window(self):
        self.root.title("TaskFlow - Gerenciador de Tarefas")
        self.root.geometry("600x700")
        self.root.minsize(400, 500)
        
        self.center_window()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
 
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_styles(self):

        self.colors = {
            'primary': '#2196F3',      
            'success': '#4CAF50',      
            'danger': '#F44336',       
            'warning': '#FF9800',      
            'light': '#F5F5F5',       
            'dark': '#212121',         
            'white': '#FFFFFF',        
            'border': '#E0E0E0'        
        }
        
        self.fonts = {
            'title': ('Segoe UI', 12, 'bold'),
            'subtitle': ('Segoe UI', 10, 'bold'),
            'body': ('Segoe UI', 9),
            'small': ('Segoe UI', 8)
        }
        
        self.style = ttk.Style()
        self.style.theme_use('clam')  
        
        self.configure_custom_styles()
    
    def configure_custom_styles(self):

        self.style.configure(
            'Primary.TButton',
            background=self.colors['primary'],
            foreground='white',
            borderwidth=0,
            focuscolor='none'
        )
        
        self.style.configure(
            'Success.TButton',
            background=self.colors['success'],
            foreground='white',
            borderwidth=0,
            focuscolor='none'
        )
        
        self.style.configure(
            'Danger.TButton',
            background=self.colors['danger'],
            foreground='white',
            borderwidth=0,
            focuscolor='none'
        )
        
        self.style.configure(
            'Section.TFrame',
            background=self.colors['white'],
            relief='solid',
            borderwidth=1
        )
    
    def create_interface(self):

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        self.create_header(main_frame)
        self.create_add_task_section(main_frame)
        self.create_filter_section(main_frame)
        self.create_task_list_section(main_frame)
        self.create_statistics_section(main_frame)
    
    def create_header(self, parent):

        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(
            header_frame,
            text="🎯 TaskFlow",
            font=('Segoe UI', 16, 'bold'),
            foreground=self.colors['primary']
        )
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Seu Gerenciador de Tarefas",
            font=self.fonts['body'],
            foreground=self.colors['dark']
        )
        subtitle_label.grid(row=1, column=0)
    
    def create_add_task_section(self, parent):

        section_frame = ttk.LabelFrame(
            parent,
            text="➕ Adicionar Nova Tarefa",
            padding="10"
        )
        section_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        section_frame.columnconfigure(1, weight=1)
        
        ttk.Label(section_frame, text="Título:", font=self.fonts['body']).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 5)
        )
        
        self.title_entry = ttk.Entry(section_frame, font=self.fonts['body'])
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.title_entry.bind('<Return>', lambda e: self.add_task())
        
        self.add_button = ttk.Button(
            section_frame,
            text="Adicionar",
            style='Success.TButton',
            command=self.add_task
        )
        self.add_button.grid(row=0, column=2)
        
        ttk.Label(section_frame, text="Descrição:", font=self.fonts['body']).grid(
            row=1, column=0, sticky=(tk.W, tk.N), padx=(0, 5), pady=(5, 0)
        )
        
        self.description_entry = tk.Text(
            section_frame,
            height=2,
            font=self.fonts['body'],
            wrap=tk.WORD
        )
        self.description_entry.grid(
            row=1, column=1, columnspan=2,
            sticky=(tk.W, tk.E), pady=(5, 0)
        )
    
    def create_filter_section(self, parent):

        section_frame = ttk.LabelFrame(
            parent,
            text="🔍 Filtros",
            padding="10"
        )
        section_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        button_frame = ttk.Frame(section_frame)
        button_frame.grid(row=0, column=0)
        
        self.filter_buttons = {}
        
        self.filter_buttons['all'] = ttk.Button(
            button_frame,
            text="Todas (0)",
            style='Primary.TButton',
            command=lambda: self.set_filter('all')
        )
        self.filter_buttons['all'].grid(row=0, column=0, padx=(0, 5))
        
        self.filter_buttons['pending'] = ttk.Button(
            button_frame,
            text="Pendentes (0)",
            command=lambda: self.set_filter('pending')
        )
        self.filter_buttons['pending'].grid(row=0, column=1, padx=(0, 5))
        
        self.filter_buttons['completed'] = ttk.Button(
            button_frame,
            text="Concluídas (0)",
            command=lambda: self.set_filter('completed')
        )
        self.filter_buttons['completed'].grid(row=0, column=2)
    
    def create_task_list_section(self, parent):

        section_frame = ttk.LabelFrame(
            parent,
            text="📋 Lista de Tarefas",
            padding="10"
        )
        section_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        section_frame.columnconfigure(0, weight=1)
        section_frame.rowconfigure(0, weight=1)
        parent.rowconfigure(3, weight=1)
        
        self.create_scrollable_task_list(section_frame)
    
    def create_scrollable_task_list(self, parent):

        self.task_canvas = tk.Canvas(parent, highlightthickness=0)
        self.task_scrollbar = ttk.Scrollbar(
            parent,
            orient="vertical",
            command=self.task_canvas.yview
        )
        self.task_canvas.configure(yscrollcommand=self.task_scrollbar.set)
        
        self.task_list_frame = ttk.Frame(self.task_canvas)
        self.task_canvas_window = self.task_canvas.create_window(
            (0, 0),
            window=self.task_list_frame,
            anchor="nw"
        )
        
        self.task_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.task_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
        self.task_list_frame.bind(
            "<Configure>",
            lambda e: self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all"))
        )
        
        self.task_canvas.bind(
            "<Configure>",
            self.on_canvas_configure
        )
    
    def on_canvas_configure(self, event):

        canvas_width = event.width
        self.task_canvas.itemconfig(self.task_canvas_window, width=canvas_width)
    
    def create_statistics_section(self, parent):

        section_frame = ttk.LabelFrame(
            parent,
            text="📊 Estatísticas",
            padding="10"
        )
        section_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))
        section_frame.columnconfigure(1, weight=1)
        
        self.stats_label = ttk.Label(
            section_frame,
            text="Total: 0 | Pendentes: 0 | Concluídas: 0",
            font=self.fonts['body']
        )
        self.stats_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Label(section_frame, text="Progresso:", font=self.fonts['body']).grid(
            row=1, column=0, sticky=tk.W, pady=(5, 0)
        )
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            section_frame,
            variable=self.progress_var,
            maximum=100,
            length=200
        )
        self.progress_bar.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=(5, 0))
        
        self.progress_label = ttk.Label(
            section_frame,
            text="0%",
            font=self.fonts['body']
        )
        self.progress_label.grid(row=1, column=2, padx=(5, 0), pady=(5, 0))
    
    def add_task(self):

        title = self.title_entry.get().strip()
        description = self.description_entry.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showwarning(
                "Campo Obrigatório",
                "Por favor, digite um título para a tarefa."
            )
            self.title_entry.focus()
            return
        
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description if description else "",
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        self.tasks.append(task)
        
        self.save_tasks()
        
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete("1.0", tk.END)
        
        self.refresh_task_list()
        self.update_statistics()
        self.update_filter_buttons()
        
        self.title_entry.focus()
        
        self.flash_button(self.add_button, self.colors['success'])
    
    def flash_button(self, button, color):

        original_style = button.cget('style')     
        self.root.after(100, lambda: button.configure(style=original_style))
    
    def set_filter(self, filter_type):

        self.current_filter = filter_type
        self.refresh_task_list()
        self.update_filter_buttons()
    
    def update_filter_buttons(self):

        total = len(self.tasks)
        pending = len([t for t in self.tasks if not t['completed']])
        completed = len([t for t in self.tasks if t['completed']])
        
        self.filter_buttons['all'].configure(text=f"Todas ({total})")
        self.filter_buttons['pending'].configure(text=f"Pendentes ({pending})")
        self.filter_buttons['completed'].configure(text=f"Concluídas ({completed})")
        
        for filter_name, button in self.filter_buttons.items():
            if filter_name == self.current_filter:
                button.configure(style='Primary.TButton')
            else:
                button.configure(style='TButton')
    
    def refresh_task_list(self):

        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        filtered_tasks = self.get_filtered_tasks()
        
        for i, task in enumerate(filtered_tasks):
            self.create_task_widget(task, i)
        
        self.task_list_frame.update_idletasks()
        self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all"))
    
    def get_filtered_tasks(self):

        if self.current_filter == "pending":
            return [t for t in self.tasks if not t['completed']]
        elif self.current_filter == "completed":
            return [t for t in self.tasks if t['completed']]
        else: 
            return self.tasks
    
    def create_task_widget(self, task, index):

        task_frame = ttk.Frame(self.task_list_frame)
        task_frame.grid(row=index, column=0, sticky=(tk.W, tk.E), pady=2)
        task_frame.columnconfigure(1, weight=1)
        
        completed_var = tk.BooleanVar(value=task['completed'])
        checkbox = ttk.Checkbutton(
            task_frame,
            variable=completed_var,
            command=lambda: self.toggle_task_completion(task['id'], completed_var.get())
        )
        checkbox.grid(row=0, column=0, padx=(0, 5))
        
        text_frame = ttk.Frame(task_frame)
        text_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        text_frame.columnconfigure(0, weight=1)
        
        title_font = self.fonts['body']
        if task['completed']:
            title_font = (title_font[0], title_font[1], 'overstrike')
        
        title_label = ttk.Label(
            text_frame,
            text=task['title'],
            font=title_font,
            foreground=self.colors['dark'] if not task['completed'] else self.colors['border']
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        if task['description']:
            desc_label = ttk.Label(
                text_frame,
                text=f"📝 {task['description']}",
                font=self.fonts['small'],
                foreground=self.colors['border']
            )
            desc_label.grid(row=1, column=0, sticky=tk.W)
        
        action_frame = ttk.Frame(task_frame)
        action_frame.grid(row=0, column=2, padx=(5, 0))
        
        edit_button = ttk.Button(
            action_frame,
            text="✏️",
            width=3,
            command=lambda: self.edit_task(task['id'])
        )
        edit_button.grid(row=0, column=0, padx=(0, 2))
        
        delete_button = ttk.Button(
            action_frame,
            text="🗑️",
            width=3,
            style='Danger.TButton',
            command=lambda: self.delete_task(task['id'])
        )
        delete_button.grid(row=0, column=1)
    
    def toggle_task_completion(self, task_id, completed):

        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = completed
                task['completed_at'] = datetime.now().isoformat() if completed else None
                break
        
        self.save_tasks()
        self.refresh_task_list()
        self.update_statistics()
        self.update_filter_buttons()
    
    def edit_task(self, task_id):

        task = next((t for t in self.tasks if t['id'] == task_id), None)
        if not task:
            return
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Tarefa")
        edit_window.geometry("400x300")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        edit_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 150
        edit_window.geometry(f"400x300+{x}+{y}")
        
        main_frame = ttk.Frame(edit_window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        edit_window.columnconfigure(0, weight=1)
        edit_window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        ttk.Label(main_frame, text="Título:", font=self.fonts['body']).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        title_entry = ttk.Entry(main_frame, font=self.fonts['body'])
        title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        title_entry.insert(0, task['title'])
        
        ttk.Label(main_frame, text="Descrição:", font=self.fonts['body']).grid(
            row=1, column=0, sticky=(tk.W, tk.N), pady=(0, 5)
        )
        
        desc_text = tk.Text(main_frame, height=6, font=self.fonts['body'], wrap=tk.WORD)
        desc_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        desc_text.insert("1.0", task['description'])
        
        main_frame.rowconfigure(1, weight=1)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        def save_changes():
            new_title = title_entry.get().strip()
            if not new_title:
                messagebox.showwarning("Campo Obrigatório", "Título não pode estar vazio.")
                return
            
            task['title'] = new_title
            task['description'] = desc_text.get("1.0", tk.END).strip()
            
            self.save_tasks()
            self.refresh_task_list()
            edit_window.destroy()
        
        def cancel_edit():
            edit_window.destroy()
        
        # Botões
        ttk.Button(
            button_frame,
            text="Salvar",
            style='Success.TButton',
            command=save_changes
        ).grid(row=0, column=0, padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=cancel_edit
        ).grid(row=0, column=1)
        
        title_entry.focus()
        title_entry.select_range(0, tk.END)
    
    def delete_task(self, task_id):

        task = next((t for t in self.tasks if t['id'] == task_id), None)
        if not task:
            return
        
        result = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a tarefa '{task['title']}'?\n\nEsta ação não pode ser desfeita.",
            icon='warning'
        )
        
        if result:
            self.tasks = [t for t in self.tasks if t['id'] != task_id]
            
            self.save_tasks()
            self.refresh_task_list()
            self.update_statistics()
            self.update_filter_buttons()
    
    def update_statistics(self):

        total = len(self.tasks)
        completed = len([t for t in self.tasks if t['completed']])
        pending = total - completed
        
        self.stats_label.configure(
            text=f"Total: {total} | Pendentes: {pending} | Concluídas: {completed}"
        )
        
        if total > 0:
            progress = (completed / total) * 100
            self.progress_var.set(progress)
            self.progress_label.configure(text=f"{progress:.0f}%")
        else:
            self.progress_var.set(0)
            self.progress_label.configure(text="0%")
    
    def save_tasks(self):

        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror(
                "Erro ao Salvar",
                f"Não foi possível salvar as tarefas:\n{str(e)}"
            )
    
    def load_tasks(self):
        
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
        except Exception as e: 
            messagebox.showerror(
                "Erro ao Carregar",
                f"Não foi possível carregar as tarefas:\n{str(e)}"
            )
            self.tasks = []
    
    def on_closing(self):

        self.save_tasks()
        self.root.destroy()
    
    def run(self):

        self.title_entry.focus()
        
        self.root.mainloop()


def main():

    try:
        app = TaskFlowGUI()
        app.run()
    except Exception as e:
        import tkinter.messagebox as mb
        mb.showerror(
            "Erro Crítico",
            f"Ocorreu um erro inesperado:\n{str(e)}\n\nO aplicativo será fechado."
        )


if __name__ == "__main__":
    main()

