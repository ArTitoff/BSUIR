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
        self.algorithm = "Окружность"
        self.is_debug = False
        self.x1 = self.y1 = self.x2 = self.y2 = 0
        
        self.setup_ui()
        self.draw_grid()
    
    def setup_ui(self):
 
        control = tk.Frame(self.root)
        control.pack(fill='x', padx=10, pady=5)
        

        tk.Label(control, text="Алгоритм:").grid(row=0, column=0, padx=5)
        self.algo_var = tk.StringVar(value="Окружность")
        self.algo_combo = ttk.Combobox(control, textvariable=self.algo_var, 
                     values=["Окружность", "Эллипс", "Гипербола", "Парабола"], width=12,
                     state='readonly')
        self.algo_combo.grid(row=0, column=1, padx=5)
        self.algo_combo.bind('<<ComboboxSelected>>', self.update_input_fields)
        
        # Фрейм для динамических полей ввода
        self.input_frame = tk.Frame(control)
        self.input_frame.grid(row=0, column=2, columnspan=5, padx=5, sticky='w')
        
        self.create_circle_inputs()
        
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
    
    def create_circle_inputs(self):
        """Создает поля ввода для окружности"""
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.input_frame, text="R:").pack(side='left', padx=2)
        self.x1_entry = tk.Entry(self.input_frame, width=4)
        self.x1_entry.pack(side='left', padx=2)
        self.x1_entry.insert(0, "8")
        
        self.y1_entry = None
        self.x2_entry = None
    
    def create_ellipse_inputs(self):
        """Создает поля ввода для эллипса"""
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.input_frame, text="a:").pack(side='left', padx=2)
        self.x1_entry = tk.Entry(self.input_frame, width=4)
        self.x1_entry.pack(side='left', padx=2)
        self.x1_entry.insert(0, "8")
        
        tk.Label(self.input_frame, text="b:").pack(side='left', padx=2)
        self.y1_entry = tk.Entry(self.input_frame, width=4)
        self.y1_entry.pack(side='left', padx=2)
        self.y1_entry.insert(0, "5")
        
        self.x2_entry = None
    
    def create_hyperbola_inputs(self):
        """Создает поля ввода для гиперболы"""
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.input_frame, text="a:").pack(side='left', padx=2)
        self.x1_entry = tk.Entry(self.input_frame, width=4)
        self.x1_entry.pack(side='left', padx=2)
        self.x1_entry.insert(0, "3")
        
        tk.Label(self.input_frame, text="b:").pack(side='left', padx=2)
        self.y1_entry = tk.Entry(self.input_frame, width=4)
        self.y1_entry.pack(side='left', padx=2)
        self.y1_entry.insert(0, "5")
        
        self.x2_entry = None
    
    def create_parabola_inputs(self):
        """Создает поля ввода для параболы"""
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.input_frame, text="p:").pack(side='left', padx=2)
        self.x1_entry = tk.Entry(self.input_frame, width=4)
        self.x1_entry.pack(side='left', padx=2)
        self.x1_entry.insert(0, "2")
        
        self.y1_entry = None
        self.x2_entry = None
    
    def update_input_fields(self, event=None):
        """Обновляет поля ввода при смене алгоритма"""
        algorithm = self.algo_var.get()
        
        if algorithm == "Окружность":
            self.create_circle_inputs()
        elif algorithm == "Эллипс":
            self.create_ellipse_inputs()
        elif algorithm == "Гипербола":
            self.create_hyperbola_inputs()
        elif algorithm == "Парабола":
            self.create_parabola_inputs()

    def draw_grid(self):
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
        
        points.append((self.integer(x), self.integer(y)))
        
        while x < 19 and y < 19:
            DH = b2 * (x + 1) * (x + 1) - a2 * y * y - a2 * b2
            
            DV = b2 * x * x - a2 * (y + 1) * (y + 1) - a2 * b2
            
            DD = b2 * (x + 1) * (x + 1) - a2 * (y + 1) * (y + 1) - a2 * b2
            
            min_abs = min(abs(DH), abs(DV), abs(DD))
            
            if abs(DD) == min_abs:
                x = x + 1
                y = y + 1
            elif abs(DH) == min_abs:
                x = x + 1
            else:
                y = y + 1
            
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
        
        # F(x,y) = y² - 2px
        points.append((self.integer(x), self.integer(y)))
        
        while x < 19:
            
            Dh = y * y - p2 * (x + 1)
            
            Dd = (y + 1) * (y + 1) - p2 * (x + 1)
        
            if abs(Dh) < abs(Dd):
                x = x + 1
            else:
                x = x + 1
                y = y + 1
            
            points.append((self.integer(x), self.integer(y)))
        
        return points   
    

    def build_line_2(self):
        try:
            self.clear_all()
            self.algorithm = self.algo_var.get()
            
            if self.algorithm == "Окружность":
                self.x1 = int(self.x1_entry.get())
                self.points = self.circle(self.x1)
            elif self.algorithm == "Эллипс":
                self.x1 = int(self.x1_entry.get())
                self.y1 = int(self.y1_entry.get())
                self.points = self.ellipse(self.x1, self.x1, self.y1)
            elif self.algorithm == "Гипербола":
                self.x1 = int(self.x1_entry.get())
                self.y1 = int(self.y1_entry.get())
                self.points = self.hyperbola(self.x1, self.y1)
            else:  # Парабола
                self.x1 = int(self.x1_entry.get())
                self.points = self.parabola(self.x1)

            # Рисуем все точки
            for x, y in self.points:
                self.draw_cell(x, y)
            
            self.info.config(text=f"{self.algorithm}: параметры введены")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Введите целые числа: {str(e)}")
    

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