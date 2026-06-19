import tkinter as tk
from tkinter import ttk


ermit_matrix = [[2, -2, 1, 1],
                [-3, 3, -2, -1],
                [0, 0, 1, 0],
                [1, 0, 0, 0]]

bezye_matrix = [[-1, 3, -3, 1],
                [3, -6, 3, 0],
                [-3, 3, 0, 0],
                [1, 0, 0, 0]]

v_spline_matrix = [[-1, 3, -3, 1],
                   [3, -6, 3, 0],
                   [-3, 0, 3, 0],
                   [1, 4, 1, 0]]

v_spline_matrix = [[elem / 6 for elem in row] for row in v_spline_matrix]


def ermit_interpolation(vector_x, vector_y, matrix):
    result_x = []
    result_y = []
    for row in matrix:
        t_xi = 0
        t_yi = 0
        for i, elem in enumerate(row):
            t_xi += vector_x[i] * elem
            t_yi += vector_y[i] * elem
        result_x.append(t_xi)
        result_y.append(t_yi)

    points = []
    for i in range(0, 11):
        t = i / 10
        x = t**3 * result_x[0] + t**2 * result_x[1] + t * result_x[2] + result_x[3]
        y = t**3 * result_y[0] + t**2 * result_y[1] + t * result_y[2] + result_y[3]
        points.append((x, y))
    return points


class CurveDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Кривые")
        self.root.geometry("1000x700")
        
        self.method = tk.StringVar(value="ermit")
        self.x_entries = []
        self.y_entries = []
        
        # Параметры координатной сетки
        self.x_min = -10
        self.x_max = 10
        self.y_min = -10
        self.y_max = 10
        
        # Режим сохранения (вкл/выкл)
        self.save_mode = tk.BooleanVar(value=False)
        
        # Список сохраненных кривых
        self.saved_curves = []  # будет хранить (метод, vector_x, vector_y, цвет)
        
        # Счетчик для цветов
        self.color_index = 0
        self.colors = ['blue', 'green', 'purple', 'orange', 'brown', 'cyan', 'magenta']
        
        self.setup_ui()
        self.draw()
    
    def setup_ui(self):
        # Панель слева
        left = ttk.Frame(self.root)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left, text="МЕТОД", font=('Arial', 12, 'bold')).pack(pady=5)
        
        ttk.Radiobutton(left, text="Эрмит", variable=self.method, 
                       value="ermit", command=self.draw).pack(anchor=tk.W)
        ttk.Radiobutton(left, text="Безье", variable=self.method, 
                       value="bezye", command=self.draw).pack(anchor=tk.W)
        ttk.Radiobutton(left, text="B-сплайн", variable=self.method, 
                       value="spline", command=self.draw).pack(anchor=tk.W)
        
        ttk.Separator(left).pack(fill=tk.X, pady=10)
        
        ttk.Label(left, text="КООРДИНАТЫ ТОЧЕК", font=('Arial', 10, 'bold')).pack()
        
        # 4 точки с полями X и Y
        for i in range(4):
            frame = ttk.Frame(left)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=f"P{i}:", width=3).pack(side=tk.LEFT)
            
            x_entry = ttk.Entry(frame, width=8)
            x_entry.pack(side=tk.LEFT, padx=2)
            x_entry.insert(0, str(i))
            self.x_entries.append(x_entry)
            
            y_entry = ttk.Entry(frame, width=8)
            y_entry.pack(side=tk.LEFT, padx=2)
            y_entry.insert(0, str(i))
            self.y_entries.append(y_entry)
        
        ttk.Separator(left).pack(fill=tk.X, pady=10)
        
        # Кнопка сохранения (вкл/выкл)
        save_frame = ttk.Frame(left)
        save_frame.pack(fill=tk.X, pady=5)
        
        ttk.Checkbutton(save_frame, text="РЕЖИМ СОХРАНЕНИЯ", 
                       variable=self.save_mode,
                       command=self.toggle_save_mode).pack(side=tk.LEFT)
        
        ttk.Label(save_frame, text="🟢", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        
        # Кнопки управления
        ttk.Button(left, text="НАРИСОВАТЬ", command=self.draw).pack(pady=5)
        ttk.Button(left, text="СОХРАНИТЬ ТЕКУЩУЮ", command=self.save_current).pack(pady=5)
        ttk.Button(left, text="ОЧИСТИТЬ ВСЕ", command=self.clear_all).pack(pady=5)
        ttk.Button(left, text="СБРОС ТОЧЕК", command=self.reset).pack(pady=5)
        
        # Информация о сохраненных кривых
        self.info_label = ttk.Label(left, text="Сохранено: 0", font=('Arial', 9))
        self.info_label.pack(pady=10)
        
        # Холст (теперь 700x600)
        self.canvas = tk.Canvas(self.root, width=700, height=600, bg='white')
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def get_matrix(self):
        if self.method.get() == "ermit":
            return ermit_matrix
        elif self.method.get() == "bezye":
            return bezye_matrix
        else:
            return v_spline_matrix
    
    def get_values(self):
        try:
            vector_x = [float(entry.get()) for entry in self.x_entries]
            vector_y = [float(entry.get()) for entry in self.y_entries]
            return vector_x, vector_y
        except:
            return None, None
    

    def world_to_pixel(self, x, y):
        """Преобразование мировых координат в пиксели"""
        w, h = 700, 600
        margin = 50
        px = margin + (x - self.x_min) * (w - 2*margin) / (self.x_max - self.x_min)
        py = h - margin - (y - self.y_min) * (h - 2*margin) / (self.y_max - self.y_min)
        return px, py
    

    def draw_grid(self):
        """Рисует координатную сетку с разметкой"""
        w, h = 700, 600
        margin = 50
        
        self.canvas.delete("grid")
        
        # Рисуем сетку
        for x in range(int(self.x_min), int(self.x_max) + 1):
            px, _ = self.world_to_pixel(x, 0)
            if margin <= px <= w - margin:
                self.canvas.create_line(px, margin, px, h - margin, 
                                       fill='lightgray', width=1, tags='grid')
                self.canvas.create_text(px, h - margin + 20, 
                                       text=str(x), fill='black', tags='grid')
        
        for y in range(int(self.y_min), int(self.y_max) + 1):
            _, py = self.world_to_pixel(0, y)
            if margin <= py <= h - margin:
                self.canvas.create_line(margin, py, w - margin, py, 
                                       fill='lightgray', width=1, tags='grid')
                self.canvas.create_text(margin - 20, py, 
                                       text=str(y), fill='black', tags='grid')
        
        # Рисуем оси
        x0, y0 = self.world_to_pixel(0, 0)
        self.canvas.create_line(margin, y0, w - margin, y0, fill='black', width=2, tags='grid')
        self.canvas.create_line(x0, margin, x0, h - margin, fill='black', width=2, tags='grid')
        
        # Стрелки на осях
        self.canvas.create_polygon(w - margin - 10, y0 - 5, w - margin, y0, 
                                  w - margin - 10, y0 + 5, fill='black', tags='grid')
        self.canvas.create_polygon(x0 - 5, margin + 10, x0, margin, 
                                  x0 + 5, margin + 10, fill='black', tags='grid')
        
        # Подписи осей
        self.canvas.create_text(w - margin + 15, y0 - 10, text="X", 
                               font=('Arial', 12, 'bold'), tags='grid')
        self.canvas.create_text(x0 + 10, margin - 15, text="Y", 
                               font=('Arial', 12, 'bold'), tags='grid')
        
        # Начало координат
        self.canvas.create_oval(x0-3, y0-3, x0+3, y0+3, fill='black', tags='grid')
    

    def draw_curve(self, method, vector_x, vector_y, color='blue', tags='curve'):
        """Рисует одну кривую заданным цветом"""
        if method == "ermit":
            matrix = ermit_matrix
        elif method == "bezye":
            matrix = bezye_matrix
        else:
            matrix = v_spline_matrix
        
        points = ermit_interpolation(vector_x, vector_y, matrix)
        
        pixel_points = []
        for x, y in points:
            px, py = self.world_to_pixel(x, y)
            if 0 <= px <= 700 and 0 <= py <= 600:
                pixel_points.append((px, py))
        
        if len(pixel_points) > 1:
            self.canvas.create_line(pixel_points, fill=color, width=2, tags=tags)
    

    def draw(self):
        """Отрисовка всего"""
        self.canvas.delete("all")
        self.draw_grid()
        
        # Если режим сохранения выключен - рисуем только текущую кривую
        if not self.save_mode.get():
            vector_x, vector_y = self.get_values()
            if vector_x is not None:
                self.draw_curve(self.method.get(), vector_x, vector_y, 'blue', 'current_curve')
        
        # Если режим сохранения включен - рисуем все сохраненные кривые
        else:
            # Рисуем все сохраненные кривые
            for i, (method, vx, vy, color) in enumerate(self.saved_curves):
                self.draw_curve(method, vx, vy, color, f'saved_{i}')
        
        # Всегда рисуем опорные точки текущей кривой (для наглядности)
        vector_x, vector_y = self.get_values()
        if vector_x is not None:
            for i, (x, y) in enumerate(zip(vector_x, vector_y)):
                px, py = self.world_to_pixel(x, y)
                if 0 <= px <= 700 and 0 <= py <= 600:
                    self.canvas.create_rectangle(px-6, py-6, px+6, py+6, 
                                                fill='red', outline='darkred', width=2,
                                                tags='current_points')
                    self.canvas.create_text(px, py-20, text=f"P{i}", 
                                           fill='red', font=('Arial', 10, 'bold'),
                                           tags='current_points')
    

    def save_current(self):
        """Сохраняет текущую кривую"""
        vector_x, vector_y = self.get_values()
        if vector_x is None:
            return
        
        # Добавляем в список сохраненных
        color = self.colors[self.color_index % len(self.colors)]
        self.saved_curves.append((self.method.get(), vector_x.copy(), vector_y.copy(), color))
        self.color_index += 1
        
        # Обновляем информацию
        self.info_label.config(text=f"Сохранено: {len(self.saved_curves)}")
        
        self.draw()
    

    def clear_all(self):
        """Очищает все сохраненные кривые"""
        self.saved_curves = []
        self.color_index = 0
        self.info_label.config(text="Сохранено: 0")
        self.draw()
    
    def toggle_save_mode(self):
        """Переключает режим сохранения"""
        self.draw()
    
    def reset(self):
        """Сброс полей к начальным значениям"""
        for i, entry in enumerate(self.x_entries):
            entry.delete(0, tk.END)
            entry.insert(0, str(i))
        for i, entry in enumerate(self.y_entries):
            entry.delete(0, tk.END)
            entry.insert(0, str(i))
        self.draw()


root = tk.Tk()
app = CurveDrawer(root)
root.mainloop()