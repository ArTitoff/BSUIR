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
        print("\n" + "="*50)
        print(f"Минимизация {'СКНФ' if is_sknf else 'СДНФ'}:")
        print(f"Исходное выражение: {expression}")
        print(f"Выделенные переменные: {', '.join(self.variables)}")
        
        # Преобразование в бинарный вид
        binary_terms = [self.term_to_binary(t, is_sknf) for t in terms]
        print("\nБинарное представление термов:")
        for t, b in zip(terms, binary_terms):
            print(f"{t} → {b}")
        
        # Процесс склеивания
        prime_implicants = set()
        current = binary_terms.copy()
        iteration = 1
        
        while True:
            print(f"\nИтерация {iteration}:")
            new_implicants = set()
            used = set()
            
            # Попарное склеивание
            for i, j in combinations(range(len(current)), 2):
                combined = self.can_combine(current[i], current[j])
                if combined:
                    new_implicants.add(combined)
                    used.add(i)
                    used.add(j)
                    print(f"Склеиваем: {current[i]} + {current[j]} → {combined}")
            
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
        print("\nПростые импликанты:")
        for imp in prime_implicants:
            print(f"{imp} → ({self.binary_to_term(imp, is_sknf)})")
        
        # Формирование результата
        operator = ' & ' if is_sknf else ' | '
        minimized = operator.join(f'({self.binary_to_term(imp, is_sknf)})' for imp in prime_implicants)
        
        print(f"\nМинимизированная {'СКНФ' if is_sknf else 'СДНФ'}: {minimized}")
        return minimized

# Пример использования
minimizer = BooleanMinimizer()

# Минимизация СКНФ
sknf = "(a|b|!c) & (a|b|c) & (!a|b|c) & (!a|b|!c) & (!a|!b|c)"
minimizer.minimize(sknf, is_sknf=True)

# Минимизация СДНФ
sdnf = "(!a&!b&c) | (!a&b&!c) | (!a&b&c) | (a&!b&!c) | (a&!b&c) | (a&b&!c)"
minimizer.minimize(sdnf, is_sknf=False)


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
from itertools import combinations

