import matplotlib.pyplot as plt

# Данные о количестве операций
operations = ['Создание', 'Запись', 'Чтение', 'Удаление', 'Копирование', 'Перемещение']
counts = [1, 2, 2, 1, 1, 1]  # Замените на реальные данные

# Построение графика
plt.bar(operations, counts, color='green')
plt.xlabel('Операции')
plt.ylabel('Количество')
plt.title('Количество операций файловой системы')
plt.show()
