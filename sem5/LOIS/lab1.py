#   Лабораторная работа №3 по дисциплине ЛОИС
#   Задача: реализовать прямой нечеткий логический вывод             
#   Вариант: 3. Реализовать прямой нечеткий логический вывод, используя 
#   треугольную норму граничного произведения и нечеткую импликацию Лукасевича     
#   Авторы: Титов А. В. (321703) 
#   Авторы: Головач В. Д. (321703)                                                   
#   Авторы: Остров М. А. (321703)  
#   
#   Используемые источники: https://github.com/rastsislaux

def list_to_matrix(data_list):
    """
    Преобразует список кортежей (row, col, value) в именованную матрицу
    
    Parameters:
        data_list: list of tuples в формате [(row, col, value), ...]
    
    Returns:
        pandas DataFrame с именованными строками и столбцами
    """
    import pandas as pd
    
    # Извлекаем уникальные имена строк и столбцов
    rows = sorted(set(item[0] for item in data_list))
    cols = sorted(set(item[1] for item in data_list))
    
    # Создаем пустую матрицу
    matrix = pd.DataFrame(0.0, index=rows, columns=cols)
    
    # Заполняем матрицу значениями
    for row, col, value in data_list:
        matrix.loc[row, col] = value
    
    return matrix

def implication(set1, set2): 
    result = []
    for a in set1:
        for b in set2:
            impl_result = (a[0], b[0], 1 if a[1] <= b[1] else 1 - a[1] + b[1])
            result.append(impl_result)
    return result


def composition(set1, impl_matrix): 
    result = {}
    kompos_matrix = []
    for a in set1:
        for m in impl_matrix:
            if a[0] == m[0]:
                komp_res = (a[0], m[1], max(0, a[1] + m[2] - 1))
                kompos_matrix.append(komp_res)
            
    for _, second, max_third in kompos_matrix:
        if second not in result.keys() or result[second] < max_third:
            result[second] = max_third

    return list(result.items())

def inference(set1, set2, set3):
    impl_matrix = implication(set1, set2)
    #matrix = list_to_matrix(impl_matrix)
    #print(matrix)
    result = composition(set3, impl_matrix)
    return result


def suitable_sets(set1, sets: dict):
    results = {}
    
    def get_variables(set):
        return {s[0] for s in set} 
    
    reference_set = get_variables(set1)
    
    for set_name, set in sets.items():
        candidate_for_set = get_variables(set)
        if candidate_for_set == reference_set:  
            results[set_name] = set
    
    return results


def set_to_str(set):
    pairs = []
    for pair in set:
        pairs.append(f"<{pair[0]}, {pair[1]}>")
    return "{" + ",".join(pairs) + "}"

            

def fuzzy_derivation(rules, sets: dict):
    old_len = -1
    new_len = 0
    result = []
    visited_sets = []

    while (new_len != old_len):
        old_len = len(sets)
        for rule in rules:
            set1 = sets[rule[0]]
            set2 = sets[rule[1]]
            inference_sets = suitable_sets(set1, sets)
            #print(inference_sets)
            #print("="*50)
            for set_name, inf_set in inference_sets.items():
                new_name = "_" + str((len(result) + 1))
                new_set = inference(set1, set2, inf_set)               
                new_str = f"{{{set_name}, {rule[0]}(x)~>{rule[1]}(y)}} |~ {new_name} = {set_to_str(new_set)}"    
               # print(new_str)               
                if new_set in sets.values() and new_set not in visited_sets:
                    result.append(new_str)
                    visited_sets.append(new_set)
                    continue
                if new_set not in sets.values():
                    result.append(new_str)
                    sets[new_name] = new_set
                    visited_sets.append(new_set)
        new_len = len(sets)
    
    return "\n".join(result)


def round_numbers_in_string(text, decimals=10):
    def round_match(match):
        number = float(match.group())
        return str(round(number, decimals))
    
    return re.sub(r'\d+\.\d+', round_match, text)
    

import re


def parse_fuzzy_data(filename):
    """Улучшенная версия с валидацией и удалением дубликатов"""
    sets_dict = {}
    rules_list = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    set_pattern = r'(\w+)\s*=\s*\{([^}]+)\}'
    element_pattern = r'<([^,]+),\s*([\d.]+)>'
    
    for match in re.finditer(set_pattern, content):
        set_name = match.group(1)
        set_content = match.group(2)
        
        # Используем словарь для автоматического удаления дубликатов
        unique_elements = {}
        
        for elem_match in re.finditer(element_pattern, set_content):
            var_name = elem_match.group(1).strip()
            value = float(elem_match.group(2))
            
            if value < 0 or value > 1:
                print(f"ПРЕДУПРЕЖДЕНИЕ: Исправлено значение {value} для '{var_name}' в множестве '{set_name}'")
                value = max(0, min(1, value))
            
            unique_elements[var_name] = value
        
        sets_dict[set_name] = [(name, value) for name, value in unique_elements.items()]
    
    rule_pattern = r'(\w+)\(?[^)]*\)?\s*~>\s*(\w+)\(?[^)]*\)?'
    for match in re.finditer(rule_pattern, content):
        rule_from = match.group(1)
        rule_to = match.group(2)
        rules_list.append((rule_from, rule_to))
    
    return sets_dict, rules_list


if __name__ == "__main__":

    sets, rules = parse_fuzzy_data('fuzzy_input.txt')
    result = fuzzy_derivation(rules, sets)
    print(round_numbers_in_string(result))



    


















    
###########  ТЕСТЫ ПРОГРАММЫ   ###################
# rules = [('A','B'), ('A','C')]
# sets = {'A' : [('x1', 0.1), ('x2', 0.7)], 'B': [('y1', 0.3), ('y2', 0.4)], 'C':  [('x1', 0.6), ('x2', 0.2)]}

# print(fuzzy_derivation(rules, sets))

