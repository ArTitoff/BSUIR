#   Лабораторная работа №1 по дисциплине МРЗвИС
#   Задача: реализовать и исследовать модель решения на конвейерной архитектуре задачи
#   вычисления попарного произведения компонентов двух векторов чисел             
#   Вариант: 7. алгоритм вычисления произведения пары 6-разрядных чисел 
#   умножением с младших разрядов со cдвигом множимого влево 
#      
#   Автор: Титов А. В. (321703)
#
#   Используемые источники: https://libeldoc.bsuir.by/handle/123456789/42611



def procces(bit_index: int, multiplier: bytes, multiplicand: bytes, product: bytes):
    if (multiplier >> bit_index) & 1:
        product = binary_summ(multiplicand, product)

    multiplicand = multiplicand << 1

    return multiplicand, product


def binary_summ(multiplicand: bytes, product: bytes):
    result = 0
    carry = 0
    for bit_index in range(p * 2):
        a_bit = (product >> bit_index) & 1
        b_bit = (multiplicand >> bit_index) & 1

        sum = a_bit ^ b_bit ^ carry
        carry = (a_bit & b_bit) | (a_bit & carry) | (carry & b_bit)

        if sum:
            result = result | 1 << bit_index
    
    return result


m = int(input("Введите количество пар чисел ")) # число входных векторов
p = 6 # разрядность множителей
product_results = [] 
conveyor_len = 6
conv_data = [None] * conveyor_len
m_er_i = 0 # multiplier_index
m_nd_i = 1 # multiplicand_index
pr_i = 2 # product_index


import os
import random
import copy


def print_conveyor(conv_data, tact_num):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Входные данные:\n{binary_pairs_str}")

    print_data = []
    for i, item in enumerate(conv_data):
        if item is not None:
            
            multiplier_bin = bin(item[0])[2:].zfill(6)  # Множитель 6 бит [2:] убирает '0b'
            multiplicand_bin = bin(item[1])[2:].zfill(12) # Множимое 12 бит (так как оно сдвигается)
            product_bin = bin(item[2])[2:].zfill(12) # Частичная сумма 12 бит

            print_data.append([
                f"Множитель: {multiplier_bin} ({item[0]})", 
                f"Множимое: {multiplicand_bin} ({item[1]})", 
                f"Частичная сумма: {product_bin} ({item[2]})",
                f"Частичное произведение: {multiplicand_bin}" if (multiplier >> i) & 1 \
                                                                else f"Частичное произведение: {bin(0b0)[2:].zfill(12)}"
                            ])
        else:
            print_data.append(None)
    print("\nКонвейер")
    print("====================================================================================================================================================")
    print(f"                                                    Такт {tact_num+1} ")
    print("====================================================================================================================================================\n")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------")
    for i, data in enumerate(print_data):
        print(f"Этап {i + 1}: {data}")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------")


def conveyor_stage(input_data: list, tact_num):
    for i in range(conveyor_len - 1, 0, -1):
        conv_data[i] = conv_data[i-1]

    conv_data[0] = input_data
 
    for i, data_unit in enumerate(conv_data):
        if data_unit is not None:
            conv_data[i][m_nd_i], conv_data[i][pr_i] = procces(i, conv_data[i][m_er_i], conv_data[i][m_nd_i], conv_data[i][pr_i])

    print_conveyor(conv_data, tact_num)

    if conv_data[-1] is not None:
        product = conv_data[-1][pr_i]
        return product
    
    return None
    

def process_all(inputs):
        results = []
        m = len(inputs)
        
        total_tacts = conveyor_len + m - 1
        tact_num = 0
        for tact in range(total_tacts):
            if tact < m:
                result = conveyor_stage(inputs[tact], tact_num)
            else:
                result = conveyor_stage(None, tact_num)
            
            tact_num = tact_num + 1
            if result is not None:
                results.append(f"Результат на этапе {tact_num}: {result}")
            print(f"\nРезультат: {results}")
            input()
        return results


def parse_input_to_binary(string_num):
    if len(string_num) > 6:
        raise ValueError("Неправильная разрядность")

    num = 0 
    for i, char in enumerate(reversed(string_num)):
        if char != '1' and char != '0':
            raise ValueError("Неправильный ввод числа")
        if char == '1':
            num = num + 2**i
    return num


binary_pairs = []

for i in range(m):
    print(f"Пара {i+1}:")
    multiplier = input("Введите множитель ")
    multiplicand = input("Введите множимое ")
    multiplier = parse_input_to_binary(multiplier)
    multiplicand = parse_input_to_binary(multiplicand)

    binary_pairs.append([multiplier, multiplicand, 0])


binary_pairs_str = "\n".join(f"Пара {i+1}: Множитель: {pair[0]}, Множимое: {pair[1]}  (bin: {bin(pair[0])[2:].zfill(6)}, {bin(pair[1])[2:].zfill(6)})" \
                             for i, pair in enumerate(binary_pairs))


print(f"\nВходные данные:\n{binary_pairs_str}\n\nНажмите Enter для продолжения")


input()
product_results = process_all(binary_pairs)


print(f"К =  {(m * conveyor_len) / (conveyor_len + m - 1)}")