class TableMinimizer:
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
    
    def count_ones(self, binary):
        """Считает количество единиц в бинарном представлении"""
        return binary.count('1')
    
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
    
    def print_implicant_table(self, groups, is_sknf):
        """Красиво выводит таблицу импликант с буквенными выражениями"""
        print("\nТаблица импликант:")
        print("-" * 60)
        for ones in sorted(groups.keys()):
            print(f"Группа {ones}:", end=" ")
            for term, used in groups[ones]:
                term_str = self.binary_to_term(term, is_sknf)
                mark = "✓" if used else ""
                print(f"{term_str:<10}{mark}", end="  ")
            print()
        print("-" * 60)
    
    def print_coverage_table(self, coverage, original_terms, is_sknf):
        """Красиво выводит таблицу покрытия с буквенными выражениями"""
        print("\nТаблица покрытия:")
        
        # Преобразуем оригинальные термы в буквенные выражения
        original_exprs = [self.binary_to_term(t, is_sknf) for t in original_terms]
        
        # Определяем максимальную ширину столбцов
        max_imp_len = max(len(self.binary_to_term(imp, is_sknf)) for imp, _ in coverage)
        max_term_len = max(len(expr) for expr in original_exprs)
        
        # Ширина таблицы
        table_width = max_imp_len + 3 + len(original_exprs)*(max_term_len + 3) + 1
        print("-" * table_width)
        
        # Заголовок таблицы
        header = "Импликанта".ljust(max_imp_len) + " |"
        for expr in original_exprs:
            header += f" {expr.center(max_term_len)} |"
        print(header)
        print("-" * table_width)
        
        # Тело таблицы
        for prime, row in coverage:
            term_str = self.binary_to_term(prime, is_sknf)
            line = f"{term_str.ljust(max_imp_len)} |"
            for i, covered in enumerate(row):
                line += f" {'X' if covered else ' ':{max_term_len}} |"
            print(line)
        print("-" * table_width)
    
    def minimize(self, expression, is_sknf):
        """Основная функция минимизации"""
        print("\n" + "="*60)
        print(f"Минимизация {'СКНФ' if is_sknf else 'СДНФ'} расчетно-табличным методом:")
        print(f"Исходное выражение: {expression}")
        
        # Парсинг и подготовка данных
        terms = self.parse_expression(expression, is_sknf)
        self.extract_variables(terms)
        binary_terms = [self.term_to_binary(t, is_sknf) for t in terms]
        
        # Вывод исходных данных
        print("\nБинарное представление:")
        for t, b in zip(terms, binary_terms):
            print(f"{t.ljust(15)} → {b} → {self.binary_to_term(b, is_sknf)}")
        
        # Находим простые импликанты
        print("\nПоиск простых импликант:")
        prime_implicants = self._find_prime_implicants(binary_terms, is_sknf)
        
        # Строим таблицу покрытия
        coverage = self._build_coverage_table(prime_implicants, binary_terms)
        self.print_coverage_table(coverage, binary_terms, is_sknf)
        
        # Выбираем минимальное покрытие
        essential = self._select_essential_primes(coverage, prime_implicants, is_sknf)
        
        # Формируем результат
        operator = ' & ' if is_sknf else ' | '
        minimized = operator.join(f'({self.binary_to_term(imp, is_sknf)})' for imp in essential)
        print(f"\nРезультат минимизации: {minimized}")
    
    def _find_prime_implicants(self, binary_terms, is_sknf):
        """Находит простые импликанты методом Квайна"""
        # Группируем по количеству единиц
        groups = {}
        for term in binary_terms:
            ones = self.count_ones(term)
            if ones not in groups:
                groups[ones] = []
            groups[ones].append((term, False))
        
        prime_implicants = []
        changed = True
        
        while changed:
            self.print_implicant_table(groups, is_sknf)
            new_groups = {}
            used_terms = set()
            changed = False
            
            # Перебираем соседние группы
            sorted_groups = sorted(groups.keys())
            for i in range(len(sorted_groups)-1):
                g1 = sorted_groups[i]
                g2 = sorted_groups[i+1]
                
                # Пробуем склеить все комбинации
                for term1, _ in groups[g1]:
                    for term2, _ in groups[g2]:
                        combined = self.can_combine(term1, term2)
                        if combined:
                            ones = self.count_ones(combined)
                            if ones not in new_groups:
                                new_groups[ones] = []
                            new_groups[ones].append((combined, False))
                            used_terms.add(term1)
                            used_terms.add(term2)
                            changed = True
            
            # Добавляем неиспользованные термы
            for group in groups.values():
                for term, _ in group:
                    if term not in used_terms:
                        prime_implicants.append(term)
            
            groups = new_groups
        
        return prime_implicants
    
    def _build_coverage_table(self, primes, original_terms):
        """Строит таблицу покрытия"""
        coverage = []
        for prime in primes:
            row = []
            for term in original_terms:
                covered = True
                for p, t in zip(prime, term):
                    if p != '-' and p != t:
                        covered = False
                        break
                row.append(covered)
            coverage.append((prime, row))
        return coverage
    
    def _select_essential_primes(self, coverage, primes, is_sknf):
        """Выбирает существенные простые импликанты"""
        essential = []
        remaining_terms = set(range(len(coverage[0][1])))
        
        while remaining_terms:
            best_idx = -1
            best_covered = set()
            
            for i, (prime, row) in enumerate(coverage):
                if i in [p[0] for p in essential]:
                    continue
                
                covered = {j for j, val in enumerate(row) if val and j in remaining_terms}
                if len(covered) > len(best_covered):
                    best_idx = i
                    best_covered = covered
            
            if best_idx == -1:
                break
            
            essential.append((best_idx, primes[best_idx]))
            remaining_terms -= best_covered
        
        return [imp for idx, imp in essential]

# Пример использования
minimizer = TableMinimizer()

# Минимизация СКНФ
sknf = "(a|b|!c) & (a|!b|c) & (!a|b|c) & (!a|b|!c) & (!a|!b|c)"
minimizer.minimize(sknf, is_sknf=True)

# Минимизация СДНФ
sdnf = "(!a&!b&c) | (!a&b&!c) | (!a&b&c) | (a&!b&!c) | (a&!b&c) | (a&b&!c)"
minimizer.minimize(sdnf, is_sknf=False)

from itertools import product

