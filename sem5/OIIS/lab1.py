import numpy as np
import matplotlib.pyplot as plt
from math import pi, sin, cos


def fft(x):
    n = len(x)
    if n <= 1:
        return x
    
    even = fft(x[0::2])
    odd = fft(x[1::2])
    
    result = [0] * n
    for k in range(n//2):
        # Вычисляем поворотный множитель
        angle = 2 * pi * k / n
        w = complex(cos(angle), -sin(angle))  # Wₙᵏ
        
        # Бабочка
        result[k] = even[k] + w * odd[k]
        result[k + n//2] = even[k] - w * odd[k]
    
    return result

def test_fft():
    N = 64  
    fs = 100.0  # Частота дискретизации (Теорема Найквиста)
    T = 1.0 / fs  # Период дискретизации
    
    # Создание временной оси
    t = np.linspace(0.0, (N-1)*T, N)
    
    # Тест 1: Синусоидальный сигнал (частота 10 Гц)
    f1 = 10.0
    signal_sin = [sin(2 * pi * f1 * t_i) for t_i in t]
    
    # Тест 2: Косинусоидальный сигнал (частота 15 Гц)
    f2 = 15.0
    signal_cos = [cos(2 * pi * f2 * t_i) for t_i in t]
    
    # Вычисление БПФ
    fft_sin = fft(signal_sin)
    fft_cos = fft(signal_cos)

    
    # Вычисление амплитудного спектра
    freq = np.fft.fftfreq(N, T)[:N//2]
    amp_sin = 2.0/N * np.abs(fft_sin[:N//2])
    amp_cos = 2.0/N * np.abs(fft_cos[:N//2])

    # print(fft_sin)
    # print("="*100)
    print(amp_sin)
    print(freq)
    print("="*100)

    # Сравнение с numpy FFT для проверки
    np_fft_sin = np.fft.fft(signal_sin)
    np_amp_sin = 2.0/N * np.abs(np_fft_sin[:N//2])
    np_fft_cos = np.fft.fft(signal_cos)
    np_amp_cos = 2.0/N * np.abs(np_fft_cos[:N//2])
    
    # Визуализация результатов - только 2 сигнала (2 строки, 2 столбца)
    _, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Синусоидальный сигнал - временная область
    axes[0, 0].plot(t, signal_sin, 'b-')
    axes[0, 0].set_title('Сигнал: sin(2π*10t)')
    axes[0, 0].set_xlabel('Время [с]')
    axes[0, 0].set_ylabel('Амплитуда')
    axes[0, 0].grid(True)
    
    # Синусоидальный сигнал - частотная область
    axes[0, 1].plot(freq, amp_sin, 'r-', label='Наша реализация')
    axes[0, 1].plot(freq, np_amp_sin, 'b--', label='NumPy FFT', alpha=0.7)
    axes[0, 1].set_title('Амплитудный спектр sin(2π*10t)')
    axes[0, 1].set_xlabel('Частота [Гц]')
    axes[0, 1].set_ylabel('Амплитуда')
    axes[0, 1].legend()
    axes[0, 1].set_xlim(0, 50)
    axes[0, 1].grid(True)
    
    # Косинусоидальный сигнал - временная область
    axes[1, 0].plot(t, signal_cos, 'g-')
    axes[1, 0].set_title('Сигнал: cos(2π*15t)')
    axes[1, 0].set_xlabel('Время [с]')
    axes[1, 0].set_ylabel('Амплитуда')
    axes[1, 0].grid(True)
    
    # Косинусоидальный сигнал - частотная область
    axes[1, 1].plot(freq, amp_cos, 'r-', label='Наша реализация')
    axes[1, 1].plot(freq, np_amp_cos, 'g--', label='NumPy FFT', alpha=0.7)
    axes[1, 1].set_title('Амплитудный спектр cos(2π*15t)')
    axes[1, 1].set_xlabel('Частота [Гц]')
    axes[1, 1].set_ylabel('Амплитуда')
    axes[1, 1].legend()
    axes[1, 1].set_xlim(0, 50)
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig('fft_results.png', dpi=300, bbox_inches='tight')
    print("Графики сохранены в файл 'fft_results.png'")
    
    # Отдельные графики для сравнения
    plt.figure(figsize=(10, 6))
    plt.plot(freq, amp_sin, 'r-', label='Наш БПФ: sin(10Гц)')
    plt.plot(freq, amp_cos, 'g-', label='Наш БПФ: cos(15Гц)')
    plt.plot(freq, np_amp_sin, 'b--', label='NumPy FFT: sin(10Гц)', alpha=0.7)
    plt.plot(freq, np_amp_cos, 'm--', label='NumPy FFT: cos(15Гц)', alpha=0.7)
    plt.title('Сравнение БПФ для sin(10Гц) и cos(15Гц)')
    plt.xlabel('Частота [Гц]')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 50)
    plt.savefig('fft_comparison.png', dpi=300, bbox_inches='tight')
    
    # Проверка точности
    print("\nПроверка точности для синусоидального сигнала:")
    peak_idx_sin = np.argmax(amp_sin)
    print(f"Наш БПФ: пик на {freq[peak_idx_sin]:.2f} Гц, амплитуда = {amp_sin[peak_idx_sin]:.6f}")
    
    peak_idx_np_sin = np.argmax(np_amp_sin)
    print(f"NumPy FFT: пик на {freq[peak_idx_np_sin]:.2f} Гц, амплитуда = {np_amp_sin[peak_idx_np_sin]:.6f}")
    
    print("\nПроверка точности для косинусоидального сигнала:")
    peak_idx_cos = np.argmax(amp_cos)
    print(f"Наш БПФ: пик на {freq[peak_idx_cos]:.2f} Гц, амплитуда = {amp_cos[peak_idx_cos]:.6f}")
    
    peak_idx_np_cos = np.argmax(np_amp_cos)
    print(f"NumPy FFT: пик на {freq[peak_idx_np_cos]:.2f} Гц, амплитуда = {np_amp_cos[peak_idx_np_cos]:.6f}")


if __name__ == "__main__":
    print("Тестирование алгоритма БПФ на функциях sin(x) и cos(x)")
    test_fft()
    