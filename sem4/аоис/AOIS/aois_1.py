num1_10 = []
num2_10 = []


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

    if len(binary_representation) > 32:
        raise ValueError("Значение слишком большое и не помещается в 32 формат")
    
    while len(binary_representation) < 32:
        binary_representation.insert(1, 0)
        
    return binary_representation

def convert_to_10(num_10: list):
    num = 0
    lenth = len(num_10)

    for index, binary in enumerate(num_10[1:], start=1):
        num = num + 2 ** (lenth - 1 - index) *  binary
    
    if num_10[0] == 1:
        num *= -1
    print(f"Значение, переведенное из двоичного: {num}")





def sum_of_binaries_multy(first_binary: list, second_binary: list) -> list:
    carry = 0
    result = []
    
    max_len = max(len(first_binary), len(second_binary))
    first_binary = [0] * (max_len - len(first_binary)) + first_binary
    second_binary = [0] * (max_len - len(second_binary)) + second_binary

    for i in range(max_len - 1, -1, -1):
        temp = first_binary[i] + second_binary[i] + carry
        res_bit = temp % 2
        carry = temp // 2
        result.insert(0, res_bit)

    if carry:
        result.insert(0, carry)

    return result

def multiplication_of_binaries(first_binary: list, second_binary: list) -> list:
    first_binary_dop = first_binary.copy()
    second_binary_dop = second_binary.copy()

    sign_first = first_binary_dop[0]
    sign_second = second_binary_dop[0]    # Дополняем до одинаковой длины

    del first_binary_dop[0]
    del second_binary_dop[0]
    max_len = max(len(first_binary),len(second_binary)  )
    first_binary = [0] * (max_len - len(first_binary)) + first_binary
    second_binary = [0] * (max_len - len(second_binary)) + second_binary

    result_sign = (sign_first + sign_second) % 2

    result = [0] * (len(first_binary_dop) + len(second_binary_dop))

    for i in range(len(second_binary_dop) - 1, -1, -1):
        if second_binary_dop[i] == 1:
            temp = first_binary_dop + [0] * (len(second_binary_dop) - 1 - i)
            result = sum_of_binaries_multy(result, temp)

    result.insert(0, result_sign)

    return result




num1_decimal = -30  
num2_decimal = -15   

binary1 = convert_to_binary(num1_decimal)
binary2 = convert_to_binary(num2_decimal)


mult = multiplication_of_binaries(binary1, binary2)
print("Произведение:", mult)  

convert_to_10(mult)

