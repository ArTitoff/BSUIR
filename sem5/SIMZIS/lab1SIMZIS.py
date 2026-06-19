# HelloWorld("print")

import random
import string
import time
from typing import Counter
import pandas as pd
import matplotlib.pyplot as plt


ALPHABET = string.ascii_lowercase

def gen_pass(length: int) -> str:
    password = ''.join(random.choice(ALPHABET) for _ in range(length))
    return password

def gen_chart(password: str):
    s = Counter(password)
    print(s.keys())
    print(s.values())
    s = pd.Series(s.values(), s.keys())
    return s

def main():
    try:
        length = int(input("Введите длину: "))
        password = gen_pass(length)
        print(f"generated password: {password}")
    except Exception as e:
        print(f"ужас: {e}")

    s = gen_chart(password)

    s.plot(kind="bar")  # столбчатый график
    plt.title("Частота букв в пароле")
    plt.xlabel("Буквы")
    plt.ylabel("Количество")
    #plt.show()
    plt.savefig("chart.png")
    
    print("occurencies frequency: ")

    average_time = 0
    new_password = gen_pass(length)   
    for _ in range(5):
        start = time.time()
        while new_password != password:
            new_password = gen_pass(length)

        new_password = ""
        end = time.time()
        average_time += end - start

        print(f"time: {end - start}")


    print(f"Среднее время подбора: ~{average_time / 5}")

if __name__ == "__main__":
    main()












    # def aazz(word: str, step: int) -> str:
#     if step == 1:
#         for i in ALPHABET:
#             print(word + i)
#             yield word + i
#     else:
#         for i in ALPHABET:
#             aazz(word+i, step-1)

# def main():
#     i = aazz('s',1)
# if __name__ == "__main__":
#     main()


# ALPHABET = string.ascii_lowercase

# def aazz(word: str, step: int):
#     if step == 1:
#         for i in ALPHABET:
#             yield word + i
#     else:
#         for i in ALPHABET:
#             yield from aazz(word + i, step - 1)

# def main():
#     # Пример использования для 1 символа (a-z)
#     print("Однобуквенные комбинации:")
#     for combo in aazz('', 1):
#         print(combo)
    
#     print("\nДвухбуквенные комбинации:")
#     # Пример для 2 символов (aa-zz)
#     for combo in aazz('', 2):
#         print(combo)
    
#     print("\nТрехбуквенные комбинации (первые 10):")
#     # Пример для 3 символов (первые 10)
#     count = 0
#     for combo in aazz('', 3):
#         print(combo)
#         count += 1
#         if count >= 10:
#             break

# if __name__ == "__main__":
#     main()



# def generate_combinations(length: int):
#     """Генерирует все комбинации букв заданной длины"""
#     for combo in product(ALPHABET, repeat=length):
#         yield ''.join(combo)



# # Использование:
#   for combo in generate_combinations(0):
 #      print(combo) 