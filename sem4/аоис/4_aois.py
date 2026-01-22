from itertools import combinations

class BooleanMinimizer:
    def __init__(self):
        self.variables = []
    
    def parse_expression(self, expression, is_sknf):
        """Парсит выражение и возвращает список термов"""
        if is_sknf:
            return [t.strip('() ') for t in expression.replace(' ', '').split('&')]
        else:
            return [t.strip('() ') for t in expression.replace(' ', '').split('|')]
    
    def extract_variables(self, terms):
        """Извлекает список переменных из термов"""
        variables = set()
        for term in terms:
            i = 0
            while i < len(term):
                if term[i] == '!':
                    variables.add(term[i+1])
                    i += 2
                elif term[i] not in ('&', '|', '-'):
                    variables.add(term[i])
                    i += 1
                else:
                    i += 1
        self.variables = sorted(variables)
        return self.variables
    
    def term_to_binary(self, term, is_sknf):
        """Преобразует терм в бинарное представление"""
        bits = []
        for var in self.variables:
            if f'!{var}' in term:
                bits.append('0' if is_sknf else '1')
            elif var in term:
                bits.append('1' if is_sknf else '0')
            else:
                bits.append('-')
        return ''.join(bits)
    
    def can_combine(self, b1, b2):
        """Проверяет возможность склеивания двух термов"""
        diff = 0
        combined = []
        for c1, c2 in zip(b1, b2):
            if c1 == c2:
                combined.append(c1)
            elif c1 == '-' or c2 == '-':
                return None
            else:
                diff += 1
                combined.append('-')
        return ''.join(combined) if diff == 1 else None
    
    def binary_to_term(self, binary, is_sknf):
        """Преобразует бинарное представление обратно в терм"""
        terms = []
        for var, bit in zip(self.variables, binary):
            if bit == '0':
                terms.append(f'!{var}' if is_sknf else var)
            elif bit == '1':
                terms.append(var if is_sknf else f'!{var}')
        return '|'.join(terms) if is_sknf else '&'.join(terms)
    
    def minimize(self, expression, is_sknf):
        """Основная функция минимизации"""
        # Парсинг выражения
        terms = self.parse_expression(expression, is_sknf)
        self.extract_variables(terms)
        
        # Вывод исходных данных
        # print("\n" + "="*50)
        # print(f"Минимизация {'СКНФ' if is_sknf else 'СДНФ'}:")
        # print(f"Исходное выражение: {expression}")
        # print(f"Выделенные переменные: {', '.join(self.variables)}")
        
        # Преобразование в бинарный вид
        binary_terms = [self.term_to_binary(t, is_sknf) for t in terms]
       # print("\nБинарное представление термов:")
        # for t, b in zip(terms, binary_terms):
        #     print(f"{t} → {b}")
        
        # Процесс склеивания
        prime_implicants = set()
        current = binary_terms.copy()
        iteration = 1
        
        while True:
          #  print(f"\nИтерация {iteration}:")
            new_implicants = set()
            used = set()
            
            # Попарное склеивание
            for i, j in combinations(range(len(current)), 2):
                combined = self.can_combine(current[i], current[j])
                if combined:
                    new_implicants.add(combined)
                    used.add(i)
                    used.add(j)
                   # print(f"Склеиваем: {current[i]} + {current[j]} → {combined}")
            
            # Добавляем неиспользованные импликанты
            for i in range(len(current)):
                if i not in used:
                    prime_implicants.add(current[i])
            
            if not new_implicants:
                break
                
            current = list(new_implicants)
            iteration += 1
        
        # Удаление дубликатов
        prime_implicants = list(set(prime_implicants))
        
        # Вывод результатов
        # print("\nПростые импликанты:")
        # for imp in prime_implicants:
        #     print(f"{imp} → ({self.binary_to_term(imp, is_sknf)})")
        
        # Формирование результата
        operator = ' & ' if is_sknf else ' | '
        minimized = operator.join(f'({self.binary_to_term(imp, is_sknf)})' for imp in prime_implicants)
        
        print(f"Минимизированная {'СКНФ' if is_sknf else 'СДНФ'}: {minimized}")
        return minimized

