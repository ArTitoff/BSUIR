from itertools import product

class TFlipFlop:
    def __init__(self):
        self.state = 0
    
    def clock(self, T):
        if T:
            self.state ^= 1
        return self.state

def generate_counter_truth_table():
    """Генерирует таблицу истинности для 3-битного счетчика"""
    truth_table = []
    for q2, q1, q0 in product([0,1], repeat=3):
        next_q2 = q2 ^ (q1 & q0)
        next_q1 = q1 ^ q0
        next_q0 = 1 ^ q0
        
        T2 = q1 & q0
        T1 = q0
        T0 = 1
        
        truth_table.append((q2, q1, q0, next_q2, next_q1, next_q0, T2, T1, T0))
    return truth_table

def minimize_kmap(kmap):
    """Упрощенная минимизация с помощью карт Карно"""
    # Реальная реализация должна анализировать карту
    if sum(sum(1 for x in row if x == 1) for row in kmap) == len(kmap)**2:
        return "1"
    elif not any(any(x == 1 for x in row) for row in kmap):
        return "0"
    return "Minimized_Expr"

def synthesize_gates(truth_table):
    """Синтезирует логические функции для T-входов"""
    # Карты Карно для каждого T-входа
    kmaps = {
        'T2': [[0]*4 for _ in range(4)],
        'T1': [[0]*4 for _ in range(4)],
        'T0': [[1]*4 for _ in range(4)]  # T0 всегда 1
    }
    
    for row in truth_table:
        q2, q1, q0, _, _, _, T2, T1, _ = row
        # Преобразуем Q2,Q1 в индексы карты 4x4
        i = q2*2 + q1
        j = q0*2 + 0  # Упрощенная 2D карта
        
        kmaps['T2'][i][j] = T2
        kmaps['T1'][i][j] = T1
    
    # Минимизируем каждую функцию
    functions = {}
    for name, kmap in kmaps.items():
        functions[name] = minimize_kmap(kmap)
    
    return functions

def main():
    print("Синтез 3-битного двоичного счетчика на T-триггерах")
    print("=================================================")
    
    # Генерируем таблицу истинности
    truth_table = generate_counter_truth_table()
    
    print("\nТаблица истинности счетчика:")
    print("Q2 Q1 Q0 | Q2' Q1'  Q0' | T2 T1 T0")
    print("----------------------------------")
    for row in truth_table[:8]:  # Показываем все 8 состояний
        print(f"{row[0]}  {row[1]}  {row[2]}  |  {row[3]}   {row[4]}   {row[5]}   |  {row[6]}  {row[7]}  {row[8]}")
    
    # Синтезируем логические функции
    synthesize_gates(truth_table)
    

if __name__ == "__main__":
    main() 

