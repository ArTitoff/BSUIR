import tkinter as tk
from tkinter import ttk, messagebox


class LineDrawerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритмы отрезков")
        self.root.geometry("750x640")
        
        self.grid_size = 20
        self.cell_size = 25
        
        self.points = []
        self.step = 0
        self.algorithm = "ЦДА"
        self.is_debug = False
        self.x1 = self.y1 = self.x2 = self.y2 = 0
        
        self.setup_ui()
        self.draw_grid()
    
    def setup_ui(self):
        # Панель управления
        control = tk.Frame(self.root)
        control.pack(fill='x', padx=10, pady=5)
        
        # Алгоритмы
        tk.Label(control, text="Алгоритм:").grid(row=0, column=0, padx=5)
        self.algo_var = tk.StringVar(value="ЦДА")
        ttk.Combobox(control, textvariable=self.algo_var, 
                     values=["ЦДА", "Брезенхем", "Ву"], width=12,
                     state='readonly').grid(row=0, column=1, padx=5)
        
        # Координаты
        tk.Label(control, text="x1:").grid(row=0, column=2, padx=5)
        self.x1_entry = tk.Entry(control, width=4)
        self.x1_entry.grid(row=0, column=3, padx=2)
        
        
        tk.Label(control, text="y1:").grid(row=0, column=4, padx=5)
        self.y1_entry = tk.Entry(control, width=4)
        self.y1_entry.grid(row=0, column=5, padx=2)
        
        
        tk.Label(control, text="x2:").grid(row=0, column=6, padx=5)
        self.x2_entry = tk.Entry(control, width=4)
        self.x2_entry.grid(row=0, column=7, padx=2)
        
        
        tk.Label(control, text="y2:").grid(row=0, column=8, padx=5)
        self.y2_entry = tk.Entry(control, width=4)
        self.y2_entry.grid(row=0, column=9, padx=2)
        
        
        # Кнопки
        tk.Button(control, text="Построить", command=self.build_line, 
                 width=10).grid(row=0, column=10, padx=5)
        tk.Button(control, text="Очистить", command=self.clear_all,
                 width=10).grid(row=0, column=11, padx=5)
        
        # Отладка
        debug_frame = tk.Frame(control)
        debug_frame.grid(row=1, column=0, columnspan=12, pady=5)
        
        self.debug_start = tk.Button(debug_frame, text="▶ Отладка", command=self.start_debug,
                 width=10)
        self.debug_start.pack(side='left', padx=2)
        
        self.debug_step_btn = tk.Button(debug_frame, text="⏭ Шаг", command=self.debug_step,
                 width=10, state='disabled')
        self.debug_step_btn.pack(side='left', padx=2)
        
        self.debug_stop = tk.Button(debug_frame, text="⏹ Стоп", command=self.stop_debug,
                 width=10, state='disabled')
        self.debug_stop.pack(side='left', padx=2)
        
        # Холст
        self.canvas = tk.Canvas(self.root, 
                               width=self.grid_size*self.cell_size,
                               height=self.grid_size*self.cell_size,
                               bg='white')
        self.canvas.pack(pady=10)
        
        self.info = tk.Label(self.root, text="Введите координаты 0-19", 
                            relief='sunken')
        self.info.pack(fill='x', padx=10, pady=5)
    

    def draw_grid(self):
        """Сетка"""
        self.canvas.delete("all")
        
        for i in range(self.grid_size + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.grid_size*self.cell_size, fill='lightgray')
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.grid_size*self.cell_size, y, fill='lightgray')
        
        for i in range(self.grid_size):
            # X внизу
            x = i * self.cell_size + self.cell_size//2
            y_text = self.grid_size * self.cell_size - 10
            self.canvas.create_text(x, y_text, text=str(i), font=('Arial', 8))
            
            # Y слева
            y_canvas = (self.grid_size - 1 - i) * self.cell_size + self.cell_size//2
            self.canvas.create_text(10, y_canvas, text=str(i), font=('Arial', 8))
    

    def canvas_y(self, grid_y):
        return (self.grid_size - 1 - grid_y) * self.cell_size
    

    def draw_cell(self, x, y, brightness=1.0):
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            gray = int(255 * (1 - brightness))
            color = f'#{gray:02x}{gray:02x}{gray:02x}'
            
            x1 = x * self.cell_size
            y1 = self.canvas_y(y)
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            self.canvas.create_rectangle(x1, y1, x2, y2, 
                                        fill=color, outline='gray', width=1)
            
            
            text_color = 'white' if brightness > 0.7 else 'black'
            self.canvas.create_text(x1+self.cell_size//2, y1+self.cell_size//2,
                                    text=f"{x},{y}", font=('Arial', 7), fill=text_color)
    


    
    def sign(self, x):
        return 1 if x > 0 else (-1 if x < 0 else 0)
    
    def integer(self, x):
        return int(x)
    
    def dda_algorithm(self, x1, y1, x2, y2):
        """Алгоритм ЦДА"""
        points = []
        
        length = max(abs(x2 - x1), abs(y2 - y1))
        if length == 0:
            return [(x1, y1, 1.0)]
        
        dx = (x2 - x1) / length
        dy = (y2 - y1) / length
        
        x = x1 + 0.5 * self.sign(dx)
        y = y1 + 0.5 * self.sign(dy)
        points.append((self.integer(x), self.integer(y), 1.0))
        
        i = 0
        while i < length:
            x += dx
            y += dy
            points.append((self.integer(x), self.integer(y), 1.0))
            i += 1
        
        return points
    

    def bresenham_algorithm(self, x1, y1, x2, y2):
        """Алгоритм Брезенхема"""
        points = []
        
        x = x1
        y = y1
        dx = x2 - x1
        dy = y2 - y1
        e = 2 * dy - dx
        
        points.append((x, y, 1.0))
        
        i = 1
        while i <= dx:
            if e >= 0:
                y += 1
                e -= 2 * dx
            x += 1
            e += 2 * dy
            points.append((x, y, 1.0))
            i += 1
        return points
    

    def wu_algorithm(self, x1, y1, x2, y2):
        """Алгоритм Ву с отдельной обработкой особых случаев"""
        points = []
        
        # Горизонтальная линия
        if y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                points.append((x, y1, 1.0))
            return points
        
        # Вертикальная линия
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                points.append((x1, y, 1.0))
            return points
        
        # Линия под 45° (dx == dy)
        if abs(x2 - x1) == abs(y2 - y1):
            # Упорядочиваем точки
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            
            step_y = 1 if y2 > y1 else -1
            
            x = x1
            y = y1
            while x <= x2:
                points.append((x, y, 1.0))
                x += 1
                y += step_y
            return points
        
        x = x1
        y = y1
        dx = x2 - x1
        dy = y2 - y1
        k = dy / dx
        
        e = 2 * dy - dx
        
        # Первая точка
        ideal_y = y1 
        y_int = int(ideal_y)
        frac = ideal_y - y_int
        
        points.append((x, y_int, 1 - frac))
        points.append((x, y_int + 1, frac))
        
        i = 1
        while i <= dx:
            if e >= 0:
                y += 1
                e -= 2 * dx
            
            x += 1
            e += 2 * dy
            
            ideal_y = y1 + k * (x - x1)
            y_int = int(ideal_y)
            frac = ideal_y - y_int
            
            # Две точки с разной яркостью
            points.append((x, y_int, 1 - frac))
            points.append((x, y_int + 1, frac))
            
            i += 1
        
        return points
    
    
    def build_line(self):
        try:
            self.x1 = int(self.x1_entry.get())
            self.y1 = int(self.y1_entry.get())
            self.x2 = int(self.x2_entry.get())
            self.y2 = int(self.y2_entry.get())
            
            if not (self.x1 <= self.x2 and self.y1 <= self.y2):
                messagebox.showerror("Ошибка", "x2 >= x1, y2 >= y1")
                return
            
            if not all(0 <= c < self.grid_size for c in [self.x1, self.y1, self.x2, self.y2]):
                messagebox.showerror("Ошибка", f"Координаты не в диапазоне 0-{self.grid_size-1}")
                return
            
            self.clear_all()
            
            self.algorithm = self.algo_var.get()
            if self.algorithm == "ЦДА":
                self.points = self.dda_algorithm(self.x1, self.y1, self.x2, self.y2)
            elif self.algorithm == "Брезенхем":
                self.points = self.bresenham_algorithm(self.x1, self.y1, self.x2, self.y2)
            else:
                self.points = self.wu_algorithm(self.x1, self.y1, self.x2, self.y2)
            
            # Рисуем все точки
            for x, y, brightness in self.points:
                self.draw_cell(x, y, brightness)
            
            # Начало и конец ярче
            self.draw_cell(self.x1, self.y1, 0.9)  # Темно-серый
            self.draw_cell(self.x2, self.y2, 0.7)  # Серый
            
            self.info.config(text=f"{self.algorithm}: ({self.x1},{self.y1})→({self.x2},{self.y2})")
            
        except:
            messagebox.showerror("Ошибка", "Введите целые числа")
    

    def start_debug(self):
        if not self.points:
            messagebox.showwarning("Внимание", "Сначала постройте линию")
            return
        
        self.is_debug = True
        self.step = 0
        
        self.debug_step_btn.config(state='normal')
        self.debug_stop.config(state='normal')
        self.debug_start.config(state='disabled')
        
        self.draw_grid()
        
        
        self.info.config(text="Отладка")
    

    def debug_step(self):
        if not self.is_debug or self.step >= len(self.points):
            return
        
        x, y, brightness = self.points[self.step]
        self.draw_cell(x, y, brightness)
        
        self.step += 1
        
        info = f"Шаг {self.step}: ({x},{y}) яркость={brightness:.2f}"
        
        self.info.config(text=info)
        
        if self.step >= len(self.points):
            self.is_debug = False
            self.draw_cell(self.x2, self.y2, 0.7)
            self.info.config(text="Отладка завершена")
    

    def stop_debug(self):
        self.is_debug = False
        self.step = 0
        
        self.debug_step_btn.config(state='disabled')
        self.debug_stop.config(state='disabled')
        self.debug_start.config(state='normal')
        
        self.draw_grid()
        for x, y, brightness in self.points:
            self.draw_cell(x, y, brightness)
        self.draw_cell(self.x1, self.y1, 0.9)
        self.draw_cell(self.x2, self.y2, 0.7)
        
        self.info.config(text="Отладка остановлена")
    

    def clear_all(self):
        self.draw_grid()
        self.points = []
        self.step = 0
        self.is_debug = False
        
        self.debug_step_btn.config(state='disabled')
        self.debug_stop.config(state='disabled')
        self.debug_start.config(state='normal')
        
        self.info.config(text="Готов к работе")


if __name__ == "__main__":
    root = tk.Tk()
    app = LineDrawerApp(root)
    root.mainloop()