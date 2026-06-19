class HashTable:
    class Entry:
        def __init__(self, key, data):
            self.key = key          # ID - ключ (фамилия студента)
            self.data = data        # Pi - данные (имя, увлечения)
            self.collision = False  # C - флаг коллизии
            self.occupied = True    # U - флаг "занято"
            self.terminal = True    # T - терминальный флаг
            self.link = True        # L - флаг связи (True - указатель)
            self.deleted = False    # D - флаг удаления
            self.next = None        # Po - указатель на следующий элемент

        def __str__(self):
            return (f"Key: {self.key}, Data: {self.data}, "
                    f"C: {self.collision}, U: {self.occupied}, "
                    f"T: {self.terminal}, L: {self.link}, "
                    f"D: {self.deleted}, Next: {self.next.key if self.next else None}")

    def __init__(self, size):
        self.size = size
        self.table = [None] * size  # Инициализация таблицы
        self.base_address = 0       # B - базовый адрес (кратен размеру таблицы)

    def hash_function(self, key):
        """Вычисление хеш-адреса по ключу"""
        if isinstance(key, str):
            # Преобразование строки в числовое значение
            numeric_value = sum(ord(c) * (i+1) for i, c in enumerate(key[:3]))
        else:
            numeric_value = int(key)
        
        # Вычисление хеш-адреса: h(V) = (B + V) % H
        return (self.base_address + numeric_value) % self.size

    def insert(self, key, data):
        """Вставка элемента в хеш-таблицу"""
        index = self.hash_function(key)
        new_entry = self.Entry(key, data)

        if self.table[index] is None:
            # Ячейка пуста, просто добавляем элемент
            self.table[index] = new_entry
        else:
            # Обработка коллизии - добавляем в цепочку
            current = self.table[index]
            current.collision = True  # Устанавливаем флаг коллизии
            
            # Ищем последний элемент в цепочке
            while current.next is not None:
                current = current.next
            
            current.terminal = False  # Предыдущий элемент больше не терминальный
            current.next = new_entry  # Добавляем новый элемент в конец цепочки
        
        print(f"Добавлен студент: {key}")

    def search(self, key):
        """Поиск элемента по ключу"""
        index = self.hash_function(key)
        current = self.table[index]
        
        while current is not None:
            if current.key == key and not current.deleted:
                return current.data
            current = current.next
        
        return None

    def update(self, key, new_data):
        """Обновление данных по ключу"""
        index = self.hash_function(key)
        current = self.table[index]
        
        while current is not None:
            if current.key == key and not current.deleted:
                current.data = new_data
                return True
            current = current.next
        
        return False

    def delete(self, key):
        """Удаление элемента (логическое - установка флага D)"""
        index = self.hash_function(key)
        current = self.table[index]
        
        while current is not None:
            if current.key == key and not current.deleted:
                current.deleted = True
                current.occupied = False
                print(f"Студент {key} удален (помечен как удаленный)")
                return True
            current = current.next
        
        print(f"Студент {key} не найден")
        return False

    def print_table(self):
        """Вывод содержимого хеш-таблицы"""
        print("\nТекущее состояние хеш-таблицы:")
        print("Индекс | Элементы")
        print("-------------------------------")
        for i in range(self.size):
            print(f"[{i:2d}]", end=" | ")
            current = self.table[i]
            while current is not None:
                status = " (удален)" if current.deleted else ""
                print(f"{current.key}{status}", end="")
                if current.next is not None:
                    print(" -> ", end="")
                current = current.next
            print()

    def load_factor(self):
        """Вычисление коэффициента заполнения"""
        count = 0
        for i in range(self.size):
            current = self.table[i]
            while current is not None:
                if not current.deleted:
                    count += 1
                current = current.next
        return count / self.size


# Пример использования для хранения данных о студентах
if __name__ == "__main__":
    # Создаем хеш-таблицу на 15 элементов
    ht = HashTable(15)
    
    # Добавляем студентов
    students = [
        ("Иванов", {"имя": "Алексей", "увлечения": ["футбол", "программирование"]}),
        ("Петров", {"имя": "Дмитрий", "увлечения": ["шахматы", "чтение"]}),
        ("Сидоров", {"имя": "Михаил", "увлечения": ["плавание", "музыка"]}),
        ("Кузнецов", {"имя": "Сергей", "увлечения": ["бег", "рисование"]}),
        ("Смирнов", {"имя": "Андрей", "увлечения": ["теннис", "кино"]}),
        ("Васильев", {"имя": "Иван", "увлечения": ["велоспорт", "фотография"]}),
        ("Попов", {"имя": "Николай", "увлечения": ["бокс", "поэзия"]}),
        ("Новиков", {"имя": "Павел", "увлечения": ["волейбол", "театр"]}),
        ("Федоров", {"имя": "Артем", "увлечения": ["гимнастика", "живопись"]}),
        ("Морозов", {"имя": "Виктор", "увлечения": ["лыжи", "история"]}),
    ]
    
    # Вставляем данные в таблицу
    for key, data in students:
        ht.insert(key, data)
    
    # Выводим таблицу
    ht.print_table()
    
    # Поиск студента
    print("\nПоиск студента Иванов:", ht.search("Иванов"))
    
    # Обновление данных
    ht.update("Иванов", {"имя": "Алексей", "увлечения": ["баскетбол", "программирование"]})
    print("После обновления Иванов:", ht.search("Иванов"))
    
    # Удаление студента
    ht.delete("Петров")
    ht.print_table()
    
    # Коэффициент заполнения
    print(f"\nКоэффициент заполнения: {ht.load_factor():.2f}")