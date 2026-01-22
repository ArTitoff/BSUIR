import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def boundary_segmentation_simple(image_path):
    """ПРОСТАЯ сегментация через выделение границ (только Canny)"""
    
    # Создаем папку impl если ее нет
    output_dir = 'impl'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Загрузка изображения
    image = cv2.imread(image_path)
    if image is None:
        print(f"Ошибка: Не удалось загрузить изображение {image_path}")
        return
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # ЕДИНСТВЕННЫЙ метод: Детектор границ Canny (самый популярный и эффективный)
    edges = cv2.Canny(gray, 50, 150)
    
    # Создаем визуализацию: исходное изображение + границы поверх
    plt.figure(figsize=(12, 5))
    
    # 1. Исходное изображение
    plt.subplot(1, 2, 1)
    plt.imshow(image_rgb)
    plt.title('Исходное изображение')
    plt.axis('off')
    
    # 2. Найденные границы
    plt.subplot(1, 2, 2)
    plt.imshow(edges, cmap='gray')
    plt.title('Выделенные границы (Canny)')
    plt.axis('off')
    
    plt.tight_layout()
    
    # Сохраняем график
    output_path = os.path.join(output_dir, 'boundary_segmentation_simple.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"График сохранен в: {output_path}")
    
    
    return edges

# Пример использования
boundary_segmentation_simple('/home/artem/Рабочий стол/BSUIR/OIIS/m1.jpg')

def region_segmentation_by_points(image_path):
    """Простая сегментация через разметку точек области"""
    
    output_dir = 'impl'
    # Загрузка изображения
    image = cv2.imread(image_path)
    if image is None:
        print(f"Ошибка: Не удалось загрузить изображение {image_path}")
        return
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Просто берем одну точку в центре для сегментации
    height, width = gray.shape
    center_x, center_y = width // 2, height // 2
    
    # Создаем маску для сегментации
    segmented = np.zeros_like(gray)
    
    # Заливаем область от центральной точки (простой flood fill)
    stack = [(center_y, center_x)]
    visited = set()
    reference_value = gray[center_y, center_x]
    
    while stack:
        y, x = stack.pop()
        
        # Проверяем границы и чтобы не посещали уже
        if (y, x) in visited or y < 0 or y >= height or x < 0 or x >= width:
            continue
            
        # Если цвет похож на начальный (допуск ±30)
        if abs(int(gray[y, x]) - int(reference_value)) < 30:
            segmented[y, x] = 255
            visited.add((y, x))
            
            # Добавляем соседей
            stack.append((y-1, x))  # верх
            stack.append((y+1, x))  # низ
            stack.append((y, x-1))  # лево
            stack.append((y, x+1))  # право
    
    # Создаем визуализацию
    plt.figure(figsize=(15, 5))
    
    # 1. Исходное изображение с точкой
    plt.subplot(1, 3, 1)
    plt.imshow(image_rgb)
    plt.plot(center_x, center_y, 'ro', markersize=10, markeredgecolor='white', markeredgewidth=2)
    plt.title('Исходное изображение\n(красная точка - начало сегментации)')
    plt.axis('off')
    
    # 2. Выделенная область
    plt.subplot(1, 3, 2)
    plt.imshow(segmented, cmap='hot')
    plt.title('Выделенная область')
    plt.axis('off')
    
    # 3. Наложение на исходное изображение
    plt.subplot(1, 3, 3)
    overlay = image_rgb.copy()
    overlay[segmented == 255] = [255, 0, 0]  # Красим выделенную область в красный
    plt.imshow(overlay)
    plt.title('Результат сегментации')
    plt.axis('off')
    
    plt.tight_layout()
    
    # Сохраняем график
    output_path = os.path.join(output_dir, 'region_segmentation.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"График сохранен в: {output_path}")

# Пример использования
region_segmentation_by_points('/home/artem/Рабочий стол/BSUIR/OIIS/m1.jpg')
