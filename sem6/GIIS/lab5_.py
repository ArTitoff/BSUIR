import tkinter as tk
import math

class SimpleZoomGrid:
    def __init__(self, root):
        self.root = root
        self.root.title("Сетка с зумом")
        self.x = 0
        self.y = 0
        self.offset_x = 0
        self.offset_y = 0
        self.window_width = 1600
        self.window_height = 1200
        
        # Размеры сетки (количество клеток)
        self.grid_cols = 200
        self.grid_rows = 100
        self.cell_size = 50

        self.polygons = []
        self.polygons_vertex = []
        self.lines = []
        
        # Массив для хранения закрашенных клеток (True - закрашена)
        self.filled_cells = [[False] * self.grid_cols for _ in range(self.grid_rows)]

        btn_frame = tk.Frame(root, bg='lightgray')
        btn_frame.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

        create_polygon_button = tk.Button(btn_frame, text="Построить полигон", command=self.create_polygon)
        create_polygon_button.pack(pady=5)
        end_polygon_button = tk.Button(btn_frame, text="Закончить полигон", command=self.end_poligon)
        end_polygon_button.pack(pady=5)
        clear_button = tk.Button(btn_frame, text="Очистить всё", command=self.clear_all)
        clear_button.pack(pady=5)
        
        # Новые кнопки
        check_convex_button = tk.Button(btn_frame, text="Проверить выпуклость", command=self.check_convexity)
        check_convex_button.pack(pady=5)
        show_normals_button = tk.Button(btn_frame, text="Показать нормали", command=self.show_normals)
        show_normals_button.pack(pady=5)


        convex_frame = tk.Frame(btn_frame, bg='lightgray')
        convex_frame.pack(fill=tk.X, pady=30)

        convex_label = tk.Label(convex_frame, text="Выпуклые оболочки:", bg='lightgray')
        convex_label.pack()

        graham_button = tk.Button(convex_frame, text="Грэхема", command=lambda: self.build_convex_hull_graham_or_jarvis(False))
        graham_button.pack(fill=tk.X)

        jarvis_button = tk.Button(convex_frame, text="Джарвиса", command=lambda: self.build_convex_hull_graham_or_jarvis(True))
        jarvis_button.pack(fill=tk.X)

        convex_frame = tk.Frame(btn_frame, bg='lightgray')
        convex_frame.pack(fill=tk.X, pady=30)

        convex_label = tk.Label(convex_frame, text="Линии и точки:", bg='lightgray')
        convex_label.pack()

        create_line_button = tk.Button(convex_frame, text="Построить линию", command=self.create_line)
        create_line_button.pack(fill=tk.X)

        intersection_button = tk.Button(convex_frame, text="Найти пересечение", command=self.line_intersection)
        intersection_button.pack(fill=tk.X)

        # После существующих кнопок добавьте:

        # Фрейм для ввода точки
        point_frame = tk.Frame(btn_frame, bg='lightgray')
        point_frame.pack(fill=tk.X, pady=10)

        point_label = tk.Label(point_frame, text="Проверка точки:", bg='lightgray')
        point_label.pack()

        coord_frame = tk.Frame(point_frame, bg='lightgray')
        coord_frame.pack()

        tk.Label(coord_frame, text="X:", bg='lightgray').pack(side=tk.LEFT)
        self.point_x_entry = tk.Entry(coord_frame, width=5)
        self.point_x_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(coord_frame, text="Y:", bg='lightgray').pack(side=tk.LEFT)
        self.point_y_entry = tk.Entry(coord_frame, width=5)
        self.point_y_entry.pack(side=tk.LEFT, padx=2)

        check_point_button = tk.Button(point_frame, text="Проверить точку", command=self.check_point_in_polygon)
        check_point_button.pack(fill=tk.X, pady=5)

        self.canvas = tk.Canvas(
            root, 
            width=self.window_width, 
            height=self.window_height, 
            bg='white'
        )
        self.canvas.pack()
        
        # Привязываем события
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Button-4>", self.zoom)
        self.canvas.bind("<Button-5>", self.zoom)
        self.canvas.bind("<ButtonPress-3>", self.on_press)  
        self.canvas.bind("<B3-Motion>", self.on_drag)
        
        # Привязываем события клавиатуры
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
        
        self.draw_grid()
    
    def create_polygon(self):
        self.canvas.bind("<Button-1>", self.fill_cell) 
        self.polygons.append([])
        self.polygons_vertex.append([])
    
    def create_polygon_line(self, grid_x, grid_y):
        if len(self.polygons[-1]) > 0:
            x1, y1 = self.polygons[-1][-1]  # последняя точка
            x2, y2 = grid_x, grid_y
            
            points = self.dda_algorithm(x1, y1, x2, y2)
            
            # Добавляем ТОЛЬКО новые точки, исключая первую (она уже есть)
            for point in points[1:]:  # пропускаем первую точку
                self.polygons[-1].append(point)
                self.filled_cells[point[1]][point[0]] = True
        else:
            # Первая точка полигона
            self.polygons[-1].append((grid_x, grid_y))
            self.filled_cells[grid_y][grid_x] = True
    
    def end_poligon(self):
        """Завершает построение полигона и замыкает его"""
        self.canvas.unbind("<Button-1>")
        
        if len(self.polygons[-1]) > 2:  # Полигон должен иметь хотя бы 3 точки
            # Замыкаем полигон: соединяем последнюю точку с первой
            first_point = self.polygons[-1][0]
            last_point = self.polygons[-1][-1]
            
            # Рисуем линию от последней к первой
            points = self.dda_algorithm(last_point[0], last_point[1], first_point[0], first_point[1])
            
            # Добавляем точки замыкающей линии (пропускаем первую, т.к. это последняя точка полигона)
            for point in points[1:]:
                if point not in self.polygons[-1]:  # избегаем дублирования
                    self.polygons[-1].append(point)
                    self.filled_cells[point[1]][point[0]] = True
            
            # Удаляем дубликаты из полигона
            self.polygons[-1] = self.remove_duplicates(self.polygons[-1])
        
        self.draw_grid()
    
    def remove_duplicates(self, points):
        """Удаляет дублирующиеся подряд точки"""
        if not points:
            return points
        
        unique = []
        for point in points:
            if not unique or unique[-1] != point:
                unique.append(point)
        return unique
    
    def clear_all(self):
        self.polygons = []
        self.lines = []
        self.polygons_vertex = []
        self.filled_cells = [[False] * self.grid_cols for _ in range(self.grid_rows)]
        self.draw_grid()
    
    def fill_cell(self, event):
        """Закрашивает клетку при клике (для построения полигона)"""
        cell = self.get_cell_coords(event.x, event.y)
        
        if cell:  
            grid_x, grid_y = cell
            self.polygons_vertex[-1].append((grid_x, grid_y))
            # Не закрашиваем клетку, если она уже есть в полигоне
            if (grid_x, grid_y) not in self.polygons[-1]:
                self.create_polygon_line(grid_x, grid_y)
                self.draw_grid()
    
    def get_cell_coords(self, x, y):
        """Преобразует координаты мыши в индексы клетки сетки"""
        grid_x = (x + self.offset_x) // self.cell_size
        grid_y = (y + self.offset_y) // self.cell_size
        
        # Проверяем, попадает ли в границы сетки
        if 0 <= grid_x < self.grid_cols and 0 <= grid_y < self.grid_rows:
            return (int(grid_x), int(grid_y))
        return None
    
    def on_key_press(self, event):
        """Обработка нажатий клавиш"""
        key = event.keysym
        print(f"Нажата клавиша: {key}")
        self.draw_grid()
    
    def get_cell_pixel_coords(self, grid_x, grid_y):
        """Преобразует индексы клетки в пиксельные координаты на холсте"""
        x1 = grid_x * self.cell_size - self.offset_x
        y1 = grid_y * self.cell_size - self.offset_y
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        return (x1, y1, x2, y2)
    
    def draw_grid(self):
        """Рисует сетку и закрашенные клетки"""
        self.canvas.delete("all")
        
        # Рисуем только видимые клетки
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x1, y1, x2, y2 = self.get_cell_pixel_coords(col, row)
                
                # Рисуем только если клетка видима на экране
                if (x2 > 0 and x1 < self.window_width and 
                    y2 > 0 and y1 < self.window_height):
                    
                    # Если клетка закрашена - рисуем черный квадрат
                    if self.filled_cells[row][col]:
                        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                   fill='black', outline='gray', width=1)
        
        # Рисуем только внутренние линии сетки
        # Вертикальные линии
        start_col = max(0, int(self.offset_x / self.cell_size))
        end_col = min(self.grid_cols, int((self.offset_x + self.window_width) / self.cell_size) + 1)
        
        for col in range(start_col, end_col):
            x = col * self.cell_size - self.offset_x
            if 0 <= x <= self.window_width:
                self.canvas.create_line(x, 0, x, self.window_height, fill='gray', width=1)
        
        # Горизонтальные линии
        start_row = max(0, int(self.offset_y / self.cell_size))
        end_row = min(self.grid_rows, int((self.offset_y + self.window_height) / self.cell_size) + 1)
        
        for row in range(start_row, end_row):
            y = row * self.cell_size - self.offset_y
            if 0 <= y <= self.window_height:
                self.canvas.create_line(0, y, self.window_width, y, fill='gray', width=1)
    
    def zoom(self, event):
        """Изменение масштаба"""
        old_size = self.cell_size
        
        # Определяем направление
        if event.num == 4 or (hasattr(event, 'delta') and event.delta > 0):
            self.cell_size = min(200, self.cell_size + 5)  # приближение
        elif event.num == 5 or (hasattr(event, 'delta') and event.delta < 0):
            self.cell_size = max(20, self.cell_size - 5)   # отдаление
        
        # Корректируем offset, чтобы зум был относительно курсора
        scale = self.cell_size / old_size
        self.offset_x = event.x - (event.x - self.offset_x) * scale
        self.offset_y = event.y - (event.y - self.offset_y) * scale
        
        # Ограничиваем offset после зума
        self._clamp_offset()
        
        self.draw_grid()
    
    def on_press(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_drag(self, event):
        # Вычисляем разницу в движении мыши
        dx = event.x - self.x
        dy = event.y - self.y
        
        # Перемещаем сетку в том же направлении, что и мышь
        new_offset_x = self.offset_x - dx
        new_offset_y = self.offset_y - dy
        
        # Проверяем, не выйдем ли мы за пределы сетки
        if self._is_offset_valid(new_offset_x, new_offset_y):
            self.offset_x = new_offset_x
            self.offset_y = new_offset_y
        
        # Обновляем последнюю позицию мыши
        self.x = event.x
        self.y = event.y
        
        self.draw_grid()
    
    def _clamp_offset(self):
        """Ограничивает offset, чтобы сетка всегда заполняла экран"""
        max_offset_x = self.grid_cols * self.cell_size - self.window_width
        max_offset_y = self.grid_rows * self.cell_size - self.window_height
        
        self.offset_x = max(0, min(self.offset_x, max_offset_x))
        self.offset_y = max(0, min(self.offset_y, max_offset_y))
    
    def _is_offset_valid(self, offset_x, offset_y):
        """Проверяет, не выходит ли offset за допустимые пределы"""
        max_offset_x = self.grid_cols * self.cell_size - self.window_width
        max_offset_y = self.grid_rows * self.cell_size - self.window_height
        
        return (0 <= offset_x <= max_offset_x and 
                0 <= offset_y <= max_offset_y)
    
    def dda_algorithm(self, x1, y1, x2, y2):
        """Улучшенный алгоритм ЦДА без дублирования"""
        points = []
        
        dx = x2 - x1
        dy = y2 - y1
        
        # Определяем количество шагов
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            return [(x1, y1)]
        
        # Шаг приращения
        x_inc = dx / steps
        y_inc = dy / steps
        
        x = x1
        y = y1
        
        for i in range(steps + 1):
            points.append((round(x), round(y)))  # используем round вместо int
            x += x_inc
            y += y_inc
        
        # Удаляем дубликаты, идущие подряд
        unique_points = []
        for point in points:
            if not unique_points or unique_points[-1] != point:
                unique_points.append(point)
        
        return unique_points
    

    
    def is_polygon_convex(self, points):
        """
        Проверка полигона на выпуклость по алгоритму из раздела 2.2
        Возвращает (True/False, знак всех векторных произведений)
        """
        if len(points) < 3:
            return False, 0
        
        n = len(points)
        sign = 0
        
        for i in range(n):
            # Получаем три последовательные вершины
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            x3, y3 = points[(i + 2) % n]
            
            # Векторы сторон
            v1x = x2 - x1
            v1y = y2 - y1
            v2x = x3 - x2
            v2y = y3 - y2
            
            # Векторное произведение (формула 2.1)
            cross = v1x * v2y - v1y * v2x
            
            if cross != 0:
                current_sign = 1 if cross > 0 else -1
                if sign == 0:
                    sign = current_sign
                elif sign != current_sign:
                    return False, 0  # вогнутый
        
        return True, sign
    
    def get_normal_to_edge(self, x1, y1, x2, y2, sign):
        """
        Находит вектор, перпендикулярный стороне (формула 2.2)
        и ориентирует его внутрь полигона
        """
        # Вектор стороны
        vx = x2 - x1
        vy = y2 - y1
        
        # Перпендикулярный вектор (формула 2.2)
        nx = -vy
        ny = vx
        
        # Нормализуем для отрисовки
        length = math.sqrt(nx*nx + ny*ny)
        if length != 0:
            nx = nx / length
            ny = ny / length
        
        # Ориентируем внутрь полигона
        # Если знак векторных произведений положительный, 
        # внутренние нормали ориентированы влево
        if sign > 0:
            return (nx, ny)
        else:
            return (-nx, -ny)
    
    def calculate_centroid(self, points):
        """Вычисляет центр масс полигона"""
        if not points:
            return None
        
        sum_x = sum(p[0] for p in points)
        sum_y = sum(p[1] for p in points)
        
        return (sum_x / len(points), sum_y / len(points))
    
    def check_convexity(self):
        """Проверяет выпуклость последнего полигона и выводит результат"""
        if not self.polygons_vertex:
            print("Нет полигонов для проверки")
            return
        
        last_polygon = self.polygons_vertex[-1]
        if len(last_polygon) < 3:
            print("Полигон должен содержать хотя бы 3 точки")
            return
        is_convex, sign = self.is_polygon_convex(last_polygon)
        
        if is_convex:
            print(f"✓ Полигон ВЫПУКЛЫЙ")
            print(f"  Количество точек: {len(last_polygon)}")
            if sign > 0:
                print(f"  Внутренние нормали ориентированы влево от контура")
            else:
                print(f"  Внутренние нормали ориентированы вправо от контура")
        else:
            print(f"✗ Полигон НЕ ВЫПУКЛЫЙ")
            print(f"  Количество точек: {len(last_polygon)}")
    
    def show_normals(self):
        """Отображает внутренние нормали для всех сторон выпуклых полигонов"""
        if not self.polygons_vertex:
            print("Нет полигонов для отображения нормалей")
            return
        
        # Сохраняем исходное состояние
        original_filled = [row[:] for row in self.filled_cells]
        
        # Создаем временный массив для нормалей
        normal_cells = [[False] * self.grid_cols for _ in range(self.grid_rows)]
        
        for polygon in self.polygons_vertex:
            if len(polygon) < 3:
                continue
            
            # Проверяем выпуклость
            is_convex, sign = self.is_polygon_convex(polygon)
            
            if is_convex:
                # Для каждой стороны полигона
                for i in range(len(polygon)):
                    x1, y1 = polygon[i]
                    x2, y2 = polygon[(i + 1) % len(polygon)]
                    
                    # Вычисляем нормаль к стороне
                    nx, ny = self.get_normal_to_edge(x1, y1, x2, y2, sign)
                    
                    # Находим середину стороны
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    
                    # Рисуем нормаль длиной 10 клеток
                    end_x = mid_x + nx * 3
                    end_y = mid_y + ny * 3
                    
                    # Получаем точки линии нормали
                    line_points = self.dda_algorithm(int(mid_x), int(mid_y), int(end_x), int(end_y))
                    
                    # Добавляем в временный массив
                    for point in line_points:
                        if 0 <= point[0] < self.grid_cols and 0 <= point[1] < self.grid_rows:
                            normal_cells[point[1]][point[0]] = True
        
        # Перерисовываем с нормалями
        self.draw_grid_with_normals(original_filled, normal_cells)
        
    
    def draw_grid_with_normals(self, original_filled, normal_cells):
        """Рисует сетку с нормалями"""
        self.canvas.delete("all")
        
        # Рисуем закрашенные клетки
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x1, y1, x2, y2 = self.get_cell_pixel_coords(col, row)
                
                if (x2 > 0 and x1 < self.window_width and 
                    y2 > 0 and y1 < self.window_height):
                    
                    # Обычные закрашенные клетки
                    if original_filled[row][col]:
                        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                   fill='black', outline='gray', width=1)
                    
                    # Клетки нормалей (красным)
                    if normal_cells[row][col]:
                        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                   fill='red', outline='gray', width=1)
        
        # Рисуем линии сетки
        # Вертикальные линии
        start_col = max(0, int(self.offset_x / self.cell_size))
        end_col = min(self.grid_cols, int((self.offset_x + self.window_width) / self.cell_size) + 1)
        
        for col in range(start_col, end_col):
            x = col * self.cell_size - self.offset_x
            if 0 <= x <= self.window_width:
                self.canvas.create_line(x, 0, x, self.window_height, fill='gray', width=1)
        
        # Горизонтальные линии
        start_row = max(0, int(self.offset_y / self.cell_size))
        end_row = min(self.grid_rows, int((self.offset_y + self.window_height) / self.cell_size) + 1)
        
        for row in range(start_row, end_row):
            y = row * self.cell_size - self.offset_y
            if 0 <= y <= self.window_height:
                self.canvas.create_line(0, y, self.window_width, y, fill='gray', width=1)



        # ==================== ВЫПУКЛЫЕ ОБОЛОЧКИ ====================

    def graham_scan(self, points):
        """
        Построение выпуклой оболочки методом обхода Грэхема
        points - список вершин (x, y)
        Возвращает список вершин выпуклой оболочки в порядке обхода
        """
        if len(points) < 3:
            return points[:]
        
        # Шаг 1: Поиск экстремальной точки p0 (с минимальной y, при равенстве - минимальной x)
        p0 = min(points, key=lambda p: (p[1], p[0]))
        
        # Шаг 2: Сортировка остальных точек по полярному углу относительно p0
        def polar_angle(p):
            # Вычисляем угол относительно p0
            dx = p[0] - p0[0]
            dy = p[1] - p0[1]
            return math.atan2(dy, dx)
        
        def distance(p):
            # Квадрат расстояния для разрешения коллизий
            dx = p[0] - p0[0]
            dy = p[1] - p0[1]
            return dx*dx + dy*dy
        
        # Сортируем точки по полярному углу, при равенстве угла - ближайшая первая
        sorted_points = sorted(points, key=lambda p: (polar_angle(p), distance(p)))
        
        # Удаляем p0 из начала (она будет добавлена в конце)
        if sorted_points[0] == p0:
            sorted_points.pop(0)
        
        # Шаг 3: Построение оболочки с использованием стека
        stack = [p0]
        
        for p in sorted_points:
            # Пока в стеке >=2 точек и последние две + текущая образуют правый поворот
            while len(stack) >= 2:
                p1 = stack[-2]
                p2 = stack[-1]
                # Проверяем направление поворота (векторное произведение)
                cross = (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0])
                if cross <= 0:  # Правый поворот или коллинеарны - удаляем последнюю точку
                    stack.pop()
                else:
                    break
            stack.append(p)
        
        return stack

    def jarvis_march(self, points):
        """
        Построение выпуклой оболочки методом Джарвиса (заворачивание подарка)
        points - список вершин (x, y)
        Возвращает список вершин выпуклой оболочки в порядке обхода
        """
        if len(points) < 3:
            return points[:]
        
        # Шаг 1: Поиск экстремальной точки p0 (с минимальной y, при равенстве - минимальной x)
        p0 = min(points, key=lambda p: (p[1], p[0]))
        
        hull = [p0]
        current = p0
        
        while True:
            # Ищем следующую точку с минимальным полярным углом относительно current
            next_point = None
            
            for p in points:
                if p == current:
                    continue
                
                if next_point is None:
                    next_point = p
                    continue
                
                # Сравниваем углы: проверяем, лежит ли p левее вектора current->next_point
                cross = (next_point[0] - current[0]) * (p[1] - current[1]) - \
                        (next_point[1] - current[1]) * (p[0] - current[0])
                
                if cross < 0:
                    # p левее - выбираем p
                    next_point = p
                elif cross == 0:
                    # Коллинеарны - выбираем более дальнюю
                    dist_next = (next_point[0] - current[0])**2 + (next_point[1] - current[1])**2
                    dist_p = (p[0] - current[0])**2 + (p[1] - current[1])**2
                    if dist_p > dist_next:
                        next_point = p
            
            # Если вернулись в начало - оболочка построена
            if next_point == hull[0]:
                break
            
            hull.append(next_point)
            current = next_point
        
        return hull


    def build_convex_hull_graham_or_jarvis(self, jarvis):
        """
        Построить выпуклую оболочку последнего полигона
        """
        if not self.polygons_vertex:
            print("Нет полигонов для построения выпуклой оболочки")
            return
        
        last_polygon = self.polygons_vertex[-1]
        if len(last_polygon) < 3:
            print(f"Полигон должен содержать хотя бы 3 точки. Сейчас: {len(last_polygon)}")
            return
        
        method = "Джарвиса" if jarvis else "Грэхема"
        print(f"Построение выпуклой оболочки методом {method}...")
        print(f"Исходные вершины ({len(last_polygon)}): {last_polygon}")
        
        hull = []
        # Строим выпуклую оболочку
        if jarvis:
            hull = self.jarvis_march(last_polygon)
        else:
            hull = self.graham_scan(last_polygon)
        
        print(f"Выпуклая оболочка ({len(hull)}): {hull}")
        
        # Очищаем текущий полигон и заменяем его выпуклой оболочкой
        self.clear_current_polygon()
        self.draw_convex_hull(hull)
        
        print("Выпуклая оболочка построена!")

    def clear_current_polygon(self):
        """
        Очищает текущий полигон (последний) из всех массивов
        """
        if self.polygons:
            # Удаляем все закрашенные клетки текущего полигона
            for point in self.polygons[-1]:
                self.filled_cells[point[1]][point[0]] = False
            
            # Удаляем полигон из списков
            self.polygons.pop()
            self.polygons_vertex.pop()
            
            # Добавляем новый пустой полигон
            self.polygons.append([])
            self.polygons_vertex.append([])

    def draw_convex_hull(self, hull):
        """
        Отрисовывает выпуклую оболочку
        hull - список вершин выпуклой оболочки
        """
        if len(hull) < 2:
            return
        
        # Добавляем вершины в polygons_vertex
        for vertex in hull:
            self.polygons_vertex[-1].append(vertex)
        
        # Рисуем стороны выпуклой оболочки
        for i in range(len(hull)):
            x1, y1 = hull[i]
            x2, y2 = hull[(i + 1) % len(hull)]
            
            # Рисуем линию между вершинами
            points = self.dda_algorithm(x1, y1, x2, y2)
            
            # Добавляем точки линии в polygons и закрашиваем
            for point in points:
                if point not in self.polygons[-1]:
                    self.polygons[-1].append(point)
                    self.filled_cells[point[1]][point[0]] = True
        
        self.draw_grid()


    def create_line(self):
        """Начать построение линии (ждем 2 клика)"""
        self.lines.append([])
        print("Режим построения линии. Нажмите первую точку...")
        self.canvas.bind("<Button-1>", self.fill_line_cell)

    def fill_line_cell(self, event):
        """Закрашивает клетку при клике (для построения линии из 2 точек)"""
        cell = self.get_cell_coords(event.x, event.y)
        
        if cell:  
            grid_x, grid_y = cell
            current_line = self.lines[-1]
            
            # Первый клик - устанавливаем первую точку
            if len(current_line) == 0:
                current_line.append((grid_x, grid_y))
                self.filled_cells[grid_y][grid_x] = True
                self.draw_grid()
                print(f"Первая точка: ({grid_x}, {grid_y})")
                print("Нажмите вторую точку...")
            
            # Второй клик - строим линию и завершаем
            else:
                x1, y1 = current_line[0]  # первая точка
                x2, y2 = grid_x, grid_y
                
                # Не строим линию в ту же точку
                if (x1, y1) == (x2, y2):
                    print("Нельзя построить линию из одной точки!")
                    return
                
                # Строим линию
                points = self.dda_algorithm(x1, y1, x2, y2)
                
                # Добавляем все точки линии 
                for point in points[1:]:
                    current_line.append(point)
                    self.filled_cells[point[1]][point[0]] = True
                
                self.draw_grid()
                print(f"Линия построена: от ({x1}, {y1}) до ({x2}, {y2})")
                print(f"Всего точек в линии: {len(current_line)}")
                
                # Завершаем режим построения
                self.canvas.unbind("<Button-1>")
                print("Режим построения линии завершен. Нажмите кнопку 'Построить линию' для новой линии.")


    # ==================== ПЕРЕСЕЧЕНИЕ ОТРЕЗКА СО СТОРОНОЙ ПОЛИГОНА ====================

    def line_intersection(self):
        """
        Находит пересечение последней построенной линии со сторонами полигонов
        и подсвечивает точки пересечения зеленым
        """
        if not self.lines:
            print("Нет построенных линий. Сначала постройте линию.")
            return
        
        if not self.polygons_vertex:
            print("Нет полигонов для проверки пересечения.")
            return
        
        # Берем последнюю построенную линию
        last_line = self.lines[-1]
        if len(last_line) < 2:
            print("Линия должна содержать хотя бы 2 точки.")
            return
        
        # Получаем концы отрезка
        x1, y1 = last_line[0]  # первая точка линии
        x2, y2 = last_line[-1]  # последняя точка линии
        
        print(f"Проверка пересечения отрезка ({x1},{y1})-({x2},{y2}) со сторонами полигонов...")
        
        # Сохраняем исходное состояние
        original_filled = [row[:] for row in self.filled_cells]
        
        # Создаем массив для точек пересечения
        intersection_cells = [[False] * self.grid_cols for _ in range(self.grid_rows)]
        
        # Проверяем пересечения со всеми полигонами
        intersection_count = 0
        for polygon_vertices in self.polygons_vertex:
            if len(polygon_vertices) < 3:
                continue
            
            # Проверяем каждую сторону полигона
            for i in range(len(polygon_vertices)):
                x3, y3 = polygon_vertices[i]
                x4, y4 = polygon_vertices[(i + 1) % len(polygon_vertices)]
                
                # Находим точку пересечения
                intersection = self.segment_intersection(x1, y1, x2, y2, x3, y3, x4, y4)
                
                if intersection:
                    ix, iy = intersection
                    # Проверяем, что точка в пределах сетки
                    if 0 <= ix < self.grid_cols and 0 <= iy < self.grid_rows:
                        intersection_cells[iy][ix] = True
                        intersection_count += 1
                        print(f"  Пересечение со стороной ({x3},{y3})-({x4},{y4}) в точке ({ix},{iy})")
        
        if intersection_count == 0:
            print("Пересечений не найдено.")
        else:
            print(f"Найдено {intersection_count} точек пересечения.")
        
        # Перерисовываем с подсветкой
        self.draw_grid_with_intersections(original_filled, intersection_cells)
        
        # Через 3 секунды возвращаем обычный вид
        self.root.after(3000, lambda: self.draw_grid())

    def segment_intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        Находит точку пересечения двух отрезков (x1,y1)-(x2,y2) и (x3,y3)-(x4,y4)
        Возвращает (x, y) если пересекаются, иначе None
        """
        # Вычисляем направляющие векторы
        dx1 = x2 - x1
        dy1 = y2 - y1
        dx2 = x4 - x3
        dy2 = y4 - y3
        
        # Вычисляем знаменатель
        denom = dx1 * dy2 - dy1 * dx2
        
        # Если знаменатель = 0, отрезки параллельны
        if abs(denom) < 1e-10:
            return None
        
        # Вычисляем параметры для точки пересечения
        t = ((x3 - x1) * dy2 - (y3 - y1) * dx2) / denom
        u = ((x3 - x1) * dy1 - (y3 - y1) * dx1) / denom
        
        # Проверяем, лежат ли точки пересечения на обоих отрезках
        if 0 <= t <= 1 and 0 <= u <= 1:
            # Вычисляем координаты точки пересечения
            ix = x1 + t * dx1
            iy = y1 + t * dy1
            return (round(ix), round(iy))
        
        return None

    def draw_grid_with_intersections(self, original_filled, intersection_cells):
        """Рисует сетку с подсвеченными точками пересечения"""
        self.canvas.delete("all")
        
        # Рисуем закрашенные клетки
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x1, y1, x2, y2 = self.get_cell_pixel_coords(col, row)
                
                if (x2 > 0 and x1 < self.window_width and 
                    y2 > 0 and y1 < self.window_height):
                    
                    # Обычные закрашенные клетки
                    if original_filled[row][col]:
                        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                fill='black', outline='gray', width=1)
                    
                    # Точки пересечения (зеленым)
                    if intersection_cells[row][col]:
                        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                fill='green', outline='gray', width=1)
        
        # Рисуем линии сетки
        self.draw_grid_lines_only()

    def draw_grid_lines_only(self):
        """Рисует только линии сетки"""
        # Вертикальные линии
        start_col = max(0, int(self.offset_x / self.cell_size))
        end_col = min(self.grid_cols, int((self.offset_x + self.window_width) / self.cell_size) + 1)
        
        for col in range(start_col, end_col):
            x = col * self.cell_size - self.offset_x
            if 0 <= x <= self.window_width:
                self.canvas.create_line(x, 0, x, self.window_height, fill='gray', width=1)
        
        # Горизонтальные линии
        start_row = max(0, int(self.offset_y / self.cell_size))
        end_row = min(self.grid_rows, int((self.offset_y + self.window_height) / self.cell_size) + 1)
        
        for row in range(start_row, end_row):
            y = row * self.cell_size - self.offset_y
            if 0 <= y <= self.window_height:
                self.canvas.create_line(0, y, self.window_width, y, fill='gray', width=1)


    # ==================== ПРИНАДЛЕЖНОСТЬ ТОЧКИ ПОЛИГОНУ ====================

    def check_point_in_polygon(self):
        """
        Проверяет принадлежность точки полигону (метод трассировки луча)
        """
        try:
            # Получаем координаты из полей ввода
            x = int(self.point_x_entry.get())
            y = int(self.point_y_entry.get())
        except ValueError:
            print("Ошибка: введите целые числа для координат точки")
            return
        
        if not self.polygons_vertex:
            print("Нет полигонов для проверки.")
            return
        
        point = (x, y)
        print(f"Проверка точки ({x}, {y}) на принадлежность полигонам...")
        
        # Сохраняем исходное состояние
        original_filled = [row[:] for row in self.filled_cells]
        
        # Создаем массив для подсветки точки
        point_cells = [[False] * self.grid_cols for _ in range(self.grid_rows)]
        
        # Проверяем для каждого полигона
        for i, polygon_vertices in enumerate(self.polygons_vertex):
            if len(polygon_vertices) < 3:
                continue
            
            is_inside = self.point_in_polygon(point, polygon_vertices)
            
            if is_inside:
                print(f"  Точка принадлежит полигону {i+1}")
                # Подсвечиваем точку
                if 0 <= x < self.grid_cols and 0 <= y < self.grid_rows:
                    point_cells[y][x] = True
            else:
                print(f"  Точка не принадлежит полигону {i+1}")
        
        # Перерисовываем с подсветкой
        self.draw_grid_with_point(original_filled, point_cells, point)
        
        # Через 3 секунды возвращаем обычный вид
        self.root.after(3000, lambda: self.draw_grid())

    def point_in_polygon(self, point, polygon):
        """
        Определяет принадлежность точки полигону методом трассировки луча
        point - (x, y)
        polygon - список вершин (x, y)
        Возвращает True если точка внутри или на границе
        """
        x, y = point
        n = len(polygon)
        inside = False
        
        for i in range(n):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % n]
            
            # Проверяем, лежит ли точка на границе
            if self.point_on_segment(point, (x1, y1), (x2, y2)):
                return True
            
            # Проверяем пересечение луча (вправо) со стороной
            # Условие: сторона пересекает горизонтальную линию y
            # и точка пересечения находится правее точки
            if ((y1 > y) != (y2 > y)):
                # Вычисляем x координату пересечения
                x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                if x_intersect > x:
                    inside = not inside
        
        return inside

    def point_on_segment(self, point, seg_start, seg_end):
        """
        Проверяет, лежит ли точка на отрезке
        """
        px, py = point
        x1, y1 = seg_start
        x2, y2 = seg_end
        
        # Проверяем коллинеарность
        cross = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
        if abs(cross) > 1e-10:
            return False
        
        # Проверяем, что точка в пределах отрезка
        if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2):
            return True
        return False

    def draw_grid_with_point(self, original_filled, point_cells, point):
        """Рисует сетку с подсвеченной точкой"""
        self.canvas.delete("all")
        
        px, py = point
        
        # Рисуем закрашенные клетки
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x1, y1, x2, y2 = self.get_cell_pixel_coords(col, row)
                
                if (x2 > 0 and x1 < self.window_width and 
                    y2 > 0 and y1 < self.window_height):
                    
                    # Обычные закрашенные клетки
                    if original_filled[row][col]:
                        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                fill='black', outline='gray', width=1)
                    
                    # Проверяемая точка (зеленым)
                    if point_cells[row][col]:
                        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                fill='green', outline='gray', width=1)
        
        # Рисуем линии сетки
        self.draw_grid_lines_only()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleZoomGrid(root)
    root.mainloop()