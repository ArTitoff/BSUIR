import random
import os

class RSA:
    def is_prime(self, n: int, k: int = 40) -> bool:
        """Проверка числа на простоту с помощью теста Миллера-Рабина"""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False
        
        # Записываем n-1 в виде (2^r)*d для Возведение в степень по модулю
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1
        
        # Проводим k тестов
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            # Возведение в квадрат по модулю
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True

    def generate_prime(self, bits):
        """Генерация простого числа заданной длины"""
        while True:
            # Генерируем случайное число с установленным старшим битом
            p = random.getrandbits(bits) | (1 << (bits - 1)) | 1
            if self.is_prime(p):
                return p

    def extended_gcd(self, a, b):
        """Расширенный алгоритм Евклида"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def mod_inverse(self, a, m):
        """Расширенный алгоритм Евклида для нахождения обратного элемента"""
        gcd, x, y = self.extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("Обратный элемент не существует")
        return x % m

    def fast_exp(self, base, exponent, modulus):
        """Быстрое возведение в степень методом последовательного возведения в квадрат и умножения"""
        result = 1
        base = base % modulus
        
        while exponent > 0:
            # Если младший бит экспоненты равен 1
            if exponent & 1:
                result = (result * base) % modulus
            
            # Сдвигаем экспоненту вправо
            exponent = exponent >> 1
            
            # Возводим base в квадрат по модулю
            base = (base * base) % modulus
        
        return result

    def generate_keys(self, bits=1024):
        """Генерация пары ключей RSA"""
        # Генерация двух больших простых чисел
        p = self.generate_prime(bits)
        q = self.generate_prime(bits)
        
        # Убедимся, что p и q разные
        while p == q:
            q = self.generate_prime(bits)
        
        # Вычисление модуля n
        n = p * q
        
        # Вычисление функции Эйлера
        phi = (p - 1) * (q - 1)
        
        # Выбор открытой экспоненты
        e = 65537
        
        # Проверяем, что e взаимно просто с phi
        while self.extended_gcd(e, phi)[0] != 1:
            e += 2
        
        # Вычисление секретной экспоненты
        d = self.mod_inverse(e, phi)
        
        return e, n, d

    def encrypt(self, message, public_key):
        """Шифрование сообщения"""
        e, n = public_key
        
        # Преобразуем строку в число
        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
            message_num = int.from_bytes(message_bytes, 'big')
        else:
            message_num = message
        
        # Проверяем, что сообщение меньше n
        if message_num >= n:
            raise ValueError("Сообщение слишком большое для шифрования")
        
        # Шифруем с использованием быстрого возведения в степень
        encrypted = self.fast_exp(message_num, e, n)
        return encrypted

    def decrypt(self, encrypted, private_key):
        """Дешифрование сообщения"""
        d, n = private_key
        
        # ДешифруемЫ
        decrypted_num = self.fast_exp(encrypted, d, n)
        
        # Преобразуем число обратно в строку
        try:
            byte_length = (decrypted_num.bit_length() + 7) // 8
            decrypted_bytes = decrypted_num.to_bytes(byte_length, 'big')
            return decrypted_bytes.decode('utf-8')
        except:
            return str(decrypted_num)

    def sign(self, message, private_key):
        """Создание цифровой подписи"""
        # Для подписи используем шифрование секретным ключом
        return self.encrypt(message, private_key)

    def verify(self, message, signature, public_key):
        """Проверка цифровой подписи"""
        # Для проверки подписи используем дешифрование открытым ключом
        try:
            decrypted_signature = self.decrypt(signature, public_key)
            
            # Преобразуем исходное сообщение для сравнения
            if isinstance(message, str):
                return decrypted_signature == message
            else:
                message_str = str(message)
                if message_str.isdigit():
                    return int(decrypted_signature) == int(message_str)
                else:
                    return decrypted_signature == message_str
        except Exception as e:
            print(f"Ошибка при проверке подписи: {e}")
            return False

def save_key(filename, key_type, e, n, d=None):
    """Сохранение ключей в файл"""
    with open(filename, 'w') as f:
        if key_type == "public":
            f.write(f"{e}\n{n}")
        else:  # private
            f.write(f"{d}\n{n}")

def load_key(filename):
    """Загрузка ключей из файла"""
    with open(filename, 'r') as f:
        lines = f.readlines()
        return int(lines[0].strip()), int(lines[1].strip())

def save_message(filename, message):
    """Сохранение сообщения в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(message))

def load_message(filename):
    """Загрузка сообщения из файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().strip()

# Создаем папку для результатов
os.makedirs("rsa_results", exist_ok=True)
rsa = RSA()

print("RSA АЛГОРИТМ - 10 ТЕСТОВ С ОБМЕНОМ ЧЕРЕЗ ФАЙЛЫ")
print("=" * 60)

for i in range(1, 11):
    print(f"\nТЕСТ {i}:")
    print("-" * 40)
    
    # 1. Генерация ключей и сохранение в файлы
    e, n, d = rsa.generate_keys(1024)
    save_key(f"rsa_results/public_key_{i}.txt", "public", e, n)
    save_key(f"rsa_results/private_key_{i}.txt", "private", e, n, d)
    print(f"Ключи сгенерированы (n={n.bit_length()} бит)")
    
    # 2. Создание и сохранение исходного сообщения
    message = f"Test message {i}: RSA с цифровой подписью"
    save_message(f"rsa_results/original_message_{i}.txt", message)
    print(f"Исходное сообщение: {message}")
    
    # 3. Загрузка открытого ключа и шифрование
    e_loaded, n_loaded = load_key(f"rsa_results/public_key_{i}.txt")
    encrypted = rsa.encrypt(message, (e_loaded, n_loaded))
    save_message(f"rsa_results/encrypted_message_{i}.txt", encrypted)
    print(f"Зашифровано")
    
    # 4. Загрузка секретного ключа и дешифрование
    d_loaded, n_loaded2 = load_key(f"rsa_results/private_key_{i}.txt")
    decrypted = rsa.decrypt(encrypted, (d_loaded, n_loaded2))
    print(f"Дешифровано: {decrypted}")
    
    # 5. Создание цифровой подписи
    signature = rsa.sign(message, (d_loaded, n_loaded2))
    save_message(f"rsa_results/signature_{i}.txt", signature)
    print(f"Создана цифровая подпись")
    
    # 6. Проверка цифровой подписи
    verified = rsa.verify(message, signature, (e_loaded, n_loaded))
    print(f"Подпись верна: {verified}")
    
    # 7. Проверка корректности шифрования
    encryption_ok = (message == decrypted)
    
    # Статус теста
    status = "УСПЕХ" if encryption_ok and verified else "ОШИБКА"
    print(f"СТАТУС ТЕСТА: {status}")

print(f"\nВсе файлы сохранены в папку: rsa_results/")
print("\nФОРМАТ ФАЙЛОВ:")
print("public_key_X.txt: e\\nn")
print("private_key_X.txt: d\\nn") 
print("original_message_X.txt: текст сообщения")
print("encrypted_message_X.txt: зашифрованное число")
print("signature_X.txt: цифровая подпись")