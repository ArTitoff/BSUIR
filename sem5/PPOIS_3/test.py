import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнялась {end_time - start_time:.4f} секунд")
        return result
    return wrapper

@timer_decorator
def calculate_sum(n):
    return sum(range(n))

print(calculate_sum(1000000))