class KarnaughMap:
    def __init__(self, variables):
        self.variables = variables
        self.kmap = {}
        self.groups = []
    
    def setup_map(self):
        """Создает пустую карту Карно"""
        n = len(self.variables)
        if n < 2 or n > 4:
            raise ValueError("Карты Карно работают только для 2-4 переменных")
        
        # Генерация серого кода
        def gray_code(bits):
            if bits == 1:
                return ['0', '1']
            prev = gray_code(bits-1)
            return ['0'+x for x in prev] + ['1'+x for x in prev[::-1]]
        
        if n == 2:
            self.rows = gray_code(1)
            self.cols = gray_code(1)
        elif n == 3:
            self.rows = gray_code(2)
            self.cols = gray_code(1)
        else:  # n == 4
            self.rows = gray_code(2)
            self.cols = gray_code(2)
        
        # Инициализируем карту None
        self.kmap = {row: {col: None for col in self.cols} for row in self.rows}
        return self.rows, self.cols
    
    def print_map(self):
        """Выводит карту Карно"""
        print("\nКарта Карно:")
        header = "     " + " ".join(self.cols)
        print(header)
        print("    " + "-"*(len(self.cols)*2 + 1))
        
        for row in self.rows:
            line = f"{row} | "
            for col in self.cols:
                val = self.kmap[row][col]
                line += f"{'1' if val == 1 else '0' if val == 0 else ' '} "
            print(line)
    
    def find_groups(self, target_value):
        """Находит группы ячеек с заданным значением"""
        visited = set()
        groups = []
        
        group_sizes = [8, 4, 2, 1] if len(self.variables) == 4 else [4, 2, 1]
        
        for size in group_sizes:
            for i, row in enumerate(self.rows):
                for j, col in enumerate(self.cols):
                    if self.kmap[row][col] == target_value and (i,j) not in visited:
                        group = self._find_group(i, j, size, target_value, visited)
                        if group:
                            groups.append(group)
                            for cell in group:
                                visited.add(cell)
        
        self.groups = groups
        return groups
    
    def _find_group(self, i, j, size, target_value, visited):
        """Вспомогательная функция для поиска группы"""
        group = [(i,j)]
        
        if size == 4:
            # Проверяем квадрат 2x2
            for di, dj in [(0,1), (1,0), (1,1)]:
                ni = (i + di) % len(self.rows)
                nj = (j + dj) % len(self.cols)
                if (ni,nj) not in visited and self.kmap[self.rows[ni]][self.cols[nj]] == target_value:
                    group.append((ni,nj))
            
            if len(group) == 4:
                return group
            
            # Проверяем другие комбинации
            group = [(i,j)]
            # Горизонтальная полоса
            if all(self.kmap[self.rows[i]][self.cols[(j+k)%len(self.cols)]] == target_value 
                   and (i,(j+k)%len(self.cols)) not in visited for k in range(4)):
                return [(i,(j+k)%len(self.cols)) for k in range(4)]
            
            # Вертикальная полоса
            if all(self.kmap[self.rows[(i+k)%len(self.rows)]][self.cols[j]] == target_value 
                   and ((i+k)%len(self.rows),j) not in visited for k in range(4)):
                return [((i+k)%len(self.rows),j) for k in range(4)]
            
            return None
        
        elif size == 2:
            # Горизонтальная пара
            nj = (j + 1) % len(self.cols)
            if self.kmap[self.rows[i]][self.cols[nj]] == target_value and (i,nj) not in visited:
                return [(i,j), (i,nj)]
            
            # Вертикальная пара
            ni = (i + 1) % len(self.rows)
            if self.kmap[self.rows[ni]][self.cols[j]] == target_value and (ni,j) not in visited:
                return [(i,j), (ni,j)]
            
            return None
        
        else:  # size == 1
            return [(i,j)]
    
    def group_to_term(self, group, is_sknf):
        """Преобразует группу в логическое выражение"""
        terms = []
        
        for var_idx, var in enumerate(self.variables):
            values = set()
            for ri, ci in group:
                address = self.rows[ri] + self.cols[ci]
                values.add(address[var_idx])
            
            if len(values) == 1:
                val = values.pop()
                if is_sknf:
                    terms.append(f'!{var}' if val == '0' else var)
                else:
                    terms.append(var if val == '1' else f'!{var}')
        
        return '|'.join(terms) if is_sknf else '&'.join(terms)
    
    def print_groups(self, is_sknf):
        """Выводит найденные группы"""
        print("\nНайденные группы:")
        for i, group in enumerate(self.groups):
            term = self.group_to_term(group, is_sknf)
            print(f"Группа {i+1}: {'СКНФ' if is_sknf else 'СДНФ'} = ({term})")
            coords = [f"{self.rows[ri]}{self.cols[ci]}" for ri, ci in group]
            print(f"    Ячейки: {', '.join(coords)}")

