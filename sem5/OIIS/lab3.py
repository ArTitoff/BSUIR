import cv2
import numpy as np
import os

class SimpleBrightnessAligner:
    def align_brightness_simple(self, image1_path, image2_path, output_path="aligned_result.jpg"):
        """
        Простое выравнивание яркости двух изображений
        """
        # Загрузка изображений
        img1 = cv2.imread(image1_path)
        img2 = cv2.imread(image2_path)
        
        if img1 is None or img2 is None:
            raise FileNotFoundError("Не удалось загрузить одно из изображений")
        
        # Приведение к одинаковому размеру
        height = min(img1.shape[0], img2.shape[0])
        width = min(img1.shape[1], img2.shape[1])
        img1 = cv2.resize(img1, (width, height))
        img2 = cv2.resize(img2, (width, height))
        
        # Конвертируем в HSV
        img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        
        # Вычисляем среднюю яркость
        brightness1 = np.mean(img1_hsv[:, :, 2])
        brightness2 = np.mean(img2_hsv[:, :, 2])
        
        print(f"Яркость image1: {brightness1:.1f}")
        print(f"Яркость image2: {brightness2:.1f}")
        
        # Выравниваем яркость image2 к image1
        ratio = brightness1 / brightness2
        img2_hsv[:, :, 2] = np.clip(img2_hsv[:, :, 2] * ratio, 0, 255).astype(np.uint8)
        
        # Конвертируем обратно в BGR
        img2_aligned = cv2.cvtColor(img2_hsv, cv2.COLOR_HSV2BGR)
        
        # Сохраняем результат
        cv2.imwrite(output_path, img2_aligned)
        print(f"Результат сохранен: {output_path}")
        
        return img2_aligned

# Простой пример использования
if __name__ == "__main__":
    aligner = SimpleBrightnessAligner()
    
    # Укажите пути к вашим изображениям
    aligned_image = aligner.align_brightness_simple(
        "/home/artem/Рабочий стол/BSUIR/OIIS/kat.jpeg", 
        "/home/artem/Рабочий стол/BSUIR/OIIS/bright_image.jpeg",
        "result_aligned.jpg"
    )