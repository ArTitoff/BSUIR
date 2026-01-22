import cv2
import numpy as np
import os
from datetime import datetime

class ImageFilterApp:
    def __init__(self):
        self.filters = {
            "1": ("Гауссовский фильтр", self.gaussian_filter),
            "2": ("Медианный фильтр", self.median_filter),
            "3": ("Фильтр Собеля (границы)", self.sobel_filter),
            "4": ("Билатеральный фильтр", self.bilateral_filter),
            "5": ("Лапласиан (усиление границ)", self.laplacian_filter),
            "6": ("Фильтр размытия (усреднение)", self.blur_filter),
            "7": ("Фильтр резкости", self.sharpen_filter)
        }
        self.output_dir = "filtered_results"
        self.create_output_dir()
    
    def create_output_dir(self):
        """Создает папку для сохранения результатов"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Создана папка для результатов: {self.output_dir}")
    
    def gaussian_filter(self, image):
        """Гауссовское размытие для уменьшения шума"""
        return cv2.GaussianBlur(image, (5, 5), 0)
    
    def median_filter(self, image):
        """Медианный фильтр для удаления шума с сохранением границ"""
        return cv2.medianBlur(image, 5)
    
    def sobel_filter(self, image):
        """Фильтр Собеля для выделения границ"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        sobel = np.sqrt(sobelx**2 + sobely**2)
        sobel = np.uint8(255 * sobel / np.max(sobel))
        return cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)
    
    def bilateral_filter(self, image):
        """Билатеральный фильтр сохраняет границы при сглаживании"""
        return cv2.bilateralFilter(image, 9, 75, 75)
    
    def laplacian_filter(self, image):
        """Лапласиан для усиления границ"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian = np.uint8(np.absolute(laplacian))
        return cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)
    
    def blur_filter(self, image):
        """Простое усредняющее размытие"""
        kernel = np.ones((5, 5), np.float32) / 25
        return cv2.filter2D(image, -1, kernel)
    
    def sharpen_filter(self, image):
        """Фильтр увеличения резкости"""
        kernel = np.array([[-1, -1, -1],
                          [-1, 9, -1],
                          [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)
    
    def load_image(self, path):
        """Загрузка изображения"""
        image = cv2.imread(path)
        if image is None:
            raise FileNotFoundError(f"Не удалось загрузить изображение: {path}")
        return image
    
    def save_filtered_image(self, original, filtered, filter_name, filename=None):
        """Сохраняет оригинальное и отфильтрованное изображение"""
        
        # Если имя файла не указано, генерируем автоматически
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filter_name}_{timestamp}.jpg"
        
        # Убедимся, что расширение .jpg
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filename += '.jpg'
        
        # Полный путь к файлу
        full_path = os.path.join(self.output_dir, filename)
        
        # Сохраняем отфильтрованное изображение
        cv2.imwrite(full_path, filtered)
        
        # Также сохраняем сравнение (оригинал + фильтр)
        comparison_path = os.path.join(self.output_dir, f"comparison_{filename}")
        self.save_comparison_image(original, filtered, filter_name, comparison_path)
        
        print(f"✓ Отфильтрованное изображение сохранено: {full_path}")
        print(f"✓ Сравнение сохранено: {comparison_path}")
        
        return full_path
    
    def save_comparison_image(self, original, filtered, filter_name, path):
        """Создает и сохраняет изображение с сравнением (оригинал + фильтр)"""
        # Изменяем размеры для сравнения (если изображение слишком большое)
        max_height = 800
        if original.shape[0] > max_height:
            scale = max_height / original.shape[0]
            new_width = int(original.shape[1] * scale)
            original_resized = cv2.resize(original, (new_width, max_height))
            filtered_resized = cv2.resize(filtered, (new_width, max_height))
        else:
            original_resized = original
            filtered_resized = filtered
        
        # Создаем объединенное изображение
        comparison = np.hstack((original_resized, filtered_resized))
        
        # Добавляем текст
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(comparison, 'Original', (10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(comparison, filter_name, (comparison.shape[1]//2 + 10, 30), font, 1, (255, 255, 255), 2)
        
        # Сохраняем
        cv2.imwrite(path, comparison)
    
    def show_available_filters(self):
        """Показывает доступные фильтры"""
        print("\n" + "="*60)
        print("ДОСТУПНЫЕ ФИЛЬТРЫ:")
        print("="*60)
        for key, (name, _) in self.filters.items():
            print(f"{key}. {name}")
        print("="*60)
    
    def run(self):
        """Основной цикл программы"""
        print("=== ПРОГРАММА ДЛЯ ПРИМЕНЕНИЯ ФИЛЬТРОВ К ИЗОБРАЖЕНИЯМ ===")
        print(f"Результаты сохраняются в папку: {self.output_dir}")
        
        original_image = None
        
        while True:
            # Загрузка изображения, если еще не загружено
            if original_image is None:
                while True:
                    image_path = input("\nВведите путь к изображению: ")
                    try:
                        original_image = self.load_image(image_path)
                        print(f"✓ Изображение успешно загружено! Размер: {original_image.shape[1]}x{original_image.shape[0]}")
                        break
                    except FileNotFoundError as e:
                        print(f"✗ {e}")
                        print("Попробуйте снова.")
            
            self.show_available_filters()
            
            print("\nВыберите действие:")
            print("1-7 - Применить соответствующий фильтр")
            print("a - Применить ВСЕ фильтры последовательно")
            print("l - Загрузить новое изображение")
            print("d - Показать содержимое папки с результатами")
            print("q - Выйти из программы")
            
            choice = input("Ваш выбор: ").lower()
            
            if choice == 'q':
                print("Выход из программы...")
                break
            elif choice == 'l':
                # Загрузка нового изображения
                image_path = input("Введите путь к новому изображению: ")
                try:
                    original_image = self.load_image(image_path)
                    print(f"✓ Новое изображение успешно загружено! Размер: {original_image.shape[1]}x{original_image.shape[0]}")
                except FileNotFoundError as e:
                    print(f"✗ {e}")
            elif choice == 'd':
                # Показать содержимое папки с результатами
                self.show_results_directory()
            elif choice == 'a':
                # Применить все фильтры
                self.apply_all_filters(original_image)
            elif choice in self.filters:
                # Применение выбранного фильтра
                filter_name, filter_func = self.filters[choice]
                print(f"Применение фильтра: {filter_name}...")
                
                try:
                    filtered_image = filter_func(original_image)
                    
                    # Предлагаем пользователю имя файла
                    default_name = f"{filter_name.replace(' ', '_').lower()}.jpg"
                    filename = input(f"Введите имя файла для сохранения (Enter для {default_name}): ").strip()
                    if not filename:
                        filename = default_name
                    
                    self.save_filtered_image(original_image, filtered_image, filter_name, filename)
                    
                except Exception as e:
                    print(f"✗ Ошибка при применении фильтра: {e}")
            else:
                print("✗ Неверный выбор! Попробуйте снова.")
    
    def apply_all_filters(self, original_image):
        """Применяет все фильтры последовательно"""
        print("\nПрименение всех фильтров...")
        
        for key, (filter_name, filter_func) in self.filters.items():
            print(f"Обработка: {filter_name}...")
            
            try:
                filtered_image = filter_func(original_image)
                filename = f"all_filters_{filter_name.replace(' ', '_').lower()}.jpg"
                self.save_filtered_image(original_image, filtered_image, filter_name, filename)
                
            except Exception as e:
                print(f"✗ Ошибка при применении {filter_name}: {e}")
        
        print("✓ Все фильтры применены успешно!")
    
    def show_results_directory(self):
        """Показывает содержимое папки с результатами"""
        print(f"\nСодержимое папки '{self.output_dir}':")
        print("-" * 50)
        
        try:
            files = os.listdir(self.output_dir)
            if not files:
                print("Папка пуста")
            else:
                for i, file in enumerate(sorted(files), 1):
                    file_path = os.path.join(self.output_dir, file)
                    file_size = os.path.getsize(file_path) // 1024  # размер в KB
                    print(f"{i:2d}. {file} ({file_size} KB)")
        except Exception as e:
            print(f"Ошибка при чтении папки: {e}")
        
        print("-" * 50)

def main():
    """Основная функция"""
    try:
        app = ImageFilterApp()
        app.run()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()