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
        self.algo_var = tk.StringVar(value="Окружность")
        ttk.Combobox(control, textvariable=self.algo_var, 
                     values=["Окружность", "Эллипс", "Гипербола", "Парабола"], width=12,
                     state='readonly').grid(row=0, column=1, padx=5)
        
        # Координаты
        tk.Label(control, text="R:").grid(row=0, column=2, padx=5)
        self.x1_entry = tk.Entry(control, width=4)
        self.x1_entry.grid(row=0, column=3, padx=2)
        
        
        tk.Label(control, text="a:").grid(row=0, column=4, padx=5)
        self.y1_entry = tk.Entry(control, width=4)
        self.y1_entry.grid(row=0, column=5, padx=2)
        
        
        tk.Label(control, text="b:").grid(row=0, column=6, padx=5)
        self.x2_entry = tk.Entry(control, width=4)
        self.x2_entry.grid(row=0, column=7, padx=2)
        
        
        # Кнопки
        tk.Button(control, text="Построить", command=self.build_line_2, 
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
    

    def draw_cell(self, x, y):
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            
            x1 = x * self.cell_size
            y1 = self.canvas_y(y)
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            self.canvas.create_rectangle(x1, y1, x2, y2, 
                                        fill='#000000', outline='gray', width=1)
            
            self.canvas.create_text(x1+self.cell_size//2, y1+self.cell_size//2,
                                    text=f"{x},{y}", font=('Arial', 7), fill='white')
    


    
    def sign(self, x):
        return 1 if x > 0 else (-1 if x < 0 else 0)
    
    def integer(self, x):
        return int(x)
    
    def circle(self, x1):
        points = []
        x = 0
        y = x1
        lim = 0
        delta = 2 - 2 * x1
        sigma = 0

        points.append((self.integer(x), self.integer(y)))

        while y > lim:
            if delta > 0:
                sigma = 2 * delta - 2 * x - 1
                if sigma > 0:
                    y = y - 1
                    delta = delta - 2 * y + 1
                else:
                    x = x + 1
                    y = y - 1
                    delta = delta + 2 * x - 2 * y + 2
            elif delta < 0:
                sigma = 2 * delta + 2 * y - 1
                if sigma > 0:
                   x = x + 1
                   y = y - 1
                   delta = delta + 2 * x - 2 * y + 2
                else:
                    x = x + 1
                    delta = delta + 2 * x + 1
            else:
                x = x + 1
                y = y - 1
                delta = delta + 2 * x - 2 * y + 2

            print(1)  
            points.append((self.integer(x), self.integer(y)))
        return points
    

    def ellipse(self, x1, a, b):
        points = []
        x = 0
        y = x1
        lim = 0
        delta = 2 - 2 * x1
        sigma = 0

        points.append((self.integer(x), self.integer(y)))

        while y > lim:
            if delta > 0:
                sigma = 2 * delta - 2 * x * b**2 - 1
                if sigma > 0:
                    y = y - 1
                    delta = delta + a**2 *(1 - 2*y)
                else:
                    x = x + 1
                    y = y - 1
                    delta = delta + b**2 * (2 * x + 1) + a**2 *(1 - 2*y)
            elif delta < 0:
                sigma = 2 * delta + 2 * y * a**2 - 1
                if sigma > 0:
                   x = x + 1
                   y = y - 1
                   delta = delta + b**2 * (2 * x + 1) + a**2 *(1 - 2*y)
                else:
                    x = x + 1
                    delta = delta + b**2 * (2 * x + 1)
            else:
                x = x + 1
                y = y - 1
                delta = delta + b**2 * (2 * x + 1) + a**2 *(1 - 2*y)

            print(1)  
            points.append((self.integer(x), self.integer(y)))
        return points
    

    def hyperbola(self, a, b):
        """
        Алгоритм Брезенхема для гиперболы x²/a² - y²/b² = 1
        """
        points = []
        x = a
        y = 0
        a2 = a * a
        b2 = b * b
        
        # НАЧАЛЬНОЕ ЗНАЧЕНИЕ ОШИБКИ - как в методичке для эллипса, но с другими знаками
        # Для точки (a, 0): D = b²*a² - a²*0² - a²b² = 0
        D = 0
        points.append((self.integer(x), self.integer(y)))
        
        # ПЕРВАЯ ЧАСТЬ - пока |наклон| > 1? (для гиперболы по-другому)
        # Гипербола в первом квадранте: x растет, y растет
        while x < 15 and y < 15:
            # Вычисляем ошибки для трех кандидатов
            # Горизонтальный (x+1, y)
            DH = b2 * (x + 1) * (x + 1) - a2 * y * y - a2 * b2
            
            # Вертикальный (x, y+1)
            DV = b2 * x * x - a2 * (y + 1) * (y + 1) - a2 * b2
            
            # Диагональный (x+1, y+1)
            DD = b2 * (x + 1) * (x + 1) - a2 * (y + 1) * (y + 1) - a2 * b2
            
            # Выбираем пиксель с МИНИМАЛЬНОЙ абсолютной ошибкой
            min_abs = min(abs(DH), abs(DV), abs(DD))
            
            if abs(DD) == min_abs:
                x = x + 1
                y = y + 1
                D = DD
            elif abs(DH) == min_abs:
                x = x + 1
                D = DH
            else:
                y = y + 1
                D = DV
            
            points.append((self.integer(x), self.integer(y)))
        
        return points

    def parabola(self, p):
        """
        Алгоритм Брезенхема для параболы y² = 2px
        По аналогии с алгоритмом окружности/эллипса
        """
        points = []
        x = 0
        y = 0
        p2 = 2 * p
        
        # Начальное значение ошибки D
        # F(x,y) = y² - 2px
        D = 0  # в точке (0,0)
        points.append((self.integer(x), self.integer(y)))
        
        while x < 19:
            # Для параболы рассматриваем ГОРИЗОНТАЛЬНЫЙ (x+1, y) и ДИАГОНАЛЬНЫЙ (x+1, y+1)
            
            # Ошибка для горизонтального пикселя
            Dh = y * y - p2 * (x + 1)
            
            # Ошибка для диагонального пикселя
            Dd = (y + 1) * (y + 1) - p2 * (x + 1)
            
            # Выбираем пиксель с МИНИМАЛЬНОЙ абсолютной ошибкой
            if abs(Dh) < abs(Dd):
                # Горизонтальный шаг
                x = x + 1
                D = Dh
            else:
                # Диагональный шаг
                x = x + 1
                y = y + 1
                D = Dd
            
            points.append((self.integer(x), self.integer(y)))
        
        return points   
    

    def build_line_2(self):
        try:
            self.x1 = int(self.x1_entry.get())
            self.y1 = int(self.y1_entry.get())
            self.x2 = int(self.x2_entry.get())
            

            print(1)
            self.clear_all()
            self.algorithm = self.algo_var.get()
            if self.algorithm == "Окружность":
                self.points = self.circle(self.x1)
            elif self.algorithm == "Эллипс":
                self.points = self.ellipse(self.x1, self.y1, self.x2)
            elif self.algorithm == "Гипербола":
                self.points = self.hyperbola(self.y1, self.x2)
            else:
                self.points = self.parabola(self.y1)

            print(21)
            # Рисуем все точки
            for x, y in self.points:
                self.draw_cell(x, y)
            print(31)
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
        
        x, y= self.points[self.step]
        self.draw_cell(x, y)
        
        self.step += 1
        
        info = f"Шаг {self.step}: ({x},{y})"
        
        self.info.config(text=info)
        
        if self.step >= len(self.points):
            self.is_debug = False
            self.draw_cell(self.x2, self.y2)
            self.info.config(text="Отладка завершена")
    

    def stop_debug(self):
        self.is_debug = False
        self.step = 0
        
        self.debug_step_btn.config(state='disabled')
        self.debug_stop.config(state='disabled')
        self.debug_start.config(state='normal')
        
        self.draw_grid()
        for x, y in self.points:
            self.draw_cell(x, y)
        
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