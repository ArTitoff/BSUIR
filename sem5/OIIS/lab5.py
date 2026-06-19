import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

class StereoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Создатель стереоизображений")
        self.root.geometry("600x350")
        
        self.left_path = None
        self.right_path = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Создание стереоизображений", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Фрейм для кнопок выбора файлов
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)
        
        # Кнопка для левого изображения
        self.left_btn = tk.Button(file_frame, text="Выбрать левое изображение", 
                                 command=self.select_left, width=22, height=2)
        self.left_btn.grid(row=0, column=0, padx=10, pady=5)
        
        self.left_label = tk.Label(file_frame, text="Не выбрано", fg="gray", wraplength=200)
        self.left_label.grid(row=1, column=0, padx=10)
        
        # Кнопка для правого изображения
        self.right_btn = tk.Button(file_frame, text="Выбрать правое изображение", 
                                  command=self.select_right, width=22, height=2)
        self.right_btn.grid(row=0, column=1, padx=10, pady=5)
        
        self.right_label = tk.Label(file_frame, text="Не выбрано", fg="gray", wraplength=200)
        self.right_label.grid(row=1, column=1, padx=10)
        
        # Фрейм для настроек
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=10)
        
        # Поле для имени выходного файла
        tk.Label(settings_frame, text="Имя результата:").grid(row=0, column=0, sticky="w")
        self.output_entry = tk.Entry(settings_frame, width=30)
        self.output_entry.insert(0, "stereo_result.jpg")
        self.output_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Кнопка создания
        self.create_btn = tk.Button(self.root, text="Создать стереоизображение", 
                                   command=self.create_stereo, bg="lightblue", 
                                   font=("Arial", 12, "bold"), height=2,
                                   state="disabled")
        self.create_btn.pack(pady=20)
        
        # Статус
        self.status_label = tk.Label(self.root, text="Выберите два изображения", fg="blue")
        self.status_label.pack()
    
    def select_left(self):
        filename = filedialog.askopenfilename(
            title="Выберите левое изображение",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if filename:
            self.left_path = filename
            self.left_label.config(text=os.path.basename(filename), fg="green")
            self.check_ready()
    
    def select_right(self):
        filename = filedialog.askopenfilename(
            title="Выберите правое изображение",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if filename:
            self.right_path = filename
            self.right_label.config(text=os.path.basename(filename), fg="green")
            self.check_ready()
    
    def check_ready(self):
        if self.left_path and self.right_path:
            self.create_btn.config(state="normal")
            self.status_label.config(text="Готов к созданию стереоизображения", fg="green")
        else:
            self.create_btn.config(state="disabled")
    
    def create_stereo(self):
        if not self.left_path or not self.right_path:
            messagebox.showerror("Ошибка", "Сначала выберите оба изображения!")
            return
        
        output_path = self.output_entry.get().strip()
        if not output_path:
            output_path = "stereo_result.jpg"
        
        self.status_label.config(text="Обрабатываю изображения...", fg="orange")
        self.root.update()
        
        try:
            # Загружаем изображения
            left_img = cv2.imread(self.left_path)
            right_img = cv2.imread(self.right_path)
            
            if left_img is None or right_img is None:
                messagebox.showerror("Ошибка", "Не удалось загрузить изображения!")
                return
            
            # Приводим к одинаковому размеру
            if left_img.shape != right_img.shape:
                right_img = cv2.resize(right_img, (left_img.shape[1], left_img.shape[0]))
            
            # Создаем стереоизображение
            stereo = np.zeros_like(left_img)
            
            # Левое изображение - только красный канал
            stereo[:, :, 2] = left_img[:, :, 2]  # Красный канал
            
            # Правое изображение - синий и зеленый каналы
            stereo[:, :, 0] = right_img[:, :, 0]  # Синий канал
            stereo[:, :, 1] = right_img[:, :, 1]  # Зеленый канал
            
            # Сохраняем результат
            cv2.imwrite(output_path, stereo)
            
            # Показываем результат
            full_path = os.path.abspath(output_path)
            messagebox.showinfo("Готово!", 
                               f"Стереоизображение успешно создано!\n\n"
                               f"Файл: {full_path}\n\n"
                               f"Для просмотра используйте красно-синие 3D-очки")
            
            self.status_label.config(text="Готово! Выберите новые изображения", fg="green")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")
            self.status_label.config(text="Ошибка при создании", fg="red")

def main():
    root = tk.Tk()
    app = StereoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()