print("Hello world")
u = 10

k = [1, 2, 3]

for i in k[::-1]:
    print(i)

bk : str =  "bob"
o = "p"
i = bk + ' ' + o
print(f"{i} masia")

def my_po(b ,*pop, **o):
    for i in pop:
        print(i)
    
    print(f"\n{b}", end = ' ')
    print(o)
    print(pop)
my_po(1, 2, "roooor", 3, 8, c="lol", l = 1)


users = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 20}
]

users.sort(key = lambda x: x ["age"])
print(users)

person = {"name": "Alice"}

# Изменение значения
person["name"] = "Bob"

# Добавление нового ключа
person["age"] = 30

# Метод update() (объединение словарей)
person.update({"city": "Paris", "age": 35})
print(person)


for i , (v, k) in enumerate(person.items()):
    print(f"{i+1}.{v} = {k}")

class Bob:
    def __init__(self, op):
        self.poo = op
        print("ooo")

class ob(Bob):
    def __init__(self, op):
        super().__init__(op)
        print(self.poo, " pooo")

j = ob(2)      



class Person:
    def __init__(self, name):
        self._name = name  # защищённое поле

    @property
    def name(self):
        print("Доступ к имени")
        return self._name

    @name.setter
    def name(self, value):
        print("Изменение имени")
        if not isinstance(value, str):
            raise ValueError("Имя должно быть строкой")
        self._name = value

    @name.deleter
    def name(self):
        print("Удаление имени")
        del self._name

p = Person("Алексей")
print(p.name)      # Вызовет геттер
p.name = "Иван"    # Вызовет сеттер
del p.name  
p.name = "Иван" 
print(p.name)        # Вызовет делитер

#fff = [2**i for i in range(5) if i % 2 == 0 else 5]   
fff = [2**i if i % 2 == 0 else 5 for i in range(5)]

for i, ff in enumerate(fff):
    print(f"{i}{ff}", end = " ")


    