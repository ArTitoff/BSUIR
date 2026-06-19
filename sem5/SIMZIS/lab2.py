import string
import time

ALPHABET = string.ascii_lowercase

def shifr_vezhenera():
    try:
        text = str(input("Введите текст "))
        key = str(input("Введите ключевое слово "))
    except Exception as e:
        print(e)
    key_text = (key * (len(text) // len(key) + 1))[:len(text)]
    print(key_text)

    result = []  
    
    for i, char in enumerate(text):
        if char in ALPHABET:
            text_pos = ALPHABET.index(char)
            key_pos = ALPHABET.index(key_text[i])
            encript_pos = (text_pos + key_pos) % 26
            result.append(ALPHABET[encript_pos])  
        else: 
            result.append(char)      
    return ''.join(result) 




def decript_shifr_vezhenera(key: str, text: str):
    key_text = (key * (len(text) // len(key) + 1))[:len(text)]

    result = [] 

    for i, char in enumerate(text):
        if char in ALPHABET:
            text_pos = ALPHABET.index(char)
            key_pos = ALPHABET.index(key_text[i])
            encript_pos = (26 + text_pos - key_pos) % 26
            result.append(ALPHABET[encript_pos])  
        else: 
            result.append(char)      
    return ''.join(result) 


def brutforce(word: str, step: int):
    if step == 1:
        for i in ALPHABET:
            yield word + i
    else:
        for i in ALPHABET:
            yield from brutforce(word + i, step - 1)


def main():
    result = shifr_vezhenera()
    print(f"Результат шифровки: {result}")
    try:
        text = str(input("Введите зашифрованный текст "))
        key = str(input("Введите ключевое слово "))
    except Exception as e:
        print(e)
    decription = decript_shifr_vezhenera(key, text)
    print(f"Результат расшифровки: {decription}")

    print("Brutforse:")
    iter = 1
    start = time.time()
    brutforce_key = ''
    while decription != brutforce_key:
        for combo in brutforce('', iter):
            # print(combo)
            brutforce_key = decript_shifr_vezhenera(combo, result)
            if decription == brutforce_key:
                break
        iter = iter + 1
    end = time.time()
    print(f"Brutforse time: {end - start}")


if __name__ == "__main__":
    main()

