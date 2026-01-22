import random

def find_deviders(number: int):
    temp = number - 1
    deviders = []
    devider = 2
    while devider ** 2 <= temp:
        if temp % devider == 0:
            deviders.append(devider) 
            while temp % devider == 0:
                temp //= devider
        devider += 1
    if temp > 1:
        deviders.append(temp)
    print(f"Делители {number}: {deviders}")
    return deviders


def find_pervoobraz(number: int):
    deviders =  find_deviders(number)
    temp = number - 1
    for g in range(2, temp):
        if pow(g, temp, number) != 1:
            continue
        pervo_flag = True
        for devider in deviders:
            if pow(g, temp // devider, number) == 1:
                pervo_flag = False
                break
        if pervo_flag:
            return g
    return None


def main():
    num_P = 7673
    num_g = find_pervoobraz(num_P)
    print(f"Первообразный корень {num_P}: {num_g}")

    alica_num = random.randint(1,100)
    print(f"Число Алисы: {alica_num}")
    A = pow(num_g, alica_num, num_P)
    print(f"Секрет Алисы: {A}")

    bob_num = random.randint(1,100)
    print(f"Число Боба: {bob_num}")
    B = pow(num_g, bob_num, num_P)
    print(f"Секрет Боба: {B}")

    S_alica = pow(B, alica_num, num_P)
    S_bob = pow(A, bob_num, num_P)
    print(f"Ключи совпали: {S_alica == S_bob}, {S_alica} == {S_bob}")


if __name__ == "__main__":
    main()