# Пример использования
minimizer = BooleanMinimizer()

# Минимизация СДНФ
sdnf = "(!a&!b&c) | (!a&b&!c) | (a&b&c) | (a&!b&!c)"
minimizer.minimize(sdnf, is_sknf=False)

sdnf_2 = "(a&!b&c) | (!a&b&c) | (a&b&c) | (a&b&!c) "
minimizer.minimize(sdnf_2, is_sknf=False)


def summator():
    print("\nТаблица истинности ОДС-3 (одноразрядного сумматора на 3 входа)")
    print("=========================")
    print("| a | b | c |  S* |  P* |")
    print("=========================")
    for a in [0,1]:
        for b in [0,1]:
            for c in [0,1]:
                sum = (a + b + c) % 2
                carry = (a & b) | (a & c) | (b & c)

                print(f"| {a} | {b} | {c} |  {sum}  |  {carry}  |")
                print("-------------------------")

if __name__ == "__main__":
    summator()

from itertools import product

def generate_bcd_plus_n_truth_table(n):
    """
    Генерирует таблицу истинности для преобразователя Д8421 в Д8421+n
    Возвращает кортеж: (таблица_истинности, неопределенные_комбинации)
    """
    truth_table = []
    undefined = []
    
    for d, c, b, a in product([0, 1], repeat=4):
        input_num = d*8 + c*4 + b*2 + a
        
        if input_num <= 9:
            # Корректная BCD цифра
            output_num = (input_num + n) % 10
            carry = 1 if (input_num + n) > 9 else 0
            
            output_d = (output_num >> 3) & 1
            output_c = (output_num >> 2) & 1
            output_b = (output_num >> 1) & 1
            output_a = output_num & 1
            
            truth_table.append((d, c, b, a, output_d, output_c, output_b, output_a))
        else:
            # Неопределенная комбинация (не BCD)
            undefined.append((d, c, b, a))
    
    return truth_table, undefined

def print_truth_table(truth_table, undefined):
    """Выводит полную таблицу истинности"""
    print("Полная таблица истинности:")
    print("D C B A | D' C' B' A'")
    print("-----------------------")
    
    # Выводим определенные комбинации
    for row in truth_table:
        print(f"{row[0]} {row[1]} {row[2]} {row[3]} |  {row[4]}  {row[5]}  {row[6]}  {row[7]}")
    
    # Выводим неопределенные комбинации
    for comb in undefined:
        print(f"{comb[0]} {comb[1]} {comb[2]} {comb[3]} |  X  X  X  X")

def generate_sdnf(truth_table, output_index):
    """
    Генерирует СДНФ для указанного выхода в формате с ! & |
    """
    sdnf_terms = []
    
    for row in truth_table:
        d, c, b, a = row[:4]
        output = row[4 + output_index]
        
        if output == 1:
            term = []
            if d == 0: term.append('!D')
            else: term.append('D')
            if c == 0: term.append('!C')
            else: term.append('C')
            if b == 0: term.append('!B')
            else: term.append('B')
            if a == 0: term.append('!A')
            else: term.append('A')
            
            sdnf_terms.append(f"({'&'.join(term)})")
    
    return ' | '.join(sdnf_terms) if sdnf_terms else '0'


def main():
    print("Синтез преобразователя Д8421 в Д8421+n")
    print("======================================")
    
    n = int(input("Введите n (1-9): "))
    if n < 1 or n > 9:
        print("Некорректное значение n!")
        return
    
    truth_table, undefined = generate_bcd_plus_n_truth_table(n)
    print_truth_table(truth_table, undefined)
    
    print("\nСДНФ и минимизированные выражения:")
    outputs = [
        (0, "D'"),
        (1, "C'"), 
        (2, "B'"), 
        (3, "A'")
    ]
    
    for index, name in outputs:
        sdnf = generate_sdnf(truth_table, index)
        print(f"\n{name}:")
        print(f"СДНФ: {sdnf}")
    print("\n======================================\n")
    for index, name in outputs:
        sdnf = generate_sdnf(truth_table, index)
        print(f"\n{name}:")
        minimizer.minimize(sdnf, is_sknf=False)
        

if __name__ == "__main__":
    main()


