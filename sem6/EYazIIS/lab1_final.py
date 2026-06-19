import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import PyPDF2
import spacy
import json
import os

nlp = spacy.load("en_core_web_md")


POS_RU = {
    'NOUN': 'существительное',
    'PROPN': 'имя собственное', 
    'VERB': 'глагол',
    'AUX': 'вспомогательный глагол',
    'ADJ': 'прилагательное',
    'ADV': 'наречие',
    'ADP': 'предлог',
    'DET': 'артикль',
    'CCONJ': 'сочинительный союз',
    'SCONJ': 'подчинительный союз',
    'PART': 'частица',
    'PRON': 'местоимение',
    'INTJ': 'междометие',
    'NUM': 'числительное',
    'SYM': 'символ',
    'PUNCT': 'знак пунктуации',
    'SPACE': 'пробел',
    'X': 'другое'
}

def get_sentence_member(dep, pos):
      # Главные члены предложения
    if dep in ['nsubj', 'nsubjpass']: #nsubj (nominal subject) - именное подлежащее, nsubjpass (nominal subject passive) - подлежащее в пассивном залоге
        return 'подлежащее'
    
    if (dep == 'ROOT' and (pos == 'VERB' or pos == 'AUX')) or dep == 'xcomp' or dep == 'cop': # ROOT - корень предложения (главное слово), xcomp (open clausal complement) - глагольное дополнение, cop (copula) - глагол-связка (обычно "to be")
        return 'сказуемое'
    
    # Второстепенные члены предложения
    if dep in ['dobj', 'iobj', 'obj', 'attr']: # obj (direct object) - прямое дополнение, iobj (indirect object) - косвенное дополнение, obj (object) - общее дополнение, attr (attribute) - атрибут (часто после глагола-связки)
        return 'дополнение'
    
    if dep in ['amod', 'nummod', 'det', 'poss', 'acomp']: # mod (adjectival modifier) - прилагательное-определение, nummod (numeric modifier) - числительное, det (determiner) - артикль/определитель, poss (possession modifier) - притяжательность, acomp (adjectival complement) - прилагательное-дополнение
        return 'определение'
    
    if dep in ['advmod', 'advcl', 'npadvmod', 'pobj']: # advmod (adverbial modifier) - наречие, advcl (adverbial clause) - придаточное обстоятельственное, npadvmod (noun phrase adverbial modifier) - существительное как обстоятельство, pobj (object of preposition) - объект предлога
        return 'обстоятельство'
    
    return '-'


class PDFAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Text Analyzer")
        self.root.geometry("1100x710")
        self.root.configure(bg='#f0f0f0')
        
        self.current_file = None
        self.results = []
        self.filtered_results = []
        
        # Файл для сохранения состояния
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.state_file = os.path.join(script_dir, 'pdf_analyzer_state.json')

        # Стили
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        
        # Автоматическая загрузка предыдущего состояния
        self.root.after(100, self.load_state)
        
        # Сохранение состояния при закрытии
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def setup_ui(self):
        # Главный контейнер
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Верхняя панель управления
        control_frame = tk.Frame(main_frame, bg='#e0e0e0', relief=tk.RAISED, bd=1)
        control_frame.pack(fill=tk.X, pady=(0, 15))

        # Кнопки управления
        btn_style = {'bg': '#4a6fa5', 'fg': 'white', 'font': ('Arial', 10, 'bold'),
                    'relief': tk.RAISED, 'bd': 2, 'padx': 15, 'pady': 8}
        
        tk.Button(control_frame, text="📁 Выбрать PDF", command=self.load_pdf, **btn_style).pack(side=tk.LEFT, padx=5)
        self.analyze_btn = tk.Button(control_frame, text="🔍 Анализировать", command=self.analyze_text, 
                                    state=tk.DISABLED, **btn_style)
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="💾 Сохранить TXT", command=self.save_txt, **btn_style).pack(side=tk.LEFT, padx=5)
        self.add_button = tk.Button(control_frame, text="➕ Добавить", command=self.add_record,state=tk.DISABLED, **btn_style)
        self.add_button.pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="❌ Удалить", command=self.delete_record, bg='#c44d56', fg='white',
                 font=('Arial', 10, 'bold'), relief=tk.RAISED, bd=2, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="📖 Помощь", command=self.show_help, bg='#6c757d', fg='white',
                 font=('Arial', 10, 'bold'), relief=tk.RAISED, bd=2, padx=15, pady=8).pack(side=tk.RIGHT, padx=5)
        
        # Панель фильтрации и поиска
        filter_frame = tk.Frame(main_frame, bg='#e8e8e8', relief=tk.GROOVE, bd=1)
        filter_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(filter_frame, text="🔎 Поиск:", bg='#e8e8e8', font=('Arial', 10)).pack(side=tk.LEFT, padx=(10, 5))
        self.search_entry = tk.Entry(filter_frame, width=25, font=('Arial', 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        search_options = ['Везде', 'По лемме', 'По слову', 'По части речи', 'По роли']
        self.search_type = ttk.Combobox(filter_frame, values=search_options, width=12, state='readonly')
        self.search_type.set('Везде')
        self.search_type.pack(side=tk.LEFT, padx=5)
        
        tk.Button(filter_frame, text="Найти", command=self.search_data, bg='#17a2b8', fg='white',
                 font=('Arial', 9, 'bold'), relief=tk.RAISED, bd=1, padx=10).pack(side=tk.LEFT, padx=5)
        
        tk.Label(filter_frame, text="Фильтр по роли:", bg='#e8e8e8', font=('Arial', 10)).pack(side=tk.LEFT, padx=(20, 5))
        self.filter_role = ttk.Combobox(filter_frame, values=['Все'] + ['подлежащее', 'сказуемое', 'дополнение', 
                                                                       'определение', 'обстоятельство', '-'],
                                       width=15, state='readonly')
        self.filter_role.set('Все')
        self.filter_role.pack(side=tk.LEFT, padx=5)
        self.filter_role.bind('<<ComboboxSelected>>', self.apply_filter)
        
        tk.Button(filter_frame, text="Сбросить", command=self.reset_filters, bg='#6c757d', fg='white',
                 font=('Arial', 9, 'bold'), relief=tk.RAISED, bd=1, padx=10).pack(side=tk.LEFT, padx=5)
        
        # Статистика
        self.stats_label = tk.Label(filter_frame, text="Слов: 0", bg='#e8e8e8', font=('Arial', 10, 'bold'))
        self.stats_label.pack(side=tk.RIGHT, padx=10)
        
        # Таблица результатов
        table_frame = tk.Frame(main_frame, bg='white', relief=tk.SUNKEN, bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('lemma', 'original', 'pos', 'member')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        # Настройка столбцов
        self.tree.heading('lemma', text='ЛЕММА')
        self.tree.heading('original', text='ИСХОДНОЕ СЛОВО')
        self.tree.heading('pos', text='ЧАСТЬ РЕЧИ')
        self.tree.heading('member', text='ЧЛЕН ПРЕДЛОЖЕНИЯ')
        
        self.tree.column('lemma', width=250, anchor='w')
        self.tree.column('original', width=200, anchor='w')
        self.tree.column('pos', width=250, anchor='w')
        self.tree.column('member', width=200, anchor='w')
        
        # Стиль таблицы
        self.style.configure('Treeview', font=('Arial', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Arial', 11, 'bold'), background='#4a6fa5', foreground='white')
        
        # Полосы прокрутки
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scroll_y.grid(row=0, column=1, sticky='ns')
        scroll_x.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Двойной клик для редактирования
        self.tree.bind('<Double-1>', self.edit_record)
        
        # Статус бар
        self.status_bar = tk.Label(self.root, text="Готов к работе...", bd=1, relief=tk.SUNKEN, 
                                  anchor=tk.W, bg='#343a40', fg='white', font=('Arial', 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    

    def save_state(self):
        try:
            state = {
                'current_file': self.current_file,
                'results': self.results,
                'filtered_results': self.filtered_results,
                'filter_role': self.filter_role.get(),
                'search_term': self.search_entry.get(),
                'search_type': self.search_type.get()
            }
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            
            self.status_bar.config(text="Состояние сохранено")
        except Exception as e:
            print(f"Ошибка сохранения состояния: {e}")
    
    
    def load_state(self):
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # Восстановление данных
                self.current_file = state.get('current_file')
                self.results = state.get('results', [])
                self.filtered_results = state.get('filtered_results', [])
                
                # Восстановление фильтров
                filter_role = state.get('filter_role', 'Все')
                search_term = state.get('search_term', '')
                search_type = state.get('search_type', 'Везде')
                
                self.filter_role.set(filter_role)
                self.search_entry.insert(0, search_term)
                self.search_type.set(search_type)
                
                # Заполнение таблицы
                if self.results:
                    for item in self.tree.get_children():
                        self.tree.delete(item)
                    
                    data_to_show = self.filtered_results if self.filtered_results else self.results
                    for result in data_to_show:
                        self.tree.insert('', tk.END, values=tuple(result))
                    
                    self.add_button.config(state=tk.NORMAL)
                    
                    # Если был загружен файл, активируем кнопку анализа
                    if self.current_file:
                        filename = os.path.basename(self.current_file)
                        self.analyze_btn.config(state=tk.NORMAL)
                        self.status_bar.config(text=f"Загружено состояние. Файл: {filename}")
                    else:
                        self.status_bar.config(text=f"Загружено состояние. Всего слов: {len(self.results)}")
                    
                    self.update_stats()
                else:
                    self.status_bar.config(text="Готов к работе...")
                    
        except Exception as e:
            print(f"Ошибка загрузки состояния: {e}")
            self.status_bar.config(text="Ошибка загрузки предыдущего состояния")
    

    def on_closing(self):
        self.save_state()
        self.root.destroy()


    def load_pdf(self):
        filepath = filedialog.askopenfilename(
            title="Выберите PDF файл",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if filepath:
            self.current_file = filepath
            filename = filepath.split('/')[-1]
            self.status_bar.config(text=f"Загружен файл: {filename}")
            self.analyze_btn.config(state=tk.NORMAL)
            messagebox.showinfo("Успех", f"Файл '{filename}' загружен")

            self.save_state()
    

    def analyze_text(self):
        if not self.current_file:
            messagebox.showerror("Ошибка", "Сначала выберите PDF файл")
            return
        
        try:
            with open(self.current_file, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + " "
            
            if not text.strip():
                messagebox.showerror("Ошибка", "Файл не содержит текста")
                return
            
            doc = nlp(text)
            self.results = []
            
            # Очистка таблицы
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Анализ каждого слова
            for token in doc:
                if token.is_punct or token.is_space:
                    continue
                lemma = token.lemma_.lower()
                original = token.text
                pos = POS_RU.get(token.pos_, token.pos_) # pos (part of speech) - часть речи
                member = get_sentence_member(token.dep_, token.pos_) #     dep - синтаксическая роль слова в предложении. Строится через дерево, вероятность и ллм
                
                self.results.append([lemma, original, pos, member])

            
            self.results.sort(key=lambda x: x[0].lower())
            
            # Заполнение таблицы отсортированными данными
            for result in self.results:
                self.tree.insert('', tk.END, values=tuple(result))

            self.filtered_results = self.results.copy()
            self.update_stats()
            self.status_bar.config(text=f"Проанализировано {len(self.results)} слов")
            self.add_button.config(state=tk.NORMAL)
            
            self.save_state()
            
            messagebox.showinfo("Успех", f"Анализ завершен. Найдено {len(self.results)} слов")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
    

    def save_txt(self):
        if not self.results:
            messagebox.showerror("Ошибка", "Нет данных для сохранения")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("="*80 + "\n")
                    f.write("АНАЛИЗ ТЕКСТА ИЗ PDF\n")
                    f.write("="*80 + "\n\n")
                    f.write(f"    ЛЕММА            | ИСХОДНОЕ СЛОВО  |      ЧАСТЬ РЕЧИ        | ЧЛЕН ПРЕДЛОЖЕНИЯ\n")
                    f.write("-"*80 + "\n")
                    for lemma, original, pos, member in self.results:
                        f.write(f"{lemma:<20} | {original:<15} | {pos:<22} | {member}\n")
                    f.write("\n" + "="*80 + "\n")
                    f.write(f"Всего слов: {len(self.results)}\n")
                    f.write("="*80)
                
                filename = filepath.split('/')[-1]
                self.status_bar.config(text=f"Сохранено в {filename}")
                messagebox.showinfo("Успех", "Результат сохранен в TXT")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")
    

    def search_data(self):
        if not self.results:
            messagebox.showerror("Ошибка", "Нет данных для поиска")
            return
        
        search_term = self.search_entry.get().lower()
        if not search_term:
            messagebox.showwarning("Предупреждение", "Введите текст для поиска")
            return
        
        search_type = self.search_type.get()
        
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Поиск по выбранному критерию
        found = 0
        for lemma, original, pos, member in self.results:
            match = False
            
            if search_type == 'Везде':
                match = (search_term in lemma or 
                        search_term in original.lower() or 
                        search_term in pos.lower() or 
                        search_term in member)
            elif search_type == 'По лемме':
                match = search_term in lemma
            elif search_type == 'По слову':
                match = search_term in original.lower()
            elif search_type == 'По части речи':
                match = search_term in pos.lower()
            elif search_type == 'По роли':
                match = search_term in member
            
            if match:
                self.tree.insert('', tk.END, values=(lemma, original, pos, member))
                found += 1
        
        self.status_bar.config(text=f"Найдено {found} записей по запросу '{search_term}'")

        self.save_state()
    

    def apply_filter(self, event=None):
        if not self.results:
            return
        
        role_filter = self.filter_role.get()
        
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if role_filter == 'Все':
            self.filtered_results = self.results.copy()
        else:
            self.filtered_results = [r for r in self.results if r[3] == role_filter]
        
        # Обновление таблицы
        for result in self.filtered_results:
            self.tree.insert('', tk.END, values=tuple(result))
        
        self.update_stats()
        self.status_bar.config(text=f"Отфильтровано: {len(self.filtered_results)} записей")

        self.save_state()
    

    def reset_filters(self):
        if not self.results:
            return
        
        self.filter_role.set('Все')
        self.search_entry.delete(0, tk.END)
        self.filtered_results = self.results.copy()
        
        # Очистка и обновление таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for result in self.results:
            self.tree.insert('', tk.END, values=tuple(result))
        
        self.update_stats()
        self.status_bar.config(text="Фильтры сброшены")

        self.save_state()
    

    def add_record(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить новую запись")
        add_window.geometry("400x300")
        add_window.configure(bg='#f0f0f0')
        add_window.transient(self.root)
        add_window.grab_set()
        
        tk.Label(add_window, text="Лемма:", bg='#f0f0f0', font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        lemma_entry = tk.Entry(add_window, width=30, font=('Arial', 10))
        lemma_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(add_window, text="Исходное слово:", bg='#f0f0f0', font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        original_entry = tk.Entry(add_window, width=30, font=('Arial', 10))
        original_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(add_window, text="Часть речи:", bg='#f0f0f0', font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        pos_combo = ttk.Combobox(add_window, values=list(POS_RU.values()), width=27, state='readonly')
        pos_combo.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(add_window, text="Член предложения:", bg='#f0f0f0', font=('Arial', 10)).grid(row=3, column=0, padx=10, pady=10, sticky='e')
        member_combo = ttk.Combobox(add_window, values=['подлежащее', 'сказуемое', 'дополнение', 
                                                       'определение', 'обстоятельство', '-'], 
                                   width=27, state='readonly')
        member_combo.grid(row=3, column=1, padx=10, pady=10)
        

        def save_record():
            lemma = lemma_entry.get().strip().lower()
            original = original_entry.get().strip()
            pos = pos_combo.get().strip()
            member = member_combo.get().strip()
            
            if not all([lemma, original, pos, member]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            # Добавление в результаты
            self.results.append([lemma, original, pos, member])
            self.filtered_results.append([lemma, original, pos, member])
            
            # Добавление в таблицу
            self.tree.insert('', tk.END, values=(lemma, original, pos, member))
            
            self.update_stats()
            self.status_bar.config(text="Добавлена новая запись")
            
            # Сохраняем состояние после добавления записи
            self.save_state()
            
            add_window.destroy()
        
        btn_frame = tk.Frame(add_window, bg='#f0f0f0')
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Сохранить", command=save_record, bg='#28a745', fg='white',
                 font=('Arial', 10, 'bold'), padx=20, pady=5).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Отмена", command=add_window.destroy, bg='#dc3545', fg='white',
                 font=('Arial', 10, 'bold'), padx=20, pady=5).pack(side=tk.LEFT, padx=10)
    

    def edit_record(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = selected[0]
        column = self.tree.identify_column(event.x)
        col_index = int(column.replace('#', '')) - 1
        
        if col_index < 0 or col_index > 3:
            return
        
        current_value = self.tree.item(item, 'values')[col_index]
        column_names = ['Лемма', 'Исходное слово', 'Часть речи', 'Член предложения']
        
        # Для комбобоксов
        if column_names[col_index] == 'Часть речи':
            new_value = simpledialog.askstring(
                "Редактирование",
                f"Введите новое значение для '{column_names[col_index]}': )",
                initialvalue=current_value
            )
        elif column_names[col_index] == 'Член предложения':
            new_value = simpledialog.askstring(
                "Редактирование",
                f"Введите новое значение для '{column_names[col_index]}':\n(доступно: подлежащее, сказуемое, дополнение, определение, обстоятельство, -)",
                initialvalue=current_value
            )
        else:
            new_value = simpledialog.askstring(
                "Редактирование",
                f"Введите новое значение для '{column_names[col_index]}': ",
                initialvalue=current_value
            )
        
        if new_value is not None and new_value != current_value:
            values = list(self.tree.item(item, 'values'))
            values[col_index] = new_value
            self.tree.item(item, values=values)
            
            # Обновление в списке результатов
            item_index = self.tree.index(item)
            if 0 <= item_index < len(self.results):
                self.results[item_index][col_index] = new_value
            
            self.status_bar.config(text="Запись обновлена")
            
            # Сохраняем состояние после редактирования
            self.save_state()
    

    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите записи для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", f"Удалить {len(selected)} выбранных записей?"):
            # Удаление в обратном порядке
            for item in reversed(selected):
                item_index = self.tree.index(item)
                
                # Удаление из списков
                if 0 <= item_index < len(self.results):
                    del self.results[item_index]
                
                # Удаление из таблицы
                self.tree.delete(item)
            
            self.filtered_results = self.results.copy()
            self.update_stats()
            self.status_bar.config(text=f"Удалено {len(selected)} записей")
            
            # Сохраняем состояние после удаления
            self.save_state()
    

    def update_stats(self):
        total = len(self.results)
        filtered = len(self.filtered_results) if self.filtered_results else total
        self.stats_label.config(text=f"Слов: {filtered}/{total}")
    

    def show_help(self):
        help_text = """
        📖 РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ
        
        1. ВЫБОР ФАЙЛА
           - Нажмите "Выбрать PDF"
           - Выберите PDF файл с английским текстом
        
        2. АНАЛИЗ ТЕКСТА
           - Нажмите "Анализировать"
           - Программа извлечет все слова
           - Для каждого слова определит:
             • Лемму
             • Исходное написание
             • Часть речи
             • Член предложения
        
        3. ПОИСК И ФИЛЬТРАЦИЯ
           🔎 Поиск:
             - Введите текст в поле поиска
             - Выберите область поиска (везде, по лемме и т.д.)
             - Нажмите "Найти"
           
           🎯 Фильтр:
             - Выберите роль из выпадающего списка
             - Таблица отфильтруется автоматически
             - Нажмите "Сбросить" для отмены фильтров
        
        4. РЕДАКТИРОВАНИЕ ДАННЫХ
           ✏️ Редактирование:
             - Двойной клик по ячейке таблицы
             - Введите новое значение
           
           ➕ Добавление:
             - Нажмите "Добавить"
             - Заполните все поля формы
           
           ❌ Удаление:
             - Выберите записи в таблице
             - Нажмите "Удалить"
             - Подтвердите удаление
        
        5. СОХРАНЕНИЕ
           💾 Сохранение:
             - Нажмите "Сохранить TXT"
             - Выберите имя файла
             - Результат сохранится в текстовом формате
        
        ⚠️ Примечание: Программа работает только с английским текстом.
        
        💾 АВТОСОХРАНЕНИЕ:
           - Все изменения автоматически сохраняются
           - При следующем запуске работа продолжится с того же места
           - Файл состояния хранится в домашней папке (.pdf_analyzer_state.json)
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Помощь")
        help_window.geometry("600x500")
        help_window.configure(bg='white')
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, font=('Arial', 10), bg='white', padx=10, pady=10)
        text_widget.insert(1.0, help_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFAnalyzer(root)
    root.mainloop()