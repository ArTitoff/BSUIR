# performance_test.py
"""
Тест производительности RAG системы
Замеряет время ответа модели на 7 вопросов и строит график
"""

import time
import sys
import matplotlib.pyplot as plt
import numpy as np
from rag_system import RAGSystem
from db import CorpusDatabase

# Конфигурация БД
DB_CONFIG = {
    'dbname': 'yazis_56',
    'user': 'postgres',
    'password': 'asd123',
    'host': '127.0.0.1',
    'port': '5432'
}

# Тестовые вопросы (7 штук)
TEST_QUESTIONS = [
    "What are the main services offered?",
    "How much does cleaning cost?",
    "What is the schedule for deliveries?",
    "Do you provide customer support?",
    "How long does it take to complete the service?",
    "What is included in the basic package?",
    "Can I cancel my order?"
]

def run_performance_test():
    """Запускает тест производительности"""
    
    print("=" * 60)
    print("🚀 ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ RAG СИСТЕМЫ")
    print("=" * 60)
    
    # Подключаемся к БД
    print("\n📂 Подключение к базе данных...")
    db = CorpusDatabase(DB_CONFIG)
    db.connect()
    
    # Создаём RAG систему
    print("🤖 Инициализация RAG системы...")
    rag = RAGSystem(db)
    
    results = []
    
    print("\n" + "=" * 60)
    print("📝 ЗАПУСК ТЕСТА")
    print("=" * 60)
    
    for i, question in enumerate(TEST_QUESTIONS, 1):
        print(f"\n[{i}/{len(TEST_QUESTIONS)}] Вопрос: {question}")
        
        # Замеряем время
        start_time = time.time()
        
        try:
            answer = rag.ask(question)
            elapsed_time = time.time() - start_time
            
            results.append({
                'question': question,
                'time': elapsed_time,
                'answer_preview': answer['answer'][:100] + "..." if len(answer['answer']) > 100 else answer['answer'],
                'sources': answer['sources'],
                'keywords': answer['keywords']
            })
            
            print(f"   ✅ Ответ получен за {elapsed_time:.2f} сек")
            print(f"   📄 Ответ: {results[-1]['answer_preview']}")
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            results.append({
                'question': question,
                'time': elapsed_time,
                'error': str(e),
                'answer_preview': f"ОШИБКА: {e}"
            })
            print(f"   ❌ Ошибка: {e}")
    
    # Закрываем соединение
    db.close()
    
    # Выводим статистику
    print("\n" + "=" * 60)
    print("📊 СТАТИСТИКА")
    print("=" * 60)
    
    valid_times = [r['time'] for r in results if 'error' not in r]
    
    if valid_times:
        print(f"✅ Успешных запросов: {len(valid_times)}/{len(results)}")
        print(f"⏱️  Среднее время ответа: {np.mean(valid_times):.2f} сек")
        print(f"⚡ Минимальное время: {np.min(valid_times):.2f} сек")
        print(f"🐢 Максимальное время: {np.max(valid_times):.2f} сек")
        print(f"📊 Стандартное отклонение: {np.std(valid_times):.2f} сек")
    
    # Строим график
    plot_results(results)
    
    return results

def plot_results(results):
    """Строит график времени ответа"""
    
    # Подготовка данных
    questions = [f"Q{i+1}" for i in range(len(results))]
    times = [r['time'] for r in results]
    colors = ['green' if 'error' not in r else 'red' for r in results]
    
    # Создаём фигуру с двумя подграфиками
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # График 1: Время ответа по каждому вопросу
    bars = ax1.bar(questions, times, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_xlabel('Вопрос', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Время ответа (секунды)', fontsize=12, fontweight='bold')
    ax1.set_title('⏱️ Время ответа модели по каждому вопросу', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Добавляем значения на столбцы
    for bar, time_val in zip(bars, times):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{time_val:.2f}s', ha='center', va='bottom', fontsize=9)
    
    # График 2: Статистика
    valid_times = [t for t in times if not isinstance(results[times.index(t)].get('error'), str)]
    
    if valid_times:
        # Гистограмма распределения
        ax2.hist(valid_times, bins=5, color='skyblue', edgecolor='black', alpha=0.7)
        ax2.axvline(np.mean(valid_times), color='red', linestyle='dashed', linewidth=2, 
                   label=f'Среднее: {np.mean(valid_times):.2f}s')
        ax2.axvline(np.median(valid_times), color='green', linestyle='dashed', linewidth=2,
                   label=f'Медиана: {np.median(valid_times):.2f}s')
        ax2.set_xlabel('Время ответа (секунды)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Частота', fontsize=12, fontweight='bold')
        ax2.set_title('📊 Распределение времени ответа', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(alpha=0.3)
    
    plt.suptitle('🚀 Performance Test Results', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    # Сохраняем график
    plt.savefig('performance_test_result.png', dpi=150, bbox_inches='tight')
    print("\n💾 График сохранён как 'performance_test_result.png'")
    
    plt.show()

def print_detailed_table(results):
    """Выводит подробную таблицу результатов"""
    
    print("\n" + "=" * 80)
    print("📋 ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ")
    print("=" * 80)
    
    print(f"\n{'№':<4} {'Вопрос':<40} {'Время':<10} {'Статус':<10}")
    print("-" * 80)
    
    for i, r in enumerate(results, 1):
        status = "✅ OK" if 'error' not in r else "❌ ERROR"
        question_short = r['question'][:37] + "..." if len(r['question']) > 37 else r['question']
        print(f"{i:<4} {question_short:<40} {r['time']:<10.2f} {status:<10}")

if __name__ == "__main__":
    print("\n🔧 Запуск теста производительности...")
    print("⚠️  ВНИМАНИЕ: Первый запрос может быть медленнее из-за загрузки модели в память\n")
    
    results = run_performance_test()
    print_detailed_table(results)
    
    print("\n" + "=" * 60)
    print("✅ ТЕСТ ЗАВЕРШЁН")
    print("=" * 60)