symbol = ['a', 'b', 'c', 'd', 'e']
operand = ['&', '|', '!', '>', '~']
stroka = ""
expression = input("Введите выражение: ")

perem = []
for i in expression:
    if i in symbol and not i in perem:
        perem.append(i)


def priority(op):
    if op in ['!']:
        return 3
    elif op in ['&', '|']:
        return 2
    elif op in ['>', '~']:
        return 1
    return 0

def postr_opz(expression):
    stack = []
    res = ""
    for i in expression:
        if i in symbol: 
            res += i
        elif i == '(':  
            stack.append(i)
        elif i == ')':  
            while stack and stack[-1] != '(':
                res += stack.pop()
            stack.pop()  
        else:  
            while stack and priority(stack[-1]) >= priority(i):
                res += stack.pop()
            stack.append(i)
    while stack:  
        res += stack.pop()
    #print(res)
    return res

def tabl_nachalnie_operanty():
    tabl = {}
    index = 2**len(perem)
    for symbol in perem:

        tabl[symbol] = []
        for i in range(2**len(perem)):
            if i % index < index / 2:
                tabl[symbol].append(0) 
            else:
                tabl[symbol].append(1) 
        index /= 2
    return tabl

tabl_ist = tabl_nachalnie_operanty()



def evaluate_submodule(operand1, operand2, sign):
    if sign == '!':
        result = 1 - operand1
    if sign == '&':
            result = operand1 and operand2
    elif sign == '|':
            result = operand1 or operand2
    elif sign == '>':
        result = (not operand1) or operand2
    elif sign == '~':
        result = operand1 == operand2

    if result:
        return 1
    return 0



def postr_tabl(stroka):
    stack = []
    sub_str = ""
    for symb in stroka:
        if symb in symbol:
            stack.append(symb)
        elif symb == '!':
            tabl_ist['!' + stack[-1]] = []
            for i in range(2**len(perem)):
                tabl_ist['!' + stack[-1]].append(evaluate_submodule(tabl_ist[stack[-1]][i], i, '!'))
            stack.append('!' + stack.pop())           
        elif symb in operand:
            sub_str = '(' + stack[-2] + symb + stack[-1] + ')'
            tabl_ist[sub_str] = []
            for i in range(2**len(perem)):
                tabl_ist[sub_str].append(evaluate_submodule(tabl_ist[stack[-2]][i], tabl_ist[stack[-1]][i], symb))
            stack.pop()
            stack.pop()
            stack.append(sub_str)
    return sub_str
    #print(tabl_ist)


def print_truth_table():
    variables = [key for key in tabl_ist.keys() if len(key) == 1]  # Переменные — это ключи длиной 1
    expressions = [key for key in tabl_ist.keys() if len(key) > 1]  # Подвыражения — это ключи длиной больше 1

    # Определяем ширину столбцов
    column_widths = {}
    for key in variables + expressions:
        # Ширина столбца равна максимальной длине ключа или значения
        max_value_length = max(len(str(val)) for val in tabl_ist[key])
        column_widths[key] = max(len(key), max_value_length)

    header = []
    for key in variables + expressions:
        header.append(key.ljust(column_widths[key]))
    print(" | ".join(header))
    separator = []
    for key in variables + expressions:
        separator.append("-" * column_widths[key])
    print("-+-".join(separator))

    num_rows = len(tabl_ist[variables[0]])

    # Вывод строк таблицы
    for i in range(num_rows):
        row = []
        for key in variables + expressions:
            # Выравниваем значение по ширине столбца
            row.append(str(tabl_ist[key][i]).ljust(column_widths[key]))
        print(" | ".join(row))


def build_scnf_sdnf(result_key):
    # Извлекаем переменные из ключей словаря
    variables = [key for key in tabl_ist.keys() if len(key) == 1]  # Переменные — это ключи длиной 1

    sdnf_terms = []  # Термы для СДНФ
    scnf_terms = []  # Термы для СКНФ

    num_rows = len(tabl_ist[result_key])

    for i in range(num_rows):
        if tabl_ist[result_key][i] == 1:
            # Строим терм для СДНФ
            term = []
            for var in variables:
                if tabl_ist[var][i] == 1:
                    term.append(var)
                else:
                    term.append(f"!{var}")
            sdnf_terms.append(" & ".join(term))
        else:
            # Строим терм для СКНФ
            term = []
            for var in variables:
                if tabl_ist[var][i] == 0:
                    term.append(var)
                else:
                    term.append(f"!{var}")
            scnf_terms.append(" | ".join(term))

    # Собираем СДНФ и СКНФ
    sdnf = " | ".join(f"({term})" for term in sdnf_terms)
    scnf = " & ".join(f"({term})" for term in scnf_terms)

    return scnf, sdnf

def convert_from_binary(result_key):
    return sum(2**i * bit for i, bit in enumerate(reversed(tabl_ist[result_key])))

res = postr_opz(expression)
sub_str = postr_tabl(res)
print_truth_table()

scnf, sdnf = build_scnf_sdnf(sub_str)

# Вывод СКНФ и СДНФ
print("СКНФ:", scnf)
print("СДНФ:", sdnf)
print("\nЧисло из двоичного кода:", convert_from_binary(sub_str))
