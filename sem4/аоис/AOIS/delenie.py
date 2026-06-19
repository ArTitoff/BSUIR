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


def convert_to_binary(num: int):
    sign = 0 if num >= 0 else 1
    num = abs(num)
    exp = 0
    binary_representation = [sign]

    while 2 ** exp <= num:
        exp += 1
    
    while exp != 0:
        exp -= 1
        if (num - 2 ** exp) >= 0:
            binary_representation.append(1)
            num = num - 2 ** exp
        else: 
            binary_representation.append(0)

    return binary_representation

def convert_to_10_del(num_10: list):
    num = 0
    lenth = len(num_10)

    for index, binary in enumerate(num_10[1:], start=1):
        num = num + 2 ** (lenth - 5 - index) *  binary
    
    if num_10[0] == 1:
        num *= -1
    print(f"Значение, переведенное из двоичного: {num}")


def delenie(num1: list, num2: list):
    delimoe = num1.copy() + [0] * 5
    delitel = num2.copy()  

    print(delimoe)
    print(delitel)

    sign = (delimoe[0] + delitel[0]) % 2
    result = [sign]
    del delimoe[0]
    del delitel[0]
    index = len(delimoe) - len(delitel)
    delitel = delitel + [0] * index

    print(delimoe)
    print(delitel)

    for i in range(index):
        dif = difference_of_binaries([0] + delimoe, [0] + delitel)
        if dif[0] == 0:
            result.append(1)
            delimoe = dif
        else:
            result.append(0)  
        del dif[0]
        
        delitel.insert(0,0)
        delitel.pop()

    return result


convert_to_10_del([1, 1, 0, 1, 0, 1, 0, 0])

num1 = convert_to_binary(40)
num2 = convert_to_binary(3)


chastn = delenie(num1, num2)
print(chastn)
convert_to_10_del(chastn)