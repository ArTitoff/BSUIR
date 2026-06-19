import cv2
import numpy as np


def median_filter_manual(image, kernel_size=3):
    # Проверяем, что размер фильтра нечётный
    if kernel_size % 2 == 0:
        raise ValueError("Размер ядра должен быть нечётным!")

    # Определяем отступ (радиус фильтра)
    pad = kernel_size // 2

    # Добавляем рамку (чтобы не выходить за границы)
    padded_image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_REFLECT)

    # Создаем выходной массив
    filtered_image = np.zeros_like(image)

    # Если изображение цветное
    if len(image.shape) == 3:
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                for c in range(image.shape[2]):
                    # Извлекаем окно
                    window = padded_image[y:y + kernel_size, x:x + kernel_size, c]
                    # Вычисляем медиану
                    filtered_image[y, x, c] = np.median(window)
    else:
        # Если изображение чёрно-белое
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                window = padded_image[y:y + kernel_size, x:x + kernel_size]
                filtered_image[y, x] = np.median(window)

    return filtered_image


# Загружаем изображение
image_path = "pig.png"  # Укажите путь к вашему изображению
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError("Не удалось загрузить изображение. Проверьте путь к файлу!")

# 1. Медианные фильтры
median_filtered = cv2.medianBlur(image, 5)
filtered = median_filter_manual(image, 5)

# 2. Гауссов фильтр
gaussian_filtered = cv2.GaussianBlur(image, (5, 5), 0)

# 3. Размытие по среднему
average_filtered = cv2.blur(image, (5, 5))

# 4. Повышение резкости
kernel_sharpening = np.array([
    [-1, -1, -1],
    [-1,  9, -1],
    [-1, -1, -1]
])
sharpened = cv2.filter2D(image, -1, kernel_sharpening)

# 5. Детектор краёв
edges = cv2.Canny(image, 100, 200)

# Сохраняем результаты
cv2.imwrite("median_filtered.jpg", median_filtered)
cv2.imwrite("gaussian_filtered.jpg", gaussian_filtered)
cv2.imwrite("average_filtered.jpg", average_filtered)
cv2.imwrite("sharpened.jpg", sharpened)
cv2.imwrite("edges.jpg", edges)
cv2.imwrite("manual_median_filtered.jpg", filtered)

print("Фильтры применены и сохранены в текущей папке.")
