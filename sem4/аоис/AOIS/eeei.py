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
    
def convi_expo(exp :int):
    bin_expo = [0] * 8

    for i in range(8):
        if exp >= 2 ** (7 - i):
            bin_expo[i] = 1
            exp -= 2 ** (7 - i)

    return bin_expo

def conv_mantiss(mantis):
    num = mantis
    exp = 0
    binary_representation = []

    while 2 ** exp <= num:
        exp += 1
    
    while len(binary_representation) < 24:
        exp -= 1
        if (num - 2 ** exp) >= 0:
            binary_representation.append(1)
            num = num - 2 ** exp
        else: 
            binary_representation.append(0)

    del binary_representation[0]

    return binary_representation

def conv_to_eeei(num):
    sign = 0 if num >= 0 else 1
    num = abs(num)
    mantis = conv_mantiss(num)
    exp = 0
    binary = [sign]

    while num >= 1: 
        num /= 2
        exp += 1

    exponent = convi_expo(127 + exp - 1) 

    binary = binary + exponent + mantis

    return binary




def print_binary(binary):
    print("".join(map(str, binary)))




def sum_of_EEEI(num1: list, num2: list):
    result = []

    if num1[1:9] == num2[1:9]:
        result = result + num1[1:9]
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
            num1.insert(9, 1)
            num1.pop()
            for i in range(exp-1):
                num1.insert(9, 0)  
                num1.pop()


    print(num1)
    print(num2)
    sum_result, carry = sum_of_mantis([num1[0], 0] + num1[9:32], [num2[0], 0] + num2[9:32])
    if sum_result[1] == 1:
        print(result)
        new_exp = get_dop_binary(result)
        result = new_exp
        print(result)
        sum_result.insert(2,0)
        sum_result.pop()
    elif num1[1:9] == num2[1:9]:
        print(result)
        new_exp = get_dop_binary(result)
        result = new_exp
        print(result)
        sum_result.insert(2,0)
        sum_result.pop()
    result.insert(0, sum_result[0])
    result = result + sum_result[2:25]  # Исправлено на круглые скобки


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

def sum_of_mantis(num1: list, num2: list):
    first_binary  = get_dop_binary_sum(num1)
    second_binary  = get_dop_binary_sum(num2)

    carry = 0
    result = []

    for i in range(len(first_binary) - 1, -1, -1):
        temp = first_binary[i] + second_binary[i] + carry
        res_bit = temp % 2
        carry = temp // 2
        result.insert(0, res_bit)
    
    if num1[0] and num2[0] == 1:
        for i in range(1, len(result)):
            if result[i] == 1:
                result[i] = 0
            else:
                result[i] = 1 
        result = get_dop_binary(result)        

    print("RES: ", result)
    return result, carry  

def difference_of_binaries(first_binary: list, second_binary: list):
    inverted_second_binary = second_binary.copy()
    inverted_second_binary[0] = 1 - inverted_second_binary[0]
    return sum_of_binaries(first_binary, inverted_second_binary)

number = float(input("Введите число: "))
binary_representation = conv_to_eeei(number)
number2 = float(input("Введите число: "))
binary_representation2 = conv_to_eeei(number2)
print_binary(binary_representation)
float_value = binary_to_float(binary_representation)
print("Переведенное число:", float_value)

summa = sum_of_EEEI(binary_representation, binary_representation2)
float_value2 = binary_to_float(summa)
print("СУМММАА:", float_value2)
print(summa)