class SDNFKarnaugh(KarnaughMap):
    def __init__(self, variables):
        super().__init__(variables)
    
    def fill_from_expression(self, sdnf_expr):
        """Заполняет карту для СДНФ"""
        terms = [t.strip('() ') for t in sdnf_expr.replace(' ', '').split('|')]
        
        for term in terms:
            mask = {}
            for var in self.variables:
                if f'!{var}' in term:
                    mask[var] = '0'
                elif var in term:
                    mask[var] = '1'
                else:
                    mask[var] = '-'
            
            for row in self.rows:
                for col in self.cols:
                    address = row + col
                    match = True
                    for i, var in enumerate(self.variables):
                        if mask[var] != '-' and mask[var] != address[i]:
                            match = False
                            break
                    if match:
                        self.kmap[row][col] = 1
    
    def minimize(self, expression):
        """Минимизирует СДНФ"""
        print("\n" + "="*60)
        print("Минимизация СДНФ методом Карно:")
        print(f"Исходное выражение: {expression}")
        
        self.setup_map()
        self.fill_from_expression(expression)
        self.print_map()
        
        self.find_groups(1)  # Ищем группы единиц для СДНФ
        self.print_groups(is_sknf=False)
        
        minimized_terms = []
        for group in self.groups:
            term = self.group_to_term(group, is_sknf=False)
            minimized_terms.append(f"({term})")
        
        minimized = " | ".join(minimized_terms)
        print(f"\nРезультат минимизации: {minimized}")
        return minimized

class SKNFKarnaugh(KarnaughMap):
    def __init__(self, variables):
        super().__init__(variables)
    
    def fill_from_expression(self, sknf_expr):
        """Заполняет карту для СКНФ"""
        terms = [t.strip('() ') for t in sknf_expr.replace(' ', '').split('&')]
        
        # Инициализируем все ячейки как 1
        for row in self.rows:
            for col in self.cols:
                self.kmap[row][col] = 1
        
        for term in terms:
            mask = {}
            for var in self.variables:
                if f'!{var}' in term:
                    mask[var] = '0'
                elif var in term:
                    mask[var] = '1'
                else:
                    mask[var] = '-'
            
            for row in self.rows:
                for col in self.cols:
                    address = row + col
                    match = True
                    for i, var in enumerate(self.variables):
                        if mask[var] != '-' and mask[var] != address[i]:
                            match = False
                            break
                    if match:
                        self.kmap[row][col] = 0
    
    def minimize(self, expression):
        """Минимизирует СКНФ"""
        print("\n" + "="*60)
        print("Минимизация СКНФ методом Карно:")
        print(f"Исходное выражение: {expression}")
        
        self.setup_map()
        self.fill_from_expression(expression)
        self.print_map()
        
        self.find_groups(0)  # Ищем группы нулей для СКНФ
        self.print_groups(is_sknf=True)
        
        minimized_terms = []
        for group in self.groups:
            term = self.group_to_term(group, is_sknf=True)
            minimized_terms.append(f"({term})")
        
        minimized = " & ".join(minimized_terms)
        print(f"\nРезультат минимизации: {minimized}")
        return minimized

# Пример использования для СДНФ
sdnf_expr = "(!a&!b&c) | (!a&b&!c) | (!a&b&c) | (a&!b&!c) | (a&!b&c) | (a&b&!c)"
variables = ['a', 'b', 'c']
sdnf_minimizer = SDNFKarnaugh(variables)
sdnf_minimizer.minimize(sdnf_expr)

# Пример использования для СКНФ
sknf_expr = "(a|b|!c) & (a|!b|c) & (!a|b|c) & (!a|b|!c) & (!a|!b|c)"
sknf_minimizer = SKNFKarnaugh(variables)
sknf_minimizer.minimize(sknf_expr)