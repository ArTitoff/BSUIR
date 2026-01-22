import cv2
import numpy as np

def simple_brightness_alignment(target_img, reference_img):
    #Простое выравнивание яркости между двумя изображениями
    
    # Конвертируем в LAB
    lab_target = cv2.cvtColor(target_img, cv2.COLOR_BGR2LAB)
    lab_ref = cv2.cvtColor(reference_img, cv2.COLOR_BGR2LAB)
    
    # Разделяем каналы
    L_target, A_target, B_target = cv2.split(lab_target)
    L_ref, _, _ = cv2.split(lab_ref)
    
    # Выравниваем яркость по среднему и стандартному отклонению
    target_mean = np.mean(L_target)
    target_std = np.std(L_target)
    ref_mean = np.mean(L_ref)
    ref_std = np.std(L_ref)
    
    # Линейное преобразование при помощи ЦЕНТРИРОВАНИЕ МАСШТАБИРОВАНИЯ И СДВИГА КОНТРАСТНОСТИ
    L_aligned = (L_target - target_mean) * (ref_std / target_std) + ref_mean
    L_aligned = np.clip(L_aligned, 0, 255).astype(np.uint8)
    
    # Объединяем обратно
    lab_aligned = cv2.merge([L_aligned, A_target, B_target])
    aligned_img = cv2.cvtColor(lab_aligned, cv2.COLOR_LAB2BGR)
    
    return aligned_img

#пример использования

reference = cv2.imread('/home/artem/Рабочий стол/BSUIR/OIIS/m2.jpg')
target = cv2.imread('/home/artem/Рабочий стол/BSUIR/OIIS/m1.jpg')
result = simple_brightness_alignment(target, reference)
cv2.imwrite('m3.jpg', result)

reference = cv2.imread('/home/artem/Рабочий стол/BSUIR/OIIS/m1.jpg')
target = cv2.imread('/home/artem/Рабочий стол/BSUIR/OIIS/m2.jpg')
result = simple_brightness_alignment(target, reference)
cv2.imwrite('m4.jpg', result)