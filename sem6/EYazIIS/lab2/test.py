"""
Тест производительности Корпусного менеджера
Замеряет время обработки в зависимости от количества слов
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from text_processor import TextProcessor
import os

def create_test_files():
    """
    Создает тестовые файлы разного размера
    """
    test_files = []
    
    # Базовый текст (100 слов)
    base_text = """
    A little fir tree was born in the forest, and in the forest it grew.
Winter and summer it was slender and green.
A snowstorm sang to it: Sleep, little fir tree, bye-bye!
Frost wrapped it in snow: watch out, don't freeze!
A cowardly little gray bunny hopped under the fir tree.
Sometimes a wolf, an angry wolf, would trot past.
    """
    
    # Создаем файлы разного размера
    sizes = [1, 5, 10, 20, 50, 100, 200, 500]  # количество копий базового текста
    
    for i, size in enumerate(sizes):
        filename = f'test_file_{size}.txt'
        
        # Умножаем текст
        full_text = base_text * size
        
        # Сохраняем
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        test_files.append({
            'name': filename,
            'words': len(full_text.split()),
            'size': size
        })
    
    return test_files

def measure_performance(processor, test_files):
    """
    Замеряет время обработки каждого файла
    """
    results = {
        'words': [],
        'time': []
    }
    
    print("=" * 60)
    print("ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ КОРПУСНОГО МЕНЕДЖЕРА")
    print("=" * 60)
    
    for test_file in test_files:
        filename = test_file['name']
        words = test_file['words']
        
        print(f"\n📁 Обработка файла: {filename}")
        print(f"📊 Количество слов: {words}")
        
        # Засекаем время
        start_time = time.time()
        
        try:
            # Обрабатываем файл
            result = processor.process_file(filename)
            
            # Считаем время
            elapsed_time = time.time() - start_time
            
            # Сохраняем результаты
            results['words'].append(words)
            results['time'].append(elapsed_time)
            
            print(f"⏱️  Время обработки: {elapsed_time:.2f} секунд")
            print(f"✅ Предложений: {len(result['sentences'])}")
            
        except Exception as e:
            print(f"❌ Ошибка при обработке: {e}")
            results['words'].append(words)
            results['time'].append(None)
    
    return results

def plot_results(results):
    """
    Строит график производительности
    """
    # Убираем None значения
    words = []
    times = []
    for w, t in zip(results['words'], results['time']):
        if t is not None:
            words.append(w)
            times.append(t)
    
    if not words:
        print("Нет данных для построения графика")
        return
    
    # Создаем фигуру с двумя подграфиками
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # График 1: Зависимость времени от количества слов
    ax1.plot(words, times, 'bo-', linewidth=2, markersize=8, label='Время обработки')
    ax1.set_xlabel('Количество слов', fontsize=12)
    ax1.set_ylabel('Время обработки (секунды)', fontsize=12)
    ax1.set_title('Зависимость времени обработки от объема текста', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Добавляем линию тренда (полиномиальная аппроксимация)
    z = np.polyfit(words, times, 2)
    p = np.poly1d(z)
    x_trend = np.linspace(min(words), max(words), 100)
    ax1.plot(x_trend, p(x_trend), 'r--', alpha=0.7, label='Линия тренда')
    ax1.legend()
    
    # График 2: Скорость обработки (слов в секунду)
    speed = [w/t for w, t in zip(words, times)]
    ax2.bar(range(len(words)), speed, color='green', alpha=0.7)
    ax2.set_xlabel('Тестовый файл', fontsize=12)
    ax2.set_ylabel('Скорость (слов/секунду)', fontsize=12)
    ax2.set_title('Скорость обработки по файлам', fontsize=14)
    ax2.set_xticks(range(len(words)))
    ax2.set_xticklabels([f'{w} слов' for w in words], rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Добавляем значения на столбцы
    for i, v in enumerate(speed):
        ax2.text(i, v + max(speed)*0.01, f'{v:.0f}', 
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    # Сохраняем график
    plt.savefig('performance_test.png', dpi=300, bbox_inches='tight')
    print(f"\n📊 График сохранен в файл: performance_test.png")
    
    # Показываем график
    plt.show()

def print_statistics(results):
    """
    Выводит статистику тестирования
    """
    # Убираем None значения
    valid_data = [(w, t) for w, t in zip(results['words'], results['time']) if t is not None]
    
    if not valid_data:
        print("Нет данных для статистики")
        return
    
    words, times = zip(*valid_data)
    
    print("\n" + "=" * 60)
    print("📊 СТАТИСТИКА ТЕСТИРОВАНИЯ")
    print("=" * 60)
    
    print(f"\n📈 Всего обработано файлов: {len(valid_data)}")
    print(f"📝 Общее количество слов: {sum(words)}")
    print(f"⏱️  Общее время обработки: {sum(times):.2f} сек")
    print(f"⚡ Средняя скорость: {sum(words)/sum(times):.0f} слов/сек")
    print(f"🚀 Макс. скорость: {max(w/t for w, t in zip(words, times)):.0f} слов/сек")
    print(f"🐢 Мин. скорость: {min(w/t for w, t in zip(words, times)):.0f} слов/сек")
    
    # Анализ масштабирования
    if len(valid_data) >= 2:
        first_speed = words[0]/times[0]
        last_speed = words[-1]/times[-1]
        degradation = (1 - last_speed/first_speed) * 100
        
        print(f"\n📉 Деградация скорости при увеличении объема: {degradation:.1f}%")
        if degradation < 10:
            print("✅ Отличное масштабирование!")
        elif degradation < 25:
            print("👍 Хорошее масштабирование")
        else:
            print("⚠️ Значительная деградация скорости")

def cleanup_test_files(test_files):
    """
    Удаляет созданные тестовые файлы
    """
    print("\n" + "=" * 60)
    print("🧹 Очистка тестовых файлов")
    print("=" * 60)
    
    for test_file in test_files:
        filename = test_file['name']
        try:
            os.remove(filename)
            print(f"✓ Удален: {filename}")
        except Exception as e:
            print(f"✗ Не удалось удалить {filename}: {e}")

def run_comprehensive_test():
    """
    Запускает полное тестирование производительности
    """
    print("🚀 ЗАПУСК ТЕСТА ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 60)
    
    # Создаем процессор
    print("\n🔧 Инициализация процессора...")
    processor = TextProcessor()
    print("✓ Процессор готов")
    
    # Создаем тестовые файлы
    print("\n📄 Создание тестовых файлов...")
    test_files = create_test_files()
    print(f"✓ Создано {len(test_files)} файлов")
    for tf in test_files:
        print(f"  - {tf['name']}: {tf['words']} слов")
    
    # Запускаем тест
    print("\n⚡ Запуск измерения производительности...")
    results = measure_performance(processor, test_files)
    
    # Выводим статистику
    print_statistics(results)
    
    # Строим график
    print("\n📊 Построение графика...")
    plot_results(results)
    
    # Спрашиваем, удалять ли тестовые файлы
    print("\n" + "=" * 60)
    response = input("🗑️  Удалить тестовые файлы? (да/нет): ").lower().strip()
    if response in ['да', 'yes', 'y', 'д']:
        cleanup_test_files(test_files)
    else:
        print("ℹ️ Тестовые файлы оставлены для повторного использования")
    
    print("\n✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")

def run_simple_test():
    """
    Быстрый тест с одним файлом
    """
    print("🚀 БЫСТРЫЙ ТЕСТ")
    print("=" * 60)
    
    # Создаем процессор
    processor = TextProcessor()
    
    # Создаем тестовый текст
    test_text = """
    Быстрая лиса прыгает через ленивую собаку. Это классическое предложение для тестирования.
    Python это отличный язык программирования. Он используется для веб-разработки и анализа данных.
    Машинное обучение становится все более популярным. Нейронные сети решают сложные задачи.
    """ * 100  # 100 раз
    
    filename = 'quick_test.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(test_text)
    
    words = len(test_text.split())
    print(f"📊 Количество слов: {words}")
    
    # Замеряем время
    start_time = time.time()
    result = processor.process_file(filename)
    elapsed_time = time.time() - start_time
    
    print(f"⏱️  Время обработки: {elapsed_time:.2f} секунд")
    print(f"⚡ Скорость: {words/elapsed_time:.0f} слов/сек")
    print(f"✅ Предложений: {len(result['sentences'])}")
    
    # Удаляем файл
    os.remove(filename)
    print("🧹 Тестовый файл удален")

if __name__ == "__main__":
    print("ВЫБЕРИТЕ РЕЖИМ ТЕСТИРОВАНИЯ:")
    print("1 - Полное тестирование (несколько файлов, график)")
    print("2 - Быстрый тест (один файл)")
    print("3 - Оба теста")
    
    choice = input("Ваш выбор (1/2/3): ").strip()
    
    if choice == '1':
        run_comprehensive_test()
    elif choice == '2':
        run_simple_test()
    elif choice == '3':
        run_simple_test()
        print("\n" + "=" * 60 + "\n")
        run_comprehensive_test()
    else:
        print("Неверный выбор. Запускаю полное тестирование...")
        run_comprehensive_test()