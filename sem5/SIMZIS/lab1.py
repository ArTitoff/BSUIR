import random
import time
from typing import Counter
import pandas as pd
import matplotlib.pyplot as plt

ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" + "абвгдеёжзийклмнопрстуфхцчшщъыьэюя".upper()

def gen_pas(len: int) -> str:
    password = ''.join(random.choice(ALPHABET) for _ in range(len))
    print(f"Сгенерированный пароль: {password}")
    return password

def plot(password: str):
    s = Counter(password)
    print(s.values())
    print(s.keys())
    s = pd.Series(s.values(), s.keys())
    return s


def main():
    length = int(input("Введите длину пароля "))
    print(ALPHABET)

    password = gen_pas(length)
    s = plot(password)

    s.plot(kind="bar")  # столбчатый график
    plt.title("Частота букв в пароле")
    plt.xlabel("Буквы")
    plt.ylabel("Количество")
    #plt.show()
    plt.savefig("chart.png")

    # av_time = 0
    # newpass = gen_pas(length)
    # for _ in range(1):
    #     start = time.time()
    #     while password != newpass:
    #         newpass = gen_pas(length)
    #     end = time.time()
    #     av_time += end - start

    # print(f"Среднее время: ~{av_time / 1}")
    
if __name__ == "__main__":
    main()
