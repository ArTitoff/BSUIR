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

   
    # можно проверить и заголовки y
    if len(y_header) != len(y):
        raise ValueError("Заголовки y не совпадают по количеству со значениями y")

    return y, x


# логика обратного нечеткого вывода

def recalculate_matrix(res : list[float], matrix: list[list[float]])-> list[list[float]]: # рассчитывваем верхние границы
    new_matrix = copy.deepcopy(matrix)
    for  i, string in enumerate(new_matrix):
        for  j, _ in enumerate(string):
            if res[i] == 0 and new_matrix[i][j] == 0:
                new_matrix[i][j] = 1
            elif matrix[i][j] == 0:
                return [[False]]
            else:
                new_matrix[i][j] = res[i] / matrix[i][j]
                #строчка с точными значениями
                #new_matrix[i][j] = float(Decimal(str(res[i])) / Decimal(str(matrix[i][j])))
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
            if len(string) == 1:
                return [[[[1, string[0]]], [[0, string[0]]]]]
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
        result = recursive_search_for_solutions(tree_solution, 0, solution)   # передаю soultion как параметр, по которому будет сравниватся другая часть и меняться последующее решение
        for res in result:
            solution_result.append(res)

    return solution_result



# часть с фильтрацией ответа
from typing import Literal


class SolutionItem:
    def __init__(self, index: Literal[0, 1], value: float):
        index, value = self.__normalize_index_and_value(index, value)
        self.index = index
        self.value = value

    def __ge__(self, other) -> bool:
        if not isinstance(other, SolutionItem):
            raise ValueError("Other object must be a SolutionItem class")

        other: SolutionItem

        greater = self.index == 0 and self.value >= other.value
        equal = self.index == 1 and other.index == 1 and self.value == other.value

        return greater or equal

    def __eq__(self, other):
        if not isinstance(other, SolutionItem):
            raise ValueError("Other object must be a SolutionItem class")

        other: SolutionItem

        return self.index == other.index and self.value == other.value

    @staticmethod
    def __normalize_index_and_value(index, value) -> tuple[int, float]:
        if index == 0 and value == 0: # Замена х1 <= 0 на х1 = 0
            return 1, 0.0
        elif index == 0 and value >= 1:
            return 0, 1.0
        elif index == 0 and value < 0:
            raise ValueError("Upper limit of the interval must be greater than or equal to 0.0")
        elif index == 1 and not 0.0 <= value <= 1.0:
            raise ValueError("Fixed value must be in the range from 0.0 to 1.0")

        return index, value

    def __repr__(self):
        return f"[{self.index}, {self.value}]"


class Solution:
    def __init__(self, value: list[list[int, float]]):
        self.value: list[SolutionItem] = self.__transform_solution(value)

    @staticmethod
    def __transform_solution(solution_value: list[list[int, float]]) -> list[SolutionItem]:
        normalized_solution_value = []

        for index, value in solution_value:
            solution_item = SolutionItem(index, value)
            normalized_solution_value.append(solution_item)

        return normalized_solution_value

    def __ge__(self, other):
        if not isinstance(other, Solution):
            raise ValueError("Other object must be a Solution class")

        other: Solution

        for self_item, other_item in zip(self.value, other.value):

            if not self_item >= other_item:
                return False

        return True

    def __eq__(self, other):
        if not isinstance(other, Solution):
            raise ValueError("Other object must be a Solution class")

        other: Solution

        for self_item, other_item in zip(self.value, other.value):
            if self_item != other_item:
                return False

        return True

    def __repr__(self):
        solution_items_str = ', '.join([str(solution_item) for solution_item in self.value])

        return f"[{solution_items_str}]"
    
    def get_value(self) -> list[list[int, float]]:
        return [[item.index, item.value] for item in self.value]


def normalize_solutions(solutions_values: list[list[list[int, float]]]):
    solutions: list[Solution] = []
    normalized_solutions: list[list[list[int, float]]] = []

    for solution_value in solutions_values:
        try:
            solution = Solution(solution_value)
        except ValueError:
            continue

        if solution in solutions:
            continue

        solutions.append(solution)

    solutions = deduplicate_solutions(solutions)

    for solution in solutions:
        if is_solution_inluded_in_another_solution(solution, solutions):
            continue

        normalized_solutions.append(solution.get_value())

    return normalized_solutions


def is_solution_inluded_in_another_solution(solution: Solution, solutions: list[Solution]):
    for other_solution in solutions:
        if other_solution is solution:
            continue

        if other_solution >= solution:
            return True

    return False


def deduplicate_solutions(solutions: list[Solution]) -> list[Solution]:
    deduplicated_solutions = []

    for solution in solutions:
        if is_dublicate_solution(solution, deduplicated_solutions):
            continue

        deduplicated_solutions.append(solution)

    return deduplicated_solutions


def is_dublicate_solution(solution: Solution, solutions: list[Solution]):
    for other_solution in solutions:
        if other_solution is solution:
            continue

        if other_solution == solution:
            return True

    return False


# оформление вывода
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


def round_numbers_in_string(text, decimals=10):
    def round_match(match):
        number = float(match.group())
        return str(round(number, decimals))
    
    return re.sub(r'\d+\.\d+', round_match, text)


def main():
    y, matrix = parse_dataset("/home/artem/Рабочий стол/BSUIR/LOIS/input.txt")
    new_matrix = recalculate_matrix(y, matrix)

    if new_matrix == [[False]]:
        print("Решений нет")
    else:
        #print(new_matrix)

        tree_solution = translate_to_tree_solution(new_matrix)
        #print(tree_solution)

        result_solutions = reverse_fuzzy_inference(tree_solution)
        #print(result_solutions)

        normalized_solutions = normalize_solutions(result_solutions)
        #print(normalized_solutions)
        normalized_solutions = list(normalized_solutions)
        print(
            round_numbers_in_string(transform_to_dnf(
                normalized_solutions
            ))
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



 # 3) заголовков X столько же, сколько столбцов
    # if len(x_header) != row_len:
    #     raise ValueError("Заголовки X не совпадают по количеству со столбцами")
