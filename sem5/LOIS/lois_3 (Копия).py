#   Лабораторная работа №2 по дисциплине ЛОИС
#   Задача: реализовать обратный нечеткий логический вывод             
#   Вариант: 3. Реализовать обратный нечеткий логический вывод на основе 
#   операции нечёткой композиции (max({max{0}U{xi+yi-1})/i})      
#   Авторы: Титов А. В. (321703)
#   Авторы: Головач В. Д. (321703)                                                   
#   Авторы: Остров М. А. (321703) 
#   Дата: 24.11.2025
#
#   Используемые источники: https://github.com/rastsislaux
#   Используемые источники: https://clck.ru/3QU9ss


import copy
from decimal import Decimal
import re


# парсер файла
def parse_dataset(path: str):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]

    # убираем пустые строки
    lines = [l for l in lines if l]

    # первая непустая строка: заголовок y
    y_header = re.split(r"\s+", lines[0])

    # вторая: сами значения y
    y_vals_str = re.split(r"\s+", lines[1])
    y = [float(v) for v in y_vals_str]

    # после этого: заголовок X
    x_header = re.split(r"\s+", lines[2])

    # дальше идут строки матрицы X
    x = []
    for line in lines[3:]:
        nums = re.split(r"\s+", line)
        x.append([float(v) for v in nums])

    # проверки
    # 1) размеры совпадают: элементов y столько же, сколько строк X
    if len(y) != len(x):
        raise ValueError(f"len(y)={len(y)} не совпадает со строками X={len(x)}")

    # 2) все строки X должны иметь одинаковую длину
    row_len = len(x[0])
    for row in x:
        if len(row) != row_len:
            raise ValueError("Строки X имеют разное количество элементов")

    # 3) заголовков X столько же, сколько столбцов
    # if len(x_header) != row_len:
    #     raise ValueError("Заголовки X не совпадают по количеству со столбцами")

    # можно проверить и заголовки y
    if len(y_header) != len(y):
        raise ValueError("Заголовки y не совпадают по количеству со значениями y")

    return y, x


# логика обратного нечеткого вывода

def recalculate_matrix(res : list[float], matrix: list[list[float]])-> list[list[float]]: # рассчитывваем верхние границы
    new_matrix = copy.deepcopy(matrix)
    for  i, string in enumerate(new_matrix):
        for  j, _ in enumerate(string):
            #new_matrix[i][j] = res[i] + 1 - matrix[i][j]
            #строчка с точными значениями
            new_matrix[i][j] = float(Decimal(str(res[i])) + Decimal('1') - Decimal(str(matrix[i][j])))
    return new_matrix


def create_new_string(string: list[float], j : int)->list[list[int, float]]:
    new_string = []
    for i, variable in enumerate(string):
        if i == j:
            new_string.append([1, variable])
        else:
            new_string.append([0, variable])
    return new_string


def translate_to_tree_solution(new_matrix: list[list[float]])->list[list[list[list[int, float]]]]:
    tree_solution = []
    for string in new_matrix:
        one_layer_branch_solution = []
        for  j, _ in enumerate(string):
            temp = create_new_string(string, j)
            one_layer_branch_solution.append(temp)
        tree_solution.append(one_layer_branch_solution)
    return tree_solution


def check_appropriate_solution(index: int, solution: list[list[int, float]], preliminary_solution: list[list[list[int, float]]])->bool: # тут проверяем все случаи, когда не надо отбрасывать ветку решений
    return (solution[0] == 1 and preliminary_solution[index][0] == 1 and solution[1] == preliminary_solution[index][1]) \
                or (solution[0] == 0 and preliminary_solution[index][0] == 1 and solution[1] >= preliminary_solution[index][1]) \
                or (solution[0] == 1 and preliminary_solution[index][0] == 0 and solution[1] <= preliminary_solution[index][1]) \
                or (solution[0] == 0 and preliminary_solution[index][0] == 0)


def calculate_new_preliminary_solution(preliminary_solution: list[list[list[int, float]]], solution: list[list[list[int, float]]]):
    new_preliminary_solution = copy.deepcopy(preliminary_solution)
    for i, prel_sol in enumerate(new_preliminary_solution):
        if prel_sol[0] == 0 and solution[i][0] == 0:
            prel_sol[1] = min(prel_sol[1], solution[i][1])
        elif solution[i][0] == 1 and prel_sol[0] == 0:
            prel_sol[1] = solution[i][1]
            prel_sol[0] = solution[i][0]
    return new_preliminary_solution


def recursive_search_for_solutions(tree_solution: list[list[list[list[int, float]]]], deep_index: int, preliminary_solution: list[list[list[int, float]]])->list[list[int, float]]:
    final_result = []
    for solutions in tree_solution[deep_index]:
        appropriate_solution = True
        for i, solution in enumerate(solutions):
            appropriate = check_appropriate_solution(i, solution, preliminary_solution)
            if not appropriate: # если не прошли проверкутдля подходящей ветки
                appropriate_solution = False 
                break
        if deep_index + 1 < len(tree_solution): # проверяем находимся мы на последнем слое дерева или нет
            if appropriate_solution:
                new_preliminary_solution = calculate_new_preliminary_solution(preliminary_solution, solutions)
                result = recursive_search_for_solutions(tree_solution, deep_index + 1, new_preliminary_solution)
                for res in result:
                    final_result.append(res)
        else:
            if appropriate_solution:
                new_preliminary_solution = calculate_new_preliminary_solution(preliminary_solution, solutions)
                final_result.append(new_preliminary_solution) 

    return final_result


