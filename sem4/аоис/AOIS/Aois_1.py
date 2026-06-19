def convert_to_10_exp(num_10: list):
    num = 0
    length = len(num_10)

    for index, binary in enumerate(num_10):
        num += 2 ** (length - 1 - index) * binary
    
    return num

def convert_to_10_mant(mant: list):
    num = 0
    for index, binary in enumerate(mant):
        num += 2 ** (-1 - index) * binary
    
    return num


def binary_to_float(binary):

    sign = binary[0]
    
    exponent = convert_to_10_exp(binary[1:9])
    exponent -= 127
    # Извлечение мантиссы
    mantissa = convert_to_10_mant(binary[9:32])

    # Вычисление конечного значения
    value = (1 + mantissa) * (2 ** exponent)
    
    # Применение знака
    if sign == 1:
        value = -value
    
    return value
    

def float_to_binary(number):
    binary = [0] * 32
    
    if number < 0:
        binary[0] = 1
        number = -number  
    else:
        binary[0] = 0

    exponent = 0

    # Приведение к нормализованной форме
    while number >= 2.0:
        number /= 2.0
        exponent += 1

    while number < 1.0 and number > 0:
        number *= 2.0
        exponent -= 1

    # Нормализация: number теперь в диапазоне [1, 2)
    number -= 1.0  # Убираем 1 перед двоичной точкой

    exponent += 127 

    exp = conv_exp(exponent)
    for i in range(8):
        binary[1 + i] = exp[i] 

    # Преобразование в мантиссу
    for i in range(23):
        number *= 2
        if number >= 1.0:
            binary[9 + i] = 1
            number -= 1.0
        else:
            binary[9 + i] = 0

    return binary

def conv_exp(num: int):
    num = abs(num)
    exp = 0
    binary_representation = []

    while 2 ** exp <= num:
        exp += 1
    
    while exp != 0:
        exp -= 1
        if (num - 2 ** exp) >= 0:
            binary_representation.append(1)
            num = num - 2 ** exp
        else: 
            binary_representation.append(0)

    if len(binary_representation) > 8:
        raise ValueError("Значение слишком большое и не помещается в 8 формат")
    
    while len(binary_representation) < 8:
        binary_representation.insert(1, 0)
        
    return binary_representation   

def print_binary(binary):
    print("".join(map(str, binary)))


def sum_of_EEEI(num1: list, num2: list):
    result = []

    if num1[1:9] == num2[1:9]:
        diff = get_dop_binary(num1[1:9])
        result = result + diff
        num1.insert(9, 0)
        num1.pop()
        num2.insert(9, 0)
        num2.pop()
    else:
        dif = difference_of_binaries([0] + num1[1:9], [0] + num2[1:9])
        sign = dif[0]
        del dif[0]
   
        exp = convert_to_10_exp(dif)
        if sign == 0:
            result = result + num1[1:9]
            num2.insert(9, 1)
            num2.pop()
            for i in range(exp-1):
                num2.insert(9, 0)
                num2.pop()
        else:
            result = result + num2[1:9]
            num2.insert(9, 1)
            num2.pop()
            for i in range(exp-1):
                num1.insert(9, 0)  # Возможно, здесь должно быть num1 вместо num2
                # Проверяем, чтобы не было ошибки при удалении
                num1.pop()

    sum_result = sum_of_binaries([num1[0]] + num1[9:32], [num2[0]] + num2[9:32])
    result.insert(0, sum_result[0])
    result = result + sum_result[1:24]  # Исправлено на круглые скобки

    return result  # Не забудьте вернуть результат


def get_dop_binary_sum(num: list):  #1
    if num[0] == 1:
        obr_binary = [1 - bit for bit in num]
        obr_binary[0] = 1 - obr_binary[0]    
        dop_binary = get_dop_binary(obr_binary)
    else:
        dop_binary = num
        
    return dop_binary


def get_dop_binary(num: list):
    
    result = []
    carry = 1

    for i in range(len(num) - 1, -1, -1):
        temp = num[i] + carry
        res_bit = temp % 2
        carry = temp // 2
        result.insert(0, res_bit)

    return result


def sum_of_binaries(num1: list, num2: list):
    first_binary  = get_dop_binary_sum(num1)
    second_binary  = get_dop_binary_sum(num2)

    carry = 0
    result = []

    for i in range(len(first_binary) - 1, -1, -1):
        temp = first_binary[i] + second_binary[i] + carry
        res_bit = temp % 2
        carry = temp // 2
        result.insert(0, res_bit)

    if result[0] == 1:
        for i in range(1, len(result)):
            if result[i] == 1:
                result[i] = 0
            else:
                result[i] = 1 
        result = get_dop_binary(result)        

    return result    


def difference_of_binaries(first_binary: list, second_binary: list):
    inverted_second_binary = second_binary.copy()
    inverted_second_binary[0] = 1 - inverted_second_binary[0]
    return sum_of_binaries(first_binary, inverted_second_binary)

number = float(input("Введите число: "))
binary_representation = float_to_binary(number)
number2 = float(input("Введите число: "))
binary_representation2 = float_to_binary(number2)
print_binary(binary_representation)
float_value = binary_to_float(binary_representation)
print("Переведенное число:", float_value)

summa = sum_of_EEEI(binary_representation, binary_representation2)
float_value2 = binary_to_float(summa)
print("СУМММАА:", float_value2)
print(summa)