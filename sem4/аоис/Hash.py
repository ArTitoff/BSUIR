from Record_and_AVL import AVLTree, Record
from tabulate import tabulate

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [AVLTree() for _ in range(size)]
        self.counter = 0

    def _hash_function(self, key): # хэш ключа как остаток от суммы ASCII-кодов всех символов по модулю размера таблицы
        return sum(ord(c) for c in key) % self.size

    def insert(self, key, data):
        index = self._hash_function(key)
        tree = self.table[index]

        collision_flag = tree.root is not None

        record = Record(self.counter, key, data)
        record.collision = collision_flag
        self.counter += 1

        tree.root = tree.insert(tree.root, record)

    def delete(self, key):
        index = self._hash_function(key)
        tree = self.table[index]
        tree.root = tree.delete(tree.root, key)

    def search(self, key):
        index = self._hash_function(key)
        tree = self.table[index]
        node = tree.search(tree.root, key)
        return node.record if node else None

    def display(self):
        headers = ["Индекс", "Хэш", "Ключ", "Данные"]
        rows = []

        hash_stats_headers = ["Индекс", "Количество записей", "Коллизии"]
        hash_stats_rows = []

        for i, tree in enumerate(self.table):
            if tree.root:
                count = self._tree_to_table(tree.root, rows, i)
                collisions = "Да" if count > 1 else "Нет"
                hash_stats_rows.append([i, count, collisions])
            else:
                hash_stats_rows.append([i, 0, "Нет"])

        print("Содержимое хэш-таблицы:")
        print(tabulate(rows, headers=headers, tablefmt="grid"))

        print("\nСтатистика хэшей и коллизий:")
        print(tabulate(hash_stats_rows, headers=hash_stats_headers, tablefmt="grid"))

        print("\nДеревья цепочек для каждого индекса:")
        for i, tree in enumerate(self.table):
            print(f"\nИндекс {i}:")
            if tree.root:
                tree.pretty_print(tree.root)
            else:
                print("  (пусто)")

    def _tree_to_table(self, node, rows, index):
        if not node:
            return 0

        rows.append([index, node.record.key, node.record.data])

        left_count = self._tree_to_table(node.left, rows, index)
        right_count = self._tree_to_table(node.right, rows, index)

        return 1 + left_count + right_count

    def display_trees_structure(self):
        print("\nСтруктура деревьев в хэш-таблице:")

        for i, tree in enumerate(self.table):  # Проходим по всем деревьям в таблице
            print(f"\nИндекс {i}:")
            if tree.root:  # Если дерево не пустое
                root = tree.root
                print(f"Корневой узел: [{root.record.key}] -> {root.record.data}")

                # Левый узел
                if root.left:
                    print(f"  Левое поддерево: [{root.left.record.key}] -> {root.left.record.data}")
                else:
                    print(f"  Левое поддерево: (пусто)")

                # Правый узел
                if root.right:
                    print(f"  Правое поддерево: [{root.right.record.key}] -> {root.right.record.data}")
                else:
                    print(f"  Правое поддерево: (пусто)")
            else:
                print("  Дерево пусто")
