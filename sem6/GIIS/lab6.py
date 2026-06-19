import tkinter as tk
from tkinter import ttk
import math

class PolygonFiller:
    def __init__(self, root):
        self.root = root
        self.root.title("Закраска полигонов")
        
        # Параметры сетки (пиксели - это большие квадратики)
        self.window_width = 1200
        self.window_height = 800
        self.grid_cols = 40   # 40x30 пикселей (квадратиков)
        self.grid_rows = 30
        self.cell_size = 25   # размер одного квадратика в пикселях
        
        # Данные для отображения
        self.offset_x = 0
        self.offset_y = 0
        self.pixels = [[False] * self.grid_cols for _ in range(self.grid_rows)]  # закрашенные пиксели
        
        # Данные полигона
        self.polygon_vertices = []      # вершины полигона (в координатах сетки)
        self.polygon_pixels = []        # все пиксели полигона (граница)
        self.is_drawing = False
        
        # Переменные для панорамирования
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Создание интерфейса
        self.setup_ui()
        
        # Холст для рисования
        self.canvas = tk.Canvas(root, width=self.window_width, height=self.window_height, bg='white')
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Привязка событий
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_press)
        self.canvas.bind("<B3-Motion>", self.on_drag)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Button-4>", self.zoom)
        self.canvas.bind("<Button-5>", self.zoom)
        
        self.draw_grid()
    
    def setup_ui(self):
        """Создание панели управления"""
        control_panel = tk.Frame(self.root, bg='lightgray', width=200)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        tk.Label(control_panel, text="Построение полигона", font=('Arial', 12, 'bold'), bg='lightgray').pack(pady=10)
        
        # Кнопки построения
        tk.Button(control_panel, text="Начать полигон", command=self.start_polygon, bg='lightblue').pack(fill=tk.X, pady=5)
        tk.Button(control_panel, text="Закончить полигон", command=self.end_polygon, bg='lightblue').pack(fill=tk.X, pady=5)
        tk.Button(control_panel, text="Очистить всё", command=self.clear_all, bg='orange').pack(fill=tk.X, pady=5)
        
        tk.Label(control_panel, text="", bg='lightgray').pack(pady=5)
        tk.Label(control_panel, text="Алгоритмы закраски", font=('Arial', 12, 'bold'), bg='lightgray').pack(pady=10)
        
        # Выбор алгоритма
        self.algorithm_var = tk.StringVar(value="active_edge")
        algorithms = [
            ("1. Простой список ребер", "simple_list"),
            ("2. Активный список ребер (САР)", "active_edge"),
            ("3. Затравка (простая)", "flood_fill"),
            ("4. Затравка построчная", "scanline_fill")
        ]
        
        for text, value in algorithms:
            tk.Radiobutton(control_panel, text=text, variable=self.algorithm_var, 
                          value=value, bg='lightgray', anchor='w').pack(fill=tk.X, padx=10, pady=2)
        
        tk.Button(control_panel, text="ЗАКРАСИТЬ!", command=self.fill_polygon, 
                 bg='green', fg='white', font=('Arial', 10, 'bold')).pack(fill=tk.X, pady=15)
        
        tk.Label(control_panel, text="", bg='lightgray').pack(pady=5)
        tk.Label(control_panel, text="Управление:", font=('Arial', 10, 'bold'), bg='lightgray').pack()
        tk.Label(control_panel, text="ЛКМ - добавить вершину\nПКМ + drag - перемещение\nКолёсико - зум", 
                bg='lightgray', justify=tk.LEFT).pack(pady=5)
    
    def start_polygon(self):
        """Начало построения полигона"""
        self.polygon_vertices = []
        self.polygon_pixels = []
        self.is_drawing = True
        self.draw_grid()
    
    def end_polygon(self):
        """Завершение построения полигона (замыкание)"""
        if len(self.polygon_vertices) >= 3:
            # Замыкаем полигон
            self.close_polygon()
        self.is_drawing = False
        self.draw_grid()
    
    def close_polygon(self):
        """Замыкание полигона - соединяем последнюю вершину с первой"""
        if len(self.polygon_vertices) < 3:
            return
        
        # Добавляем ребро от последней вершины к первой
        last_vertex = self.polygon_vertices[-1]
        first_vertex = self.polygon_vertices[0]
        
        # Добавляем промежуточные пиксели по DDA
        for p in self.dda(last_vertex[0], last_vertex[1], first_vertex[0], first_vertex[1]):
            if p not in self.polygon_pixels:
                self.polygon_pixels.append(p)
    
    def on_click(self, event):
        """Обработка клика - добавление вершины полигона"""
        if not self.is_drawing:
            return
        
        # Получаем координаты пикселя (квадратика)
        col = int((event.x + self.offset_x) // self.cell_size)
        row = int((event.y + self.offset_y) // self.cell_size)
        
        if 0 <= col < self.grid_cols and 0 <= row < self.grid_rows:
            if self.polygon_vertices:
                # Добавляем ребро от последней вершины к новой
                last = self.polygon_vertices[-1]
                for p in self.dda(last[0], last[1], col, row):
                    if p not in self.polygon_pixels:
                        self.polygon_pixels.append(p)
            
            self.polygon_vertices.append((col, row))
            if (col, row) not in self.polygon_pixels:
                self.polygon_pixels.append((col, row))
            
            self.draw_grid()
    
    def dda(self, x1, y1, x2, y2):
        """Алгоритм DDA для растеризации линии"""
        steps = max(abs(x2 - x1), abs(y2 - y1))
        if steps == 0:
            return [(x1, y1)]
        
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps
        
        points = []
        x, y = x1, y1
        for _ in range(steps + 1):
            points.append((round(x), round(y)))
            x += dx
            y += dy
        
        # Удаляем дубликаты
        result = [points[0]]
        for p in points[1:]:
            if p != result[-1]:
                result.append(p)
        return result
    
    def clear_all(self):
        """Очистка всего"""
        self.polygon_vertices = []
        self.polygon_pixels = []
        self.pixels = [[False] * self.grid_cols for _ in range(self.grid_rows)]
        self.is_drawing = False
        self.draw_grid()
    
    # ==================== АЛГОРИТМЫ ЗАКРАСКИ ====================
    
    def fill_polygon(self):
        """Запуск выбранного алгоритма закраски"""
        if not self.polygon_pixels:
            print("Сначала постройте полигон!")
            return
        
        # Очищаем предыдущую закраску
        self.pixels = [[False] * self.grid_cols for _ in range(self.grid_rows)]
        
        # Запускаем выбранный алгоритм
        algorithm = self.algorithm_var.get()
        
        if algorithm == "simple_list":
            self.fill_simple_list()
        elif algorithm == "active_edge":
            self.fill_active_edge()
        elif algorithm == "flood_fill":
            self.fill_flood_fill()
        elif algorithm == "scanline_fill":
            self.fill_scanline()
        
        self.draw_grid()
    
    # -------------------- 1. Простой список ребер --------------------
    def fill_simple_list(self):
        """Алгоритм растровой развертки с упорядоченным списком ребер"""
        if len(self.polygon_vertices) < 3:
            return
        
        # Находим границы
        min_y = min(v[1] for v in self.polygon_vertices)
        max_y = max(v[1] for v in self.polygon_vertices)
        
        # Собираем все пересечения для каждой строки
        for y in range(min_y, max_y + 1):
            intersections = []
            
            # Проверяем каждое ребро
            for i in range(len(self.polygon_vertices)):
                x1, y1 = self.polygon_vertices[i]
                x2, y2 = self.polygon_vertices[(i + 1) % len(self.polygon_vertices)]
                
                # Пропускаем горизонтальные рёбра
                if y1 == y2:
                    continue
                
                # Проверяем пересечение со сканирующей строкой
                if (y1 <= y < y2) or (y2 <= y < y1):
                    # Вычисляем x пересечения
                    x = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                    intersections.append(x)
            
            # Сортируем пересечения
            intersections.sort()
            
            # Закрашиваем интервалы между парами
            for j in range(0, len(intersections), 2):
                if j + 1 < len(intersections):
                    x_start = int(math.ceil(intersections[j]))
                    x_end = int(math.floor(intersections[j + 1]))
                    for x in range(x_start, x_end + 1):
                        if 0 <= x < self.grid_cols and 0 <= y < self.grid_rows:
                            self.pixels[y][x] = True
    
    # -------------------- 2. Активный список ребер (САР) --------------------
    def fill_active_edge(self):
        """Алгоритм с упорядоченным списком ребер и списком активных ребер"""
        if len(self.polygon_vertices) < 3:
            return
        
        # Подготовка данных для каждого ребра
        edges = []
        for i in range(len(self.polygon_vertices)):
            x1, y1 = self.polygon_vertices[i]
            x2, y2 = self.polygon_vertices[(i + 1) % len(self.polygon_vertices)]
            
            if y1 == y2:
                continue  # пропускаем горизонтальные
            
            # Ориентируем ребро сверху вниз
            if y1 > y2:
                x1, y1, x2, y2 = x2, y2, x1, y1
            
            # y_max - наибольшая y, y_min - наименьшая y
            y_max = y2
            y_min = y1
            
            # x при y_min
            x_at_ymin = x1
            
            # dx/dy - приращение x при движении на 1 пиксель вниз
            dx = (x2 - x1) / (y2 - y1)
            
            edges.append({
                'y_max': y_max,
                'y_min': y_min,
                'x': x_at_ymin,
                'dx': dx
            })
        
        # Сортируем рёбра по y_min
        edges.sort(key=lambda e: e['y_min'])
        
        # Находим границы
        min_y = min(v[1] for v in self.polygon_vertices)
        max_y = max(v[1] for v in self.polygon_vertices)
        
        # Список активных рёбер
        active_edges = []
        edge_index = 0
        
        # Проходим по сканирующим строкам
        for y in range(min_y, max_y + 1):
            # Добавляем новые рёбра в САР
            while edge_index < len(edges) and edges[edge_index]['y_min'] == y:
                active_edges.append(edges[edge_index].copy())
                edge_index += 1
            
            # Сортируем активные рёбра по x
            active_edges.sort(key=lambda e: e['x'])
            
            # Закрашиваем интервалы между парами
            for j in range(0, len(active_edges), 2):
                if j + 1 < len(active_edges):
                    x_start = int(math.ceil(active_edges[j]['x']))
                    x_end = int(math.floor(active_edges[j + 1]['x']))
                    for x in range(x_start, x_end + 1):
                        if 0 <= x < self.grid_cols and 0 <= y < self.grid_rows:
                            self.pixels[y][x] = True
            
            # Обновляем x для активных рёбер и удаляем закончившиеся
            i = 0
            while i < len(active_edges):
                active_edges[i]['x'] += active_edges[i]['dx']
                if active_edges[i]['y_max'] == y + 1:
                    active_edges.pop(i)
                else:
                    i += 1
    
    # -------------------- 3. Простая затравка (Flood Fill) --------------------
    def fill_flood_fill(self):
        """Простой алгоритм заполнения с затравкой (рекурсивный)"""
        if not self.polygon_pixels:
            return
        
        # Находим внутреннюю точку (центр масс или первую не на границе)
        seed = self.find_seed_point()
        if not seed:
            print("Не удалось найти внутреннюю точку!")
            return
        
        # Используем стек вместо рекурсии (чтобы избежать RecursionError)
        stack = [seed]
        
        # Создаём копию границы для быстрой проверки
        boundary = set(self.polygon_pixels)
        
        visited = set()
        
        while stack:
            x, y = stack.pop()
            
            # Проверяем границы
            if not (0 <= x < self.grid_cols and 0 <= y < self.grid_rows):
                continue
            
            # Если пиксель уже закрашен или является границей
            if self.pixels[y][x] or (x, y) in boundary:
                continue
            
            # Закрашиваем
            self.pixels[y][x] = True
            
            # Добавляем 4-связных соседей
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append((nx, ny))
    
    def find_seed_point(self):
        """Поиск внутренней точки полигона"""
        if not self.polygon_vertices:
            return None
        
        # Берём центроид (среднее арифметическое вершин)
        cx = sum(v[0] for v in self.polygon_vertices) / len(self.polygon_vertices)
        cy = sum(v[1] for v in self.polygon_vertices) / len(self.polygon_vertices)
        
        seed = (int(cx), int(cy))
        
        # Проверяем, что точка внутри (через трассировку луча)
        if self.is_point_inside_polygon(seed[0], seed[1]):
            return seed
        
        # Если не внутри, ищем ближайшую
        for y in range(self.grid_rows):
            for x in range(self.grid_cols):
                if self.is_point_inside_polygon(x, y):
                    return (x, y)
        
        return None
    
    def is_point_inside_polygon(self, x, y):
        """Проверка принадлежности точки полигону (метод луча)"""
        if len(self.polygon_vertices) < 3:
            return False
        
        inside = False
        n = len(self.polygon_vertices)
        
        for i in range(n):
            x1, y1 = self.polygon_vertices[i]
            x2, y2 = self.polygon_vertices[(i + 1) % n]
            
            # Проверяем пересечение горизонтального луча с ребром
            if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                inside = not inside
        
        return inside
    
    # -------------------- 4. Построчная затравка --------------------
    def fill_scanline(self):
        """Построчный алгоритм заполнения с затравкой"""
        if not self.polygon_pixels:
            return
        
        # Находим затравку
        seed = self.find_seed_point()
        if not seed:
            print("Не удалось найти внутреннюю точку!")
            return
        
        boundary = set(self.polygon_pixels)
        stack = [seed]
        
        while stack:
            x, y = stack.pop()
            
            # Идём влево до границы
            x_left = x
            while x_left - 1 >= 0 and not self.pixels[y][x_left - 1] and (x_left - 1, y) not in boundary:
                x_left -= 1
            
            # Идём вправо до границы
            x_right = x
            while x_right + 1 < self.grid_cols and not self.pixels[y][x_right + 1] and (x_right + 1, y) not in boundary:
                x_right += 1
            
            # Закрашиваем интервал
            for xi in range(x_left, x_right + 1):
                self.pixels[y][xi] = True
            
            # Проверяем строку выше (y-1) на новые интервалы
            if y - 1 >= 0:
                xi = x_left
                while xi <= x_right:
                    # Пропускаем закрашенные и граничные
                    while xi <= x_right and (self.pixels[y - 1][xi] or (xi, y - 1) in boundary):
                        xi += 1
                    
                    if xi <= x_right:
                        # Нашли начало интервала - добавляем затравку
                        stack.append((xi, y - 1))
                        # Пропускаем интервал
                        while xi <= x_right and not self.pixels[y - 1][xi] and (xi, y - 1) not in boundary:
                            xi += 1
            
            # Проверяем строку ниже (y+1)
            if y + 1 < self.grid_rows:
                xi = x_left
                while xi <= x_right:
                    while xi <= x_right and (self.pixels[y + 1][xi] or (xi, y + 1) in boundary):
                        xi += 1
                    
                    if xi <= x_right:
                        stack.append((xi, y + 1))
                        while xi <= x_right and not self.pixels[y + 1][xi] and (xi, y + 1) not in boundary:
                            xi += 1
    
    # ==================== ОТРИСОВКА ====================
    
    def draw_grid(self):
        """Отрисовка сетки и полигона"""
        self.canvas.delete("all")
        
        # Рисуем закрашенные пиксели
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if self.pixels[row][col]:
                    x1 = col * self.cell_size - self.offset_x
                    y1 = row * self.cell_size - self.offset_y
                    if -self.cell_size < x1 < self.window_width and -self.cell_size < y1 < self.window_height:
                        self.canvas.create_rectangle(x1, y1, x1 + self.cell_size, y1 + self.cell_size, 
                                                     fill='black', outline='gray')
        
        # Рисуем границу полигона (красным)
        for x, y in self.polygon_pixels:
            x1 = x * self.cell_size - self.offset_x
            y1 = y * self.cell_size - self.offset_y
            if -self.cell_size < x1 < self.window_width and -self.cell_size < y1 < self.window_height:
                self.canvas.create_rectangle(x1, y1, x1 + self.cell_size, y1 + self.cell_size,
                                             fill='red', outline='darkred')
        
        # Рисуем вершины (синие квадратики)
        for x, y in self.polygon_vertices:
            x1 = x * self.cell_size - self.offset_x
            y1 = y * self.cell_size - self.offset_y
            if -self.cell_size < x1 < self.window_width and -self.cell_size < y1 < self.window_height:
                self.canvas.create_rectangle(x1, y1, x1 + self.cell_size, y1 + self.cell_size,
                                             fill='blue', outline='darkblue')
        
        # Рисуем линии сетки
        # Вертикальные линии
        first_col = max(0, int(self.offset_x // self.cell_size))
        last_col = min(self.grid_cols, int((self.offset_x + self.window_width) // self.cell_size) + 1)
        for col in range(first_col, last_col):
            x = col * self.cell_size - self.offset_x
            self.canvas.create_line(x, 0, x, self.window_height, fill='lightgray')
        
        # Горизонтальные линии
        first_row = max(0, int(self.offset_y // self.cell_size))
        last_row = min(self.grid_rows, int((self.offset_y + self.window_height) // self.cell_size) + 1)
        for row in range(first_row, last_row):
            y = row * self.cell_size - self.offset_y
            self.canvas.create_line(0, y, self.window_width, y, fill='lightgray')
    
    # ==================== УПРАВЛЕНИЕ ====================
    
    def on_press(self, event):
        """Начало панорамирования"""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def on_drag(self, event):
        """Панорамирование"""
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        
        self.offset_x -= dx
        self.offset_y -= dy
        
        # Ограничения
        max_offset_x = self.grid_cols * self.cell_size - self.window_width
        max_offset_y = self.grid_rows * self.cell_size - self.window_height
        self.offset_x = max(0, min(self.offset_x, max_offset_x))
        self.offset_y = max(0, min(self.offset_y, max_offset_y))
        
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        
        self.draw_grid()
    
    def zoom(self, event):
        """Зум колёсиком мыши"""
        old_cell_size = self.cell_size
        
        if event.num == 4 or event.delta > 0:
            self.cell_size = min(80, self.cell_size + 5)
        else:
            self.cell_size = max(15, self.cell_size - 5)
        
        # Корректировка offset для зума относительно курсора
        if hasattr(event, 'x') and hasattr(event, 'y'):
            ratio = self.cell_size / old_cell_size
            self.offset_x = event.x - (event.x - self.offset_x) * ratio
            self.offset_y = event.y - (event.y - self.offset_y) * ratio
        
        # Ограничения
        max_offset_x = self.grid_cols * self.cell_size - self.window_width
        max_offset_y = self.grid_rows * self.cell_size - self.window_height
        self.offset_x = max(0, min(self.offset_x, max_offset_x))
        self.offset_y = max(0, min(self.offset_y, max_offset_y))
        
        self.draw_grid()


if __name__ == "__main__":
    root = tk.Tk()
    app = PolygonFiller(root)
    root.mainloop()