import tkinter as tk
import math
from tkinter import filedialog
import json

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

        self.d = 50

        self.object = [
            [-3, -3, -3], [3, -3, -3], [3, 3, -3], [-3, 3, -3],  # задняя грань
            [-3, -3, 3], [3, -3, 3], [3, 3, 3], [-3, 3, 3]       # передняя грань
        ]

        self.edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # задняя грань
            [4, 5], [5, 6], [6, 7], [7, 4],  # передняя грань
            [0, 4], [1, 5], [2, 6], [3, 7]   # соединения
        ]
        
        # Находим центр фигуры
        self.center = self.find_center_by_average(self.object)
        self.coordinates_center = self.center.copy()
        print(f"Центр фигуры: {self.center}")
        
        self.transformed_points = self.object.copy()

        # Массив для хранения закрашенных клеток (True - закрашена)
        self.filled_cells = [[False] * self.grid_cols for _ in range(self.grid_rows)]

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
    

    def on_key_press(self, event):
        """Обработка нажатий клавиш"""
        key = event.keysym
        print(f"Нажата клавиша: {key}")

        # Перемещение
        if key == "Left":
            self.move(-1, 0, 0)
        elif key == "Right":
            self.move(1, 0, 0)
        elif key == "Up":
            self.move(0, 1, 0)
        elif key == "Down":
            self.move(0, -1, 0)
        elif key == "comma":
            self.move(0, 0, 1)
        elif key == "period":
            self.move(0, 0, -1)
        
        # Поворот
        elif key == "a":
            self.rotate('x', 10)
        elif key == "z":
            self.rotate('x', -10)
        elif key == "s":
            self.rotate('y', 10)
        elif key == "x":
            self.rotate('y', -10)
        elif key == "d":
            self.rotate('z', 10)
        elif key == "c":
            self.rotate('z', -10)
        
        # Масштабирование
        elif key == "plus" or key == "equal":
            self.scale(1.1, 1.1, 1.1)
        elif key == "minus":
            self.scale(0.9, 0.9, 0.9)
        elif key == "1":
            self.scale(1.2, 1, 1)
        elif key == "2":
            self.scale(1, 1.2, 1)
        elif key == "3":
            self.scale(1, 1, 1.2)
        
        # Отражение
        elif key == "r":
            self.reflect('x')
        elif key == "t":
            self.reflect('y')
        elif key == "y":
            self.reflect('z')
        
        # Перспектива
        elif key == "o":
            self.d = max(2, self.d - 1)
            print(f"d = {self.d}")
        elif key == "p":
            self.d = min(60, self.d + 1)
            print(f"d = {self.d}")
        
        # Сброс
        elif key == "space":
            self.reset()

        # загрузить с файла
        elif key == "l":
            self.load_from_file()
        
        self.draw_grid()
    
    
    def load_from_file(self):
        """Загружает модель из JSON файла"""
        file_path = filedialog.askopenfilename(
            title="Выберите JSON файл",
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")]
        )
        
        if not file_path:
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.object = data['vertices']
            self.edges = data['edges']
            self.reset()
            print(self.object)

            print(self.edges)
            print(f"Загружено: {len(self.object)} вершин, {len(self.edges)} рёбер")
            return True
            
        except Exception as e:
            print(f"Ошибка: {e}")
            tk.messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")
            return False
        
        
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
        
        self.draw_object()
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

    def find_center_by_average(self, points):

        if not points:
            return None
        
        n = len(points)
        center = [0, 0, 0]
        
        for point in points:
            center[0] += point[0]
            center[1] += point[1]
            center[2] += point[2]
        
        center[0] /= n
        center[1] /= n
        center[2] /= n
        
        return center
    
    def multiply_matrix_vector(self, matrix, vector):
        """Умножение матрицы 4x4 на вектор-строку 1x4"""
        result = [0, 0, 0, 0]
        for i in range(4):
            result[i] = (vector[0] * matrix[0][i] + 
                        vector[1] * matrix[1][i] + 
                        vector[2] * matrix[2][i] + 
                        vector[3] * matrix[3][i])
        return result


    def project_point(self, point_3d):
        """
        Проецирует одну 3D точку (x, y, z) в 2D
        """
        x, y, z = point_3d
        
        # Матрица проекции
        P = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 1/self.d],
            [0, 0, 0, 1]
        ]
        
        point_h = [x, y, z, 1]
        
        projected_h = self.multiply_matrix_vector(P, point_h)
        
        # x_2d = projected_h[0] 
        # y_2d = projected_h[1] 
        # return [x_2d, y_2d]
        w = projected_h[3]
        if w != 0:
            x_2d = projected_h[0] / w
            y_2d = projected_h[1] / w
            return [x_2d, y_2d]
        else:
            return [0, 0]  


    def scale(self, sx, sy, sz):
        """Масштабирование относительно центра"""
        print(f"Масштабирование: sx={sx:.2f}, sy={sy:.2f}, sz={sz:.2f}")
        self.center = self.find_center_by_average(self.transformed_points)
        
        S = [
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ]
        
        
        new_points = []
        for point in self.transformed_points:
            point_h = [point[0], point[1], point[2], 1]
            p1 = self.multiply_matrix_vector(S, point_h)
            new_points.append([p1[0], p1[1], p1[2]])
        
        self.transformed_points = new_points


    def move(self, dx, dy, dz):
        """Матрица переноса"""
        print(f"Перенос: dx={dx}, dy={dy}, dz={dz}")
        M = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [dx, dy, dz, 1]
        ]
        new_points = []
        for point in self.transformed_points:
            point_h = [point[0], point[1], point[2], 1]
            p = self.multiply_matrix_vector(M, point_h)
            new_points.append([p[0], p[1], p[2]])
        
        self.transformed_points = new_points    


    def rotate_x(self, angle_degrees):
        angle = math.radians(angle_degrees)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [
            [1, 0, 0, 0],
            [0, cos_a, sin_a, 0],
            [0, -sin_a, cos_a, 0],
            [0, 0, 0, 1]
        ]
    
    def rotate_y(self, angle_degrees):
        angle = math.radians(angle_degrees)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [
            [cos_a, 0, -sin_a, 0],
            [0, 1, 0, 0],
            [sin_a, 0, cos_a, 0],
            [0, 0, 0, 1]
        ]
    
    def rotate_z(self, angle_degrees):
        angle = math.radians(angle_degrees)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [
            [cos_a, sin_a, 0, 0],
            [-sin_a, cos_a, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    
    def rotate(self, axis, angle_degrees):
        """Поворот вокруг указанной оси относительно центра фигуры"""
        print(f"Поворот вокруг оси {axis} на {angle_degrees}°")
        
        self.center = self.find_center_by_average(self.transformed_points)
        T1 = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-self.center[0], -self.center[1], -self.center[2], 1]
        ]
        
        if axis == 'x':
            R = self.rotate_x(angle_degrees)
        elif axis == 'y':
            R = self.rotate_y(angle_degrees)
        else:
            R = self.rotate_z(angle_degrees)
        
        T2 = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [self.center[0], self.center[1], self.center[2], 1]
        ]
        
        new_points = []
        for point in self.transformed_points:
            point_h = [point[0], point[1], point[2], 1]
            p1 = self.multiply_matrix_vector(T1, point_h)
            p2 = self.multiply_matrix_vector(R, p1)
            p3 = self.multiply_matrix_vector(T2, p2)
            new_points.append([p3[0], p3[1], p3[2]])
        
        self.transformed_points = new_points


    def reflect(self, axis):
        """Отражение относительно оси"""
        print(f"Отражение относительно оси {axis}")
        
        if axis == 'x':
            R = [
                [1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        elif axis == 'y':
            R = [
                [-1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        else:
            R = [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1]
            ]
        
        
        new_points = []
        for point in self.transformed_points:
            point_h = [point[0], point[1], point[2], 1]
            p1 = self.multiply_matrix_vector(R, point_h)
            new_points.append([p1[0], p1[1], p1[2]])
        
        self.transformed_points = new_points


    def reset(self):
        """Сброс к исходному состоянию"""
        print("Сброс")
        self.transformed_points = self.object.copy()
        self.center = self.find_center_by_average(self.object)


    def sign(self, x):
        return 1 if x > 0 else (-1 if x < 0 else 0)
    

    def dda_algorithm(self, x1, y1, x2, y2):
        """Алгоритм ЦДА"""
        points = []

        length = max(abs(x2 - x1), abs(y2 - y1))
        if length == 0:
            return [(x1, y1)]
        
        dx = (x2 - x1) / length
        dy = (y2 - y1) / length
        
        x = x1 + 0.5 * self.sign(dx)
        y = y1 + 0.5 * self.sign(dy)
        points.append((int(x), int(y)))
        
        i = 0
        while i < length:
            x += dx
            y += dy
            points.append((int(x), int(y)))
            i += 1
        
        return points

            
    def draw_object(self):
        points_2d = []

        for point in self.transformed_points:
            points_2d.append(self.project_point(point))
        
        points_to_draw = []

        center_x = self.grid_cols // 2
        center_y = self.grid_rows // 2
        scale = 2

        for edge in self.edges:
            p1 = points_2d[edge[0]]
            p2 = points_2d[edge[1]]
            grid_x1 = int(center_x + p1[0] * scale)
            grid_y1 = int(center_y - p1[1] * scale)  
            grid_x2 = int(center_x + p2[0] * scale)
            grid_y2 = int(center_y - p2[1] * scale)
            
            points_to_draw.extend(self.dda_algorithm(grid_x1, grid_y1, grid_x2, grid_y2))
        
        self.filled_cells = [[False] * self.grid_cols for _ in range(self.grid_rows)]

        for point_2d in points_to_draw:     
            if point_2d:
                x, y = point_2d
                if 0 <= y < self.grid_rows and 0 <= x < self.grid_cols:
                    self.filled_cells[y][x] = True  # сначала Y (строка), потом X (колонка)




if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleZoomGrid(root)
    root.mainloop()



