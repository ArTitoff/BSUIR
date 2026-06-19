import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from ultralytics import YOLO
import torch
import gc

class ObjectRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Распознавание объектов - Лабораторная работа №6")
        self.root.geometry("1200x800")
        
        # Переменные для хранения изображений
        self.detect_image = None
        self.source_image = None
        self.replacement_image = None
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.setup_ui()
    
    def load_yolo_model(self):
        """Загрузка YOLO модели с полной очисткой предыдущей"""
        try:
            # Очищаем предыдущую модель
            if hasattr(self, 'model'):
                del self.model
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            
            print("🔄 Загрузка YOLO модели...")
            self.model = YOLO('yolov8n.pt')
            print(f"✅ YOLO модель загружена! Устройство: {self.device}")
            return True
        except Exception as e:
            print(f"❌ Ошибка загрузки YOLO: {e}")
            messagebox.showerror("Ошибка", "Не удалось загрузить YOLO модель!")
            return False
    
    def setup_ui(self):
        """Создание интерфейса"""
        # Создаем вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка 1: Детекция объектов YOLO
        self.tab_detection = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_detection, text="Детекция объектов YOLO")
        
        # Вкладка 2: Замена объектов
        self.tab_replace = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_replace, text="Умная замена объектов")
        
        self.setup_detection_tab()
        self.setup_replacement_tab()
    
    def setup_detection_tab(self):
        """Настройка вкладки детекции"""
        title_label = tk.Label(self.tab_detection, 
                              text="Детекция объектов с помощью YOLO", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Фрейм для управления
        control_frame = tk.Frame(self.tab_detection)
        control_frame.pack(pady=10)
        
        # Загрузка изображения
        self.load_detect_btn = tk.Button(control_frame, text="Загрузить изображение", 
                                       command=self.load_detection_image, width=20, height=2)
        self.load_detect_btn.grid(row=0, column=0, padx=5)
        
        # Выбор класса для детекции
        tk.Label(control_frame, text="Класс объекта:").grid(row=0, column=1)
        self.detect_class = ttk.Combobox(control_frame, 
                                        values=["Все объекты", "person", "car", "sports ball", "cat", "dog", "bottle"],
                                        state="readonly", width=15)
        self.detect_class.set("Все объекты")
        self.detect_class.grid(row=0, column=2, padx=5)
        
        # Порог уверенности
        tk.Label(control_frame, text="Порог уверенности:").grid(row=0, column=3)
        self.confidence_var = tk.DoubleVar(value=0.25)
        confidence_scale = tk.Scale(control_frame, from_=0.1, to=0.9, resolution=0.05,
                                  orient=tk.HORIZONTAL, variable=self.confidence_var, length=150)
        confidence_scale.grid(row=0, column=4, padx=5)
        
        # Кнопка детекции
        self.detect_btn = tk.Button(control_frame, text="Обнаружить объекты", 
                                   command=self.detect_objects_yolo, 
                                   bg="lightgreen", width=20, height=2)
        self.detect_btn.grid(row=0, column=5, padx=10)
        
        # Статус загрузки
        self.detect_status = tk.Label(control_frame, text="Изображение не загружено", fg="red")
        self.detect_status.grid(row=1, column=0, columnspan=6)
        
        # Область отображения
        result_frame = tk.Frame(self.tab_detection)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.detect_canvas = tk.Canvas(result_frame, bg='white', relief=tk.SUNKEN, bd=2)
        self.detect_canvas.pack(fill='both', expand=True)
        
        # Статистика
        self.stats_label = tk.Label(self.tab_detection, text="")
        self.stats_label.pack()
    
    def setup_replacement_tab(self):
        """Настройка вкладки замены объектов"""
        title_label = tk.Label(self.tab_replace, 
                              text="Умная замена объектов на изображениях", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Фрейм управления
        control_frame = tk.Frame(self.tab_replace)
        control_frame.pack(pady=10)
        
        # Загрузка изображений
        self.load_source_btn = tk.Button(control_frame, text="Исходное изображение", 
                                        command=self.load_source, width=20, height=2)
        self.load_source_btn.grid(row=0, column=0, padx=5)
        
        self.load_replacement_btn = tk.Button(control_frame, text="Объект для замены", 
                                             command=self.load_replacement_obj, width=20, height=2)
        self.load_replacement_btn.grid(row=0, column=1, padx=5)
        
        # Выбор типа объекта для замены
        type_frame = tk.Frame(self.tab_replace)
        type_frame.pack(pady=10)
        
        tk.Label(type_frame, text="Заменить объекты:").grid(row=0, column=0)
        
        self.replace_class = ttk.Combobox(type_frame, 
                                         values=["sports ball", "person", "car", "cat", "dog", "bottle"],
                                         state="readonly", width=15)
        self.replace_class.set("sports ball")
        self.replace_class.grid(row=0, column=1, padx=5)
        
        # Настройки смешанной замены
        tk.Label(type_frame, text="Прозрачность:").grid(row=0, column=2)
        self.alpha_var = tk.DoubleVar(value=0.7)
        alpha_scale = tk.Scale(type_frame, from_=0.1, to=1.0, resolution=0.1,
                              orient=tk.HORIZONTAL, variable=self.alpha_var, length=100)
        alpha_scale.grid(row=0, column=3, padx=5)
        
        # Кнопка замены
        self.replace_btn = tk.Button(type_frame, text="Выполнить умную замену", 
                                    command=self.smart_replace_objects, 
                                    bg="lightcoral", width=20, height=2)
        self.replace_btn.grid(row=0, column=4, padx=10)
        
        # Статус
        self.replace_status = tk.Label(type_frame, text="Загрузите изображения")
        self.replace_status.grid(row=1, column=0, columnspan=5)
        
        # Область отображения
        result_frame = tk.Frame(self.tab_replace)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.replace_canvas = tk.Canvas(result_frame, bg='white', relief=tk.SUNKEN, bd=2)
        self.replace_canvas.pack(fill='both', expand=True)
    
    def load_detection_image(self):
        """Загрузка изображения для детекции"""
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if filename:
            image = cv2.imread(filename)
            if image is not None:
                self.detect_image = image.copy()
                self.detect_status.config(text=f"Изображение: {os.path.basename(filename)}", fg="green")
                self.display_image(self.detect_image, self.detect_canvas)
                self.stats_label.config(text="Готово к детекции")
                print(f"✅ Детекция: загружено изображение {filename}")
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить изображение!")
    
    def load_source(self):
        """Загрузка исходного изображения для замены"""
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if filename:
            self.source_image = cv2.imread(filename)
            if self.source_image is not None:
                self.display_image(self.source_image, self.replace_canvas)
                self.replace_status.config(text="Исходное изображение загружено")
                print(f"✅ Замена: загружено исходное изображение {filename}")
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить изображение!")
    
    def load_replacement_obj(self):
        """Загрузка объекта для замены"""
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if filename:
            self.replacement_image = cv2.imread(filename)
            if self.replacement_image is not None:
                self.replace_status.config(text="Все изображения загружены")
                print(f"✅ Замена: загружен объект замены {filename}")
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить объект!")
    
    def detect_objects_yolo(self):
        """Детекция объектов с помощью YOLO"""
        if self.detect_image is None:
            messagebox.showerror("Ошибка", "Сначала загрузите изображение!")
            return
        
        # ПОЛНАЯ ПЕРЕЗАГРУЗКА МОДЕЛИ
        if not self.load_yolo_model():
            return
        
        try:
            self.stats_label.config(text="Выполняется детекция...")
            self.root.update()
            
            target_class = self.detect_class.get()
            confidence = self.confidence_var.get()
            
            print(f"🔍 Детекция: класс={target_class}, уверенность={confidence}")
            
            # Запускаем детекцию
            if target_class == "Все объекты":
                results = self.model.predict(
                    self.detect_image, 
                    conf=confidence,
                    device=self.device,
                    verbose=False
                )
            else:
                # Находим ID класса
                class_id = None
                for idx, name in self.model.names.items():
                    if name == target_class:
                        class_id = idx
                        break
                
                if class_id is None:
                    messagebox.showerror("Ошибка", f"Класс '{target_class}' не найден!")
                    return
                
                results = self.model.predict(
                    self.detect_image,
                    conf=confidence,
                    classes=[class_id],
                    device=self.device,
                    verbose=False
                )
            
            # Получаем аннотированное изображение
            annotated_image = results[0].plot()
            
            # Собираем статистику
            stats = self._collect_detection_stats(results[0])
            
            # Отображаем результат
            self.display_image(annotated_image, self.detect_canvas)
            self.stats_label.config(text=stats)
            print(f"✅ Детекция: завершена успешно, найдено {len(results[0].boxes)} объектов")
            
            # ОЧИСТКА ПАМЯТИ
            del results
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
        except Exception as e:
            print(f"❌ Детекция: ошибка - {str(e)}")
            messagebox.showerror("Ошибка", f"Ошибка при детекции: {str(e)}")
            self.stats_label.config(text="Ошибка детекции")
    
    def _collect_detection_stats(self, result):
        """Сбор статистики по детекциям"""
        boxes = result.boxes
        
        if len(boxes) == 0:
            return "Объекты не обнаружены"
        
        class_counts = {}
        for box in boxes:
            cls_id = int(box.cls[0])
            cls_name = result.names[cls_id]
            class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
        
        stats_text = f"Найдено объектов: {len(boxes)}\n"
        for cls_name, count in sorted(class_counts.items()):
            stats_text += f"{cls_name}: {count}\n"
        
        return stats_text
    
    def smart_replace_objects(self):
        """Умная смешанная замена объектов"""
        if self.source_image is None or self.replacement_image is None:
            messagebox.showerror("Ошибка", "Сначала загрузите исходное изображение и объект для замены!")
            return
        
        # ПОЛНАЯ ПЕРЕЗАГРУЗКА МОДЕЛИ
        if not self.load_yolo_model():
            return
        
        try:
            self.replace_status.config(text="Выполняется умная замена...")
            self.root.update()
            
            target_class = self.replace_class.get()
            alpha = self.alpha_var.get()
            
            print(f"🔧 Замена: класс={target_class}, прозрачность={alpha}")
            
            # Находим ID класса
            class_id = None
            for idx, name in self.model.names.items():
                if name == target_class:
                    class_id = idx
                    break
            
            if class_id is None:
                messagebox.showerror("Ошибка", f"Класс '{target_class}' не найден!")
                return
            
            # Детектируем объекты нужного класса
            results = self.model.predict(
                self.source_image,
                conf=0.25,
                classes=[class_id],
                device=self.device,
                verbose=False
            )
            
            # СОЗДАЕМ КОПИЮ для результата
            result_image = self.source_image.copy()
            replaced_count = 0
            
            # Заменяем найденные объекты с умным смешиванием
            boxes = results[0].boxes
            for box in boxes:
                if int(box.cls[0]) == class_id:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    w = x2 - x1
                    h = y2 - y1
                    
                    if w > 0 and h > 0:
                        replacement_resized = self.resize_replacement(self.replacement_image, w, h)
                        self.blend_replacement(result_image, replacement_resized, x1, y1, x2, y2, alpha)
                        replaced_count += 1
            
            # Отображаем результат
            self.display_image(result_image, self.replace_canvas)
            self.replace_status.config(text=f"Умная замена завершена! Заменено объектов: {replaced_count}")
            print(f"✅ Замена: завершена успешно, заменено {replaced_count} объектов")
            
            # ОЧИСТКА ПАМЯТИ
            del results
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
        except Exception as e:
            print(f"❌ Замена: ошибка - {str(e)}")
            messagebox.showerror("Ошибка", f"Ошибка при замене: {str(e)}")
            self.replace_status.config(text="Ошибка замены")
    
    def resize_replacement(self, replacement_img, target_w, target_h):
        """Изменение размера изображения замены с сохранением пропорций"""
        h, w = replacement_img.shape[:2]
        aspect_ratio = w / h
        
        if target_w / target_h > aspect_ratio:
            new_h = target_h
            new_w = int(target_h * aspect_ratio)
        else:
            new_w = target_w
            new_h = int(target_w / aspect_ratio)
        
        resized = cv2.resize(replacement_img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        result = np.zeros((target_h, target_w, 3), dtype=np.uint8)
        y_offset = (target_h - new_h) // 2
        x_offset = (target_w - new_w) // 2
        
        result[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        
        return result
    
    def blend_replacement(self, background, replacement, x1, y1, x2, y2, alpha):
        """Смешанная замена с плавным переходом"""
        try:
            target_region = background[y1:y2, x1:x2]
            
            if replacement.shape[:2] != target_region.shape[:2]:
                replacement = cv2.resize(replacement, (target_region.shape[1], target_region.shape[0]))
            
            mask = self.create_smooth_mask(replacement.shape[1], replacement.shape[0])
            
            for c in range(3):
                target_region[:, :, c] = (target_region[:, :, c] * (1 - mask * alpha) + 
                                        replacement[:, :, c] * mask * alpha).astype(np.uint8)
                
        except Exception as e:
            print(f"❌ Смешивание: ошибка - {e}")
            background[y1:y2, x1:x2] = replacement
    
    def create_smooth_mask(self, width, height):
        """Создание маски с плавными краями для смешивания"""
        mask = np.ones((height, width), dtype=np.float32)
        
        border_size = min(width, height) // 8
        
        for i in range(border_size):
            mask[i, :] *= i / border_size
            mask[height - 1 - i, :] *= i / border_size
            mask[:, i] *= i / border_size
            mask[:, width - 1 - i] *= i / border_size
        
        return mask
    
    def display_image(self, image, canvas):
        """Отображение изображения на canvas"""
        if isinstance(image, str):
            pil_image = Image.open(image)
        else:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
        
        canvas_width = canvas.winfo_width() if canvas.winfo_width() > 1 else 800
        canvas_height = canvas.winfo_height() if canvas.winfo_height() > 1 else 600
        
        img_ratio = pil_image.width / pil_image.height
        canvas_ratio = canvas_width / canvas_height
        
        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)
        
        pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(pil_image)
        canvas.delete("all")
        canvas.create_image(canvas_width//2, canvas_height//2, 
                          anchor=tk.CENTER, image=photo)
        canvas.image = photo

def main():
    root = tk.Tk()
    app = ObjectRecognitionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()