def reverse_fuzzy_inference(tree_solution: list[list[list[list[int, float]]]])->list[list[list[int, float]]]:
    solution_result = []
    for solution in tree_solution[0]:   # тут перебираются корневые решения, от которых начинаются все остальные и запускается рекурсивная функция
        result = recursive_search_for_solutions(tree_solution, 1, solution)   # передаю soultion как параметр, по которому будет сравниватся другая часть и меняться последующее решение
        for res in result:
            solution_result.append(res)

    return solution_result



def is_solution_included_in_another_solution(sol_1, sol_2) -> bool:
    """
    Проверяет, содержится ли решение sol_1 в решении sol_2.
    sol_1 содержится в sol_2, если для каждой координаты i:
        - если sol_1[i] точечное (index=1), то sol_2[i] либо точечное с тем же значением,
          либо интервальное с верхней границей >= этому значению;
        - если sol_1[i] интервальное (index=0), то sol_2[i] либо интервальное с верхней границей >=,
          либо точечное, лежащее внутри интервала sol_1[i] (но это возможно только если интервал вырожден).
    В нашей модели интервал всегда 0 <= A(x) <= value.
    """
    for i in range(len(sol_1)):
        t1, v1 = sol_1[i]  # тип и значение из sol_1
        t2, v2 = sol_2[i]  # тип и значение из sol_2

        if t1 == 1:  # точечное в sol_1
            if t2 == 1:  # точечное в sol_2
                if v1 != v2:
                    return False
            else:  # t2 == 0, интервал в sol_2
                # v2 — верхняя граница интервала
                if v1 > v2:
                    return False
                # если v1 <= v2, то условие выполнено
        else:  # t1 == 0, интервал в sol_1
            if t2 == 1:  # точечное в sol_2
                # интервал [0, v1] содержит точку v2?
                # только если v2 == v1 и v1 == 0? Нет, если v2 <= v1.
                # Но у нас интервал в sol_1, а точечное в sol_2.
                # sol_1 содержится в sol_2 только если весь интервал [0, v1] лежит в {v2},
                # т.е. только если v1 == v2 == 0 (вырожденный интервал).
                if v1 != v2 or v1 != 0.0:
                    return False
            else:  # t2 == 0, оба интервала
                # интервал [0, v1] содержится в [0, v2]?
                if v1 > v2:
                    return False
                # нижняя граница 0 общая, поэтому проверяем только верхнюю
    return True


def normalize_index_and_value(pre_normalized_solution):
    normalized_solution = []
    for solution in pre_normalized_solution:
        appropriate_solution = True
        for i in range(len(solution)):
            index, value = solution[i]
            if index == 0 and value == 0:  # [0, 0] → [1, 0.0]
                solution[i] = [1, 0.0]
            elif index == 0 and value >= 1:
                solution[i] = [0, 1.0]
            elif index == 0 and value < 0:
                appropriate_solution = False
                break
            elif index == 1 and not 0.0 <= value <= 1.0:
                appropriate_solution = False
                break
        if appropriate_solution:
            normalized_solution.append(solution)
    return normalized_solution


def normalize_solution(solutions) -> list[list[list[int, float]]]:
    pre_normalized = []
    n = len(solutions)
    for i in range(n):
        is_included = False
        for j in range(n):
            if i == j:
                continue
            if is_solution_included_in_another_solution(solutions[i], solutions[j]):
                is_included = True
                break
        if not is_included and solutions[i] not in pre_normalized:
            pre_normalized.append(solutions[i])

    return normalize_index_and_value(pre_normalized)

def create_disjunct(data: list[list[int]]) -> str:
    expressions = []
    for i, (flag, value) in enumerate(data, 1):
        if flag == 1:
            expressions.append(f"(A(x{i}) = {value})")
        else:
            expressions.append(f"(0 <= A(x{i}) <= {value})")
    
    result = expressions[0]
    for expr in expressions[1:]:
        result = f"({result}/\\{expr})"
    
    return result


def transform_to_dnf(answers_list):
    if not answers_list:
        return "Решений не найдено"
    disjuncts = list(map(create_disjunct, answers_list))

    result = disjuncts[0]
    for dis in disjuncts[1:]:
        result = f"({result}\\/{dis})"
    
    return result


def main():
    y, matrix = parse_dataset("/home/artem/Рабочий стол/BSUIR/LOIS/input.txt")

    new_matrix = recalculate_matrix(y, matrix)
    #print(new_matrix)

    tree_solution = translate_to_tree_solution(new_matrix)
    #print(tree_solution)

    result_solutions = reverse_fuzzy_inference(tree_solution)
    #print(result_solutions)


    normalized_solutions = normalize_solution(result_solutions)
    #print(normalized_solutions)
    print(
    transform_to_dnf(
        normalized_solutions
    )
)

if __name__ == "__main__":
    main()
























# test = [[1.0, 0.2], [0.7, 0.2]]
# res = [0.3, 0.3]

# test = [[0.8, 0.4, 0.6], [0.6, 0.7, 0.5], [0.5, 0.3, 0.8]]
# res = [0.3, 0.2, 0.4]

# test = [[0.7, 0.6], [0.5, 0.8]]
# res = [0.4, 0.3]

# test = [[0.6, 0.4, 0.7], [0.5, 0.8, 0.4], [0.7, 0.3, 0.6]]
# res = [0.4, 0.3, 0.5]

# нет решений
# test = [[0.6, 0.8, 0.4, 0.7], [0.7, 0.5, 0.6, 0.4], [0.5, 0.6, 0.8, 0.3], [0.4, 0.7, 0.5, 0.6]]
# res = [0.3, 0.4, 0.2, 0.5]

# test = [[0.7, 0.6, 0.5, 0.8], [0.6, 0.7, 0.8, 0.5], [0.5, 0.8, 0.6, 0.7], [0.8, 0.5, 0.7, 0.6]]
# res = [0.2, 0.3, 0.4, 0.3]