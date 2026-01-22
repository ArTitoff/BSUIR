from tkinter import *
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import re


class UserPaginationApp:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("База клиентов")
        self.root.geometry("1400x600")

        self.page_size = 10 
        self.current_page = 0

        self.tree_frame = Frame(self.root)
        self.tree_frame.pack(side=TOP, fill=BOTH, expand=True)  

        self.columns = ("name", "surname", "otchestvo", "account_num", "address", "mob_telephone", "home_telephone")
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=True)

        self.tree.heading("name", text="Имя")
        self.tree.heading("surname", text="Фамилия")
        self.tree.heading("otchestvo", text="Отчество")
        self.tree.heading("account_num", text="Номер счета")
        self.tree.heading("address", text="Адрес")
        self.tree.heading("mob_telephone", text="Мобильный телефон")
        self.tree.heading("home_telephone", text="Домашний телефон")

        self.hierarchical_tree = ttk.Treeview(self.tree_frame, show="tree")
        self.hierarchical_tree.pack(fill=BOTH, expand=True)
        self.hierarchical_tree.pack_forget() 

        self.show_hierarchical_var = BooleanVar()
        self.show_hierarchical_checkbutton = Checkbutton(
            self.root, text="Показать иерархическое дерево", variable=self.show_hierarchical_var, command=self.toggle_view
        )
        self.show_hierarchical_checkbutton.pack(anchor=W, padx=10, pady=5)

        # Кнопки навигации
        button_frame = Frame(self.root)
        button_frame.pack(fill=X)

        self.first_button = Button(button_frame, text="Первая страница", command=self.first_page)
        self.first_button.pack(side=LEFT)

        self.previous_button = Button(button_frame, text="Предыдущая", command=self.previous_page)
        self.previous_button.pack(side=LEFT)

        self.next_button = Button(button_frame, text="Следующая", command=self.next_page)
        self.next_button.pack(side=LEFT)

        self.last_button = Button(button_frame, text="Последняя страница", command=self.last_page)
        self.last_button.pack(side=LEFT)

        # Элементы управления страницами
        control_frame = Frame(self.root)
        control_frame.pack(fill=X)

        self.page_size_label = Label(control_frame, text="Записей на странице:")
        self.page_size_label.pack(side=LEFT)

        self.page_size_entry = Entry(control_frame, width=5)
        self.page_size_entry.insert(0, str(self.page_size))
        self.page_size_entry.pack(side=LEFT)

        self.set_page_size_button = Button(control_frame, text="Установить", command=self.set_page_size)
        self.set_page_size_button.pack(side=LEFT)

        self.info_label = Label(control_frame, text="")
        self.info_label.pack(side=LEFT)

        # Создание меню
        menu = Menu(self.root)
        self.root.config(menu=menu)

        # Добавление подменю
        file_menu = Menu(menu)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Добавить запись", command=self.add_record_dialog)
        file_menu.add_command(label="Поиск записи", command=self.search_record_dialog)
        file_menu.add_command(label="Удалить запись", command=self.delete_record_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Сохранить в XML", command=self.save_to_xml)
        file_menu.add_command(label="Загрузить из XML", command=self.load_from_xml)
        file_menu.add_separator()
        file_menu.add_command(label="Сохранить в БД", command=self.save_to_db)
        file_menu.add_command(label="Загрузить из БД", command=self.load_from_db)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        # Добавление панели инструментов
        toolbar = Frame(self.root)
        toolbar.pack(side=TOP, fill=X)

        add_button = Button(toolbar, text="Добавить запись", bg="#00FF00" , command=self.add_record_dialog)
        add_button.pack(side=LEFT)

        search_button = Button(toolbar, text="Поиск записи", bg="#00FFFF", command=self.search_record_dialog)
        search_button.pack(side=LEFT)

        delete_button = Button(toolbar, text="Удалить запись", bg="#DC143C", command=self.delete_record_dialog)
        delete_button.pack(side=LEFT)

        self.update_treeview()

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        start_index = self.current_page * self.page_size
        end_index = start_index + self.page_size
        for client in self.controller.get_clients()[start_index:end_index]:
            self.tree.insert("", END, values=(
                client.get_name(),
                client.get_surname(),
                client.get_otchestvo(),
                client.get_account_num(),
                client.get_address(),
                client.get_mob_telephone(),
                client.get_home_telephone()
            ))

        total_records = len(self.controller.get_clients())
        total_pages = (total_records + self.page_size - 1) // self.page_size  # Округление вверх
        self.info_label.config(text=f"Записи: {start_index + 1} - {min(end_index, total_records)} из {total_records}. "
                                     f"Страница {self.current_page + 1} из {total_pages}.")

    def update_hierarchical_tree(self):
        self.hierarchical_tree.delete(*self.hierarchical_tree.get_children())  # Очищаем дерево

        start_index = self.current_page * self.page_size
        end_index = start_index + self.page_size

        for client in self.controller.get_clients()[start_index:end_index]:
            client_id = self.hierarchical_tree.insert("", END, text=f"{client.get_surname()} {client.get_name()}", open=True)
            self.hierarchical_tree.insert(client_id, END, text=f"Отчество: {client.get_otchestvo()}")
            self.hierarchical_tree.insert(client_id, END, text=f"Номер счета: {client.get_account_num()}")
            self.hierarchical_tree.insert(client_id, END, text=f"Адрес: {client.get_address()}")
            self.hierarchical_tree.insert(client_id, END, text=f"Мобильный телефон: {client.get_mob_telephone()}")
            self.hierarchical_tree.insert(client_id, END, text=f"Домашний телефон: {client.get_home_telephone()}")

    def toggle_view(self):
        if self.show_hierarchical_var.get():  
            self.tree.pack_forget() 
            self.hierarchical_tree.pack(fill=BOTH, expand=True)  
            self.update_hierarchical_tree() 
        else: 
            self.hierarchical_tree.pack_forget()  
            self.tree.pack(fill=BOTH, expand=True)  
            self.update_treeview()  

    def add_record_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Добавить запись")

        labels = ["Имя", "Фамилия", "Отчество", "Номер счета (ХХХХХХ)", "Адрес", "Мобильный телефон (+ХХХХХХХ)", "Домашний телефон (ХХХ-ХХХ)"]
        entries = []
        for label in labels:
            Label(dialog, text=label).pack()
            entry = Entry(dialog)
            entry.pack()
            entries.append(entry)
        def save_record():
            name = entries[0].get()
            surname = entries[1].get()
            otchestvo = entries[2].get()
            account_num = entries[3].get()
            address = entries[4].get()
            mob_telephone = entries[5].get()
            home_telephone = entries[6].get()

            if not name or not surname or not otchestvo or not address:
                messagebox.showerror("Некорректный ввод", "Все поля должны быть заполнены")
                return
            
            if not re.match(r"^\+\d{7}$", mob_telephone):
                messagebox.showerror("Некорректный ввод", "Мобильный телефон должен быть в формате +xxxxxxx")
                return

            if not re.match(r"^\d{3}-\d{3}$", home_telephone):
                messagebox.showerror("Некорректный ввод", "Домашний телефон должен быть в формате xxx-xxx")
                return

            if not re.match(r"^\d{6}$", account_num):
                messagebox.showerror("Некорректный ввод", "Номер счета должен быть в формате xxxxxx")
                return

            try:
                account_num = int(account_num) 
                self.controller.add_client(name, surname, otchestvo, account_num, address, mob_telephone, home_telephone)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Номер счета должен быть числом")

        Button(dialog, text="Сохранить", command=save_record).pack(pady=10)

    def search_record_dialog(self):
        dialog = Toplevel(self.root, bg="lightblue")
        dialog.title("Поиск записи")

        toolbar = Frame(dialog, bg="lightblue")
        toolbar.pack(padx=10, pady=10, fill=X)

        first_cond = Button(toolbar, text="Поиск по номеру телефона или фамилии", 
                            command=lambda: self.search_by_something("Поиск по номеру телефона или фамилии", 
                                                                      "Введите фамилию или телефон (+ХХХХХХХ)/(ХХХ-ХХХ):", True))
        first_cond.pack(pady=5)

        second_cond = Button(toolbar, text="Поиск по номеру счета или адресу", 
                             command=lambda: self.search_by_something("Поиск по номеру счета или адресу", 
                                                                      "Введите номер счета (ХХХХХХ) или адрес:", False))
        second_cond.pack(pady=5)

        third_cond = Button(toolbar, text="Поиск по ФИО и цифрам встречающемся в одном из номеров"
        " (может быть заполнен только один элемент ФИО, например имя)", command=self.search_by_something_big)
        third_cond.pack(pady=5)


    
    def search_by_something(self,name: str, input_text: str, first: bool):
        dialog = Toplevel(self.root)
        dialog.title(name)

        Label(dialog, text=input_text).pack(pady=10)
        entry = Entry(dialog)
        entry.pack()

        result_box = Text(dialog, height=20, width=130)
        result_box.pack(pady=10)

        def search_records():
            query = entry.get()
            if first:
                results = self.controller.search_clients_by_first(query)
            else:
                results = self.controller.search_clients_by_second(query)
            result_box.delete(1.0, END)
            if results:
                for client in results:
                    result_box.insert(END, f"{client.get_surname()} {client.get_name()} {client.get_otchestvo()}, "
                                          f"Номер счета: {client.get_account_num()}, Адрес: {client.get_address()}, "
                                          f"Мобильный телефон: {client.get_mob_telephone()}, "
                                          f"Домашний телефон: {client.get_home_telephone()}\n")
            else:
                result_box.insert(END, "Записи не найдены.")

        Button(dialog, text="Поиск", command=search_records).pack(pady=10)

    def search_by_something_big(self):
        dialog = Toplevel(self.root)
        dialog.title("Поиск по ФИО и цифрам встречающемся в одном из номеров"
                     " (может быть заполнен только один элемент ФИО, например имя)")

        Label(dialog, text="Введите фамилию").pack(pady=10)
        entry_fam = Entry(dialog)
        entry_fam.pack()
        Label(dialog, text="Введите имя").pack(pady=10)
        entry_name = Entry(dialog)
        entry_name.pack()
        Label(dialog, text="Введите отчество").pack(pady=10)
        entry_otch = Entry(dialog)
        entry_otch.pack()
        Label(dialog, text="Введите цифры").pack(pady=10)
        entry_dig = Entry(dialog)
        entry_dig.pack()

        result_box = Text(dialog, height=20, width=130)
        result_box.pack(pady=10)

        def search_records():
            query_1 = entry_fam.get()
            query_2 = entry_name.get()
            query_3 = entry_otch.get()
            query_4 = entry_dig.get()
            results = self.controller.search_clients_by_third(query_2, query_1, query_3, query_4)
            result_box.delete(1.0, END)
            if results:
                for client in results:
                    result_box.insert(END, f"{client.get_surname()} {client.get_name()} {client.get_otchestvo()}, "
                                          f"Номер счета: {client.get_account_num()}, Адрес: {client.get_address()}, "
                                          f"Мобильный телефон: {client.get_mob_telephone()}, "
                                          f"Домашний телефон: {client.get_home_telephone()}\n")
            else:
                result_box.insert(END, "Записи не найдены.")

        Button(dialog, text="Поиск", command=search_records).pack(pady=10)
        

    def delete_record_dialog(self):
        dialog = Toplevel(self.root, bg="#FA8072")
        dialog.title("Поиск записи")

        toolbar = Frame(dialog, bg="#FA8072")
        toolbar.pack(padx=10, pady=10, fill=X)

        first_cond = Button(toolbar, text="Удалить по номеру телефона или фамилии", 
                            command=lambda: self.delete_by_something("Удалить по номеру телефона или фамилии", 
                                                                      "Введите фамилию или телефон (+ХХХХХХХ)/(ХХХ-ХХХ):", True))
        first_cond.pack(pady=5)

        second_cond = Button(toolbar, text="Удалить по номеру счета или адресу", 
                             command=lambda: self.delete_by_something("Удалить по номеру телефона или фамилии", 
                                                                      "Введите номер счета (ХХХХХХ) или адрес:", False))
        second_cond.pack(pady=5)

        third_cond = Button(toolbar, text="Удалить по ФИО и цифрам встречающемся в одном из номеров"
        " (может быть заполнен только один элемент ФИО, например имя)", command=self.delete_by_something_big)
        third_cond.pack(pady=5)

    def delete_by_something(self, name: str, input_text: str, first: bool):
        dialog = Toplevel(self.root)
        dialog.title(name)

        Label(dialog, text=input_text).pack(pady=10)
        entry = Entry(dialog)
        entry.pack()

        def delete_records():
            query = entry.get()
            if first:
                deleted_count = self.controller.delete_clients_first(query)
            else:
                deleted_count = self.controller.delete_clients_second(query)
            if deleted_count > 0:
                messagebox.showinfo("Удаление", f"Удалено записей: {deleted_count}")
            else:
                messagebox.showwarning("Удаление", "Записи не найдены.")
            dialog.destroy()

        Button(dialog, text="Удалить", command=delete_records).pack(pady=10)

    def delete_by_something_big(self):
        dialog = Toplevel(self.root)
        dialog.title("Удалить по ФИО и цифрам встречающемся в одном из номеров"
        " (может быть заполнен только один элемент ФИО, например имя)")

        Label(dialog, text="Введите фамилию").pack(pady=10)
        entry_fam = Entry(dialog)
        entry_fam.pack()
        Label(dialog, text="Введите имя").pack(pady=10)
        entry_name = Entry(dialog)
        entry_name.pack()
        Label(dialog, text="Введите отчество").pack(pady=10)
        entry_otch = Entry(dialog)
        entry_otch.pack()
        Label(dialog, text="Введите цифры").pack(pady=10)
        entry_dig = Entry(dialog)
        entry_dig.pack()

        def delete_records():
            query_1 = entry_fam.get()
            query_2 = entry_name.get()
            query_3 = entry_otch.get()
            query_4 = entry_dig.get()
            deleted_count = self.controller.delete_clients_third(query_2, query_1, query_3, query_4)
            if deleted_count > 0:
                messagebox.showinfo("Удаление", f"Удалено записей: {deleted_count}")
            else:
                messagebox.showwarning("Удаление", "Записи не найдены.")
            dialog.destroy()

        Button(dialog, text="Удалить", command=delete_records).pack(pady=10)

    def first_page(self):
        self.current_page = 0
        if self.show_hierarchical_var.get():
            self.update_hierarchical_tree()
        else:
            self.update_treeview()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            if self.show_hierarchical_var.get():
                self.update_hierarchical_tree()
            else:
                self.update_treeview()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.controller.get_clients()):
            self.current_page += 1
            if self.show_hierarchical_var.get():
                self.update_hierarchical_tree()
            else:
                self.update_treeview()

    def last_page(self):
        self.current_page = (len(self.controller.get_clients()) - 1) // self.page_size
        if self.show_hierarchical_var.get():
            self.update_hierarchical_tree()
        else:
            self.update_treeview()

    def set_page_size(self):
        try:
            new_size = int(self.page_size_entry.get())
            if new_size > 0:
                self.page_size = new_size
                self.current_page = 0  
                if self.show_hierarchical_var.get():
                    self.update_hierarchical_tree()
                else:
                    self.update_treeview()
        except ValueError:
            pass  

    def save_to_xml(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            self.controller.save_to_xml(file_path)
            messagebox.showinfo("Сохранение", "Данные успешно сохранены в XML.")

    def success_load(self, load: bool):
        if load:
            messagebox.showinfo("Загрузка", "Данные успешно загружены из XML.")
        else: 
            messagebox.showinfo("Ошибка", "С данными какая-то проблема.")

    def load_from_xml(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            success, message = self.controller.load_from_xml(file_path)
            if success:
                self.update_treeview()
                if self.show_hierarchical_var.get():
                    self.update_hierarchical_tree()
                messagebox.showinfo("Загрузка", message)
            else:
                messagebox.showerror("Ошибка загрузки", message)

    def save_to_db(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite files", "*.db")])
        if file_path:
            self.controller.save_to_db(file_path)
            messagebox.showinfo("Сохранение", "Данные успешно сохранены в базу данных.")

    def load_from_db(self):
        file_path = filedialog.askopenfilename(filetypes=[("SQLite files", "*.db")])
        if file_path:
            success, message = self.controller.load_from_db(file_path)
            if success:
                self.update_treeview()
                if self.show_hierarchical_var.get():
                    self.update_hierarchical_tree()
                messagebox.showinfo("Загрузка", message)
            else:
                messagebox.showerror("Ошибка загрузки", message)

    def run(self):
        self.root.mainloop()