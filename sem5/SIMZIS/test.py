import matplotlib.pyplot as plt
import numpy as np

# Ваши экспериментальные данные
lengths = [1, 2, 3, 4]
times = [1.5211105346679687e-05, 0.0020370960235595705, 0.4837979793548584, 75.96359300613403]

# Преобразуем в массивы numpy для удобства
lengths_np = np.array(lengths)
times_np = np.array(times)

# Создаем фигуру с двумя графиками
plt.figure(figsize=(14, 10))

# График 1: Линейная шкала
plt.subplot(2, 2, 1)
plt.plot(lengths_np, times_np, 'o-', linewidth=3, markersize=10, color='red', markerfacecolor='blue')
plt.xlabel('Длина пароля', fontsize=12)
plt.ylabel('Время подбора (секунды)', fontsize=12)
plt.title('Зависимость времени подбора от длины пароля\n(Линейная шкала)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xticks(lengths_np)

# Добавляем аннотации с значениями
for i, (x, y) in enumerate(zip(lengths_np, times_np)):
    if i == 3:  # Для последней точки смещаем аннотацию
        plt.annotate(f'{y:.2f} сек', (x, y), textcoords="offset points", xytext=(0,15), ha='center')
    else:
        plt.annotate(f'{y:.6f} сек', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

# График 2: Логарифмическая шкала по Y
plt.subplot(2, 2, 2)
plt.semilogy(lengths_np, times_np, 's-', linewidth=3, markersize=10, color='green', markerfacecolor='orange')
plt.xlabel('Длина пароля', fontsize=12)
plt.ylabel('Время подбора (секунды, log scale)', fontsize=12)
plt.title('Зависимость времени подбора от длины пароля\n(Логарифмическая шкала)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xticks(lengths_np)

# График 3: Предсказание для больших длин (экстраполяция)
plt.subplot(2, 2, (3, 4))

# Аппроксимируем экспоненциальной функцией
# Логарифмируем время и делаем линейную регрессию
log_times = np.log(times_np)
coefficients = np.polyfit(lengths_np, log_times, 1)
a = np.exp(coefficients[1])  # Коэффициент перед экспонентой
b = coefficients[0]          # Показатель степени

print(f"Аппроксимирующая функция: time = {a:.2e} * exp({b:.2f} * length)")

# Создаем точки для предсказания
prediction_lengths = np.array([1, 2, 3, 4, 5, 6, 7, 8])
predicted_times = a * np.exp(b * prediction_lengths)

# Рисуем экспериментальные данные и предсказание
plt.plot(lengths_np, times_np, 'o', markersize=10, color='red', label='Экспериментальные данные')
plt.plot(prediction_lengths, predicted_times, '--', linewidth=2, color='purple', label='Экстраполяция')

plt.yscale('log')
plt.xlabel('Длина пароля', fontsize=12)
plt.ylabel('Время подбора (секунды, log scale)', fontsize=12)
plt.title('Экстраполяция времени подбора для больших длин', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend()

# Добавляем аннотации с предсказанными значениями
for i, (x, y) in enumerate(zip(prediction_lengths[4:], predicted_times[4:])):
    plt.annotate(f'Длина {x}: {y:.1e} сек\n({y/3600:.1f} часов)', 
                (x, y), textcoords="offset points", xytext=(0,20), ha='center', 
                bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.7))

plt.tight_layout()
plt.savefig('password_cracking_time_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Выводим статистику
print("\n" + "="*60)
print("АНАЛИЗ ЭКСПОНЕНЦИАЛЬНОГО РОСТА ВРЕМЕНИ ПОДБОРА")
print("="*60)

print(f"\nЭкспериментальные данные:")
for length, time_val in zip(lengths, times):
    print(f"Длина {length}: {time_val:.9f} сек")

print(f"\nКоэффициент роста: {np.exp(b):.2f} раз на каждый дополнительный символ")
print(f"Время увеличивается в ~{np.exp(b):.0f} раз при увеличении длины на 1 символ")

print(f"\nПредсказание для больших длин:")
for length in [5, 6, 7, 8]:
    pred_time = a * np.exp(b * length)
    print(f"Длина {length}: {pred_time:.2e} сек ≈ {pred_time/3600:.1f} часов ≈ {pred_time/(3600*24):.1f} дней")