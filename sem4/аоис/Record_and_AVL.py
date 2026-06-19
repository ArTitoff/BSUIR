# баланс = высота_левого_поддерева - высота_правого_поддерева (-1 до 1 — всё в порядке, дерево сбалансировано)



class Record:
    def __init__(self, index, key, data):
        self.index = index
        self.key = key
        self.data = data
        self.collision = False

    def __str__(self):
        return f"[{self.index}] '{self.key}': '{self.data}' (Коллизия: {'Да' if self.collision else 'Нет'})"

class AVLNode:
    def __init__(self, record):
        self.record = record # Содержит сам объект Record
        self.height = 1 # Высота узла
        self.left = None # Ссылка на лево (левое поддерево)
        self.right = None # Ссылка на право (право поддерево)


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, record):
        if not root:
            return AVLNode(record)

        if record.key < root.record.key: # В зависимости от ключа или влево или вправо
            root.left = self.insert(root.left, record)
        elif record.key > root.record.key:
            root.right = self.insert(root.right, record)
        else:
            root.record.data = record.data
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        return self.balance(root)

    def delete(self, root, key):
        if not root:
            return root

        if key < root.record.key:
            root.left = self.delete(root.left, key)
        elif key > root.record.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left: # Если у удаляемого узла есть только один потомок, он заменяется на этот потомок
                return root.right
            elif not root.right:
                return root.left

            temp = self.get_min_value_node(root.right) # Если у узла два потомка, его замещают минимальным значением из правого поддерева
            root.record = temp.record
            root.right = self.delete(root.right, temp.record.key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        return self.balance(root)

    def search(self, root, key):
        if not root or root.record.key == key:
            return root

        if key < root.record.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def get_min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def get_height(self, root):
        return root.height if root else 0

    def get_balance(self, root):
        return self.get_height(root.left) - self.get_height(root.right) if root else 0

    def balance(self, root):
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def pretty_print(self, node, indent="", last=True):
        if node:
            prefix = "└── " if last else "├── "
            print(indent + prefix + f"[{node.record.key}] -> {node.record.data}")

            indent += "    " if last else "│   "

            self.pretty_print(node.left, indent, last=False)
            self.pretty_print(node.right, indent, last